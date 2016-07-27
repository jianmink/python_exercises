import subprocess

import argparse

TO_APP_NAME = {
'16777250':"STa",
'16777265':"SWx",
'16777272':"S6b",
'16777264':"SWm",
'16777217':"Sh",
'99887766':"SWm+"
               }

NULL_VALUE = "<Empty>"
WILDCARD_SYMBOL = "*"


# todo list
# 1. support multiple value of otpdiaSelector.destination 
# 2. support rm record by record id
# 3. support transaction for immcfg cmd
# 4. support shell mode
# 5. support add/remove hss/dra into/from load-sharing group
# 6. support change priority of failover group
# 7. refresh record_id 


ATTRIBUTE_HAS_MULTI_VALUE = ("host", "applicationId") #, "destination",  )


class OtpdiaObject(object):
    def __init__(self):
        pass
    
    def parse(self, text):
        # extract selected key value pairs from 
        for each in text:
            t = each.split()
            if len(t) > 2:
                
                k = t[0].rstrip()
                if k in ATTRIBUTE_HAS_MULTI_VALUE:
                    value_list = [each.rstrip() for each in t[2:] if '(' not in each ]
                    
                    self.key_value_pairs[k] = value_list
                else:
                    v = t[2].rstrip()    
                    self.key_value_pairs[k] = v
        
         
    
class Selector(OtpdiaObject):   
        
    def parse(self, text):
        self.key_value_pairs={}
        super(Selector,self).parse(text)
            
        self.app = self.key_value_pairs['applicationId']
        self.service = self.key_value_pairs['service']
        self.destination = self.key_value_pairs['destination']
        self.peer = self.key_value_pairs['peer']
        self.rdn = self.key_value_pairs['otpdiaSelector']
        
        return self

    def to_string(self):
        return ("service='%s'\n"
        "applicationId='%s'\n"
        "destination='%s'\n"
        "peer='%s'\n" %(self.service, self.app, self.destination, self.peer))
        
    
class Link(OtpdiaObject):        
    def parse(self, text):
        self.key_value_pairs={} 
        super(Link,self).parse(text)
                    
        self.data = self.key_value_pairs['head']
        self.next = self.key_value_pairs['tail']
        self.rdn =  self.key_value_pairs['otpdiaCons']

        return self
    
    def to_string(self):
        return ("data='%s'\n"
        "next='%s'\n" %(self.data, self.next))
        

class Domain(OtpdiaObject):    
    def parse(self, text):
        self.key_value_pairs={}
        super(Domain,self).parse(text)
            
        self.realm = self.key_value_pairs['realm']
        self.host = self.key_value_pairs['host']
        self.rdn = self.key_value_pairs['otpdiaDomain']

        return self
        
    def to_string(self):
        if self.host == [NULL_VALUE,]:
            host = WILDCARD_SYMBOL
        else:
            host = self.host
            
        if self.realm == NULL_VALUE:
            realm = WILDCARD_SYMBOL
        else:
            realm = self.realm
            
        return ("host = %s,  realm = %s" %(host, realm))

class OtpdiaObjectFactory(object):
    @staticmethod
    def create(class_name):
        if class_name == "OtpdiaSelector":
            return Selector()
        elif class_name == "OtpdiaCons":
            return Link()
        elif class_name == "OtpdiaDomain":
            return Domain()
        else:
            return None

class IMMCFG():
    def __init__(self):
        
        self.SERVICE_DN="otpdiaService=epc_aaa,otpdiaProduct=AAAServer"
        pass
    
    def rm_imm_object(self, rdn):
#         rdn = "otpdiaCons=link_to_" + host + "_" + realm
        cmd_rm = "immcfg -d " + rdn
        print cmd_rm
        
        run_command(cmd_rm)
    
    
    def add_otpdiaselector(self, app, host, realm, peer):
        # dest: (host,realm)
        rdn = "otpdiaSelector=selector_" + host + "_" + realm
        cmd_create = 'immcfg -c OtpdiaSelector %s -a peer="%s" -a  service="%s"' %(rdn, peer.rdn, self.SERVICE_DN )
        print cmd_create
        run_command(cmd_create)
        
        for each in app:
            cmd_set = "immcfg -a app+=%s %s" %(each,rdn)
            print cmd_set
            run_command(cmd_set)
    
    def add_otpdiacons(self, domain):
        rdn =  "otpdiaCons=link_to_" + domain.host+"_" + domain.realm
        
        cmd_create = "immcfg -c OtpdiaCons %s -a head=%s" %(rdn, domain.rdn)
        print cmd_create
        run_command(cmd_create)
    
    
    def add_otpdiadomain(self, host, realm):
        # cmd example:
        #     immcfg -c OtpdiaDomain otpdiaDomain=domain_hss3 -a realm=ericsson.se
        #     immcfg -a host=hss3 otpdiaDomain=domain_hss3  
        
        rdn = "otpdiaDomain=domain_" + host+"_" + realm
        
        cmd_create = "immcfg -c OtpdiaDomain %s -a head=%s" %(rdn)
        print cmd_create
        run_command(cmd_create)
        
        cmd_set = "immcfg -a host=%s %s" %(host,rdn)
        print cmd_set
        run_command(cmd_set)
        
    
    
    def load(self, class_name="OtpdiaSelector"):
        dict_={}
        command = "immfind -c " + class_name 
        for line in run_command(command):
            cmd = "immlist "+line
            
            text = run_command(cmd)
            s = OtpdiaObjectFactory.create(class_name).parse(text)
            dict_[line.rstrip()]=s
        return dict_
    

class IMM(object):
    def __init__(self):
        self.selectors={}
        self.links={}
        self.domains={}
        self.immcfg = IMMCFG()
        
    
    def load(self):
        self.selectors=self.immcfg.load("OtpdiaSelector")
        self.links = self.immcfg.load("OtpdiaCons")
        self.domains = self.immcfg.load("OtpdiaDomain")
    
     
    def sizeof_links(self, link_head):
        
        link = link_head
        count = 1
        while link.next != NULL_VALUE:
            
            count += 1
            link = self.links[link.next]
            
        return count
            
    def rm_selector(self, rdn):
        selector = self.selectors[rdn]
        
        link_head = self.links[selector.peer]
        
        link_size = self.sizeof_links(link_head)
        if  link_size == 1:
            print "INFO: link size is one, so remove the selector"
            self.selectors.pop(rdn)
            # todo: invoke IMM CFG -d command
        else:
            print "INFO: link size is %d" %(link_size)
            
    
    def add_selector(self, app, dest, peer):
        s = Selector()
        
        s.app = app
        s.destination = dest.rdn
        s.peer = peer.rdn
        s.rdn = ("otpdiaSelector=%s_%s" %(''.join(dest.host), dest.realm) )
        
        if s.rdn not in self.selectors.keys():
            self.selectors[s.rdn] = s
            
        return s
        
            
    def add_domain(self,host, realm):
        d = Domain()
        
        if len(host) == 0 or host[0] == NULL_VALUE:
            d.rdn = ("otpdiaDomain=_%s" %(realm))
        else:
            d.rdn = ("otpdiaDomain=%s_%s" %(''.join(host), realm))
        d.host = host
        d.realm = realm
        
        self.domains[d.rdn] = d
        
        return d
        
         
    def add_link(self, domain):
        n = Link()
        
        n.rdn =("otpdiaCons=%s_%s" %(''.join(domain.host), domain.realm))
        n.next = NULL_VALUE
        n.data = domain.rdn
        
        if n.rdn not in self.links.keys():
            self.links[n.rdn] = n
        
        return n
    
    def rm_domain(self, rdn):
        
        self.domains.pop(rdn)
        
        self.immcfg.rm_imm_object(rdn)
        
    def rm_link(self, h_rdn, rdn):
        
        if self.sizeof_links(self.links[h_rdn]) == 1:
            self.links.pop(rdn)
            self.immcfg.rm_imm_object(rdn)
            return NULL_VALUE
            
        if h_rdn == rdn: # link head
            node = self.links.pop(rdn)
            self.immcfg.rm_imm_object(rdn)
            return node.next
        # else
        else:
            pre_node = None
            for each in self.links.values():
                if each.next == rdn:
                    pre_node = each 
                    break
            
            node = self.links.pop(rdn)
            self.immcfg.rm_imm_object(rdn)
        
            pre_node.next = node.next 
            
            return h_rdn


class RouteRecord(object):
    def __init__(self, record_id, selector, dest, peer, priority):
        
        self.record_id = record_id
        self.selector = selector
        self.app = selector.app
        self.dest = dest 
        self.peer = peer
        self.priority = priority
    
    def rm(self, imm):
        
        imm.rm_selector(self.selector.rdn)
        
        link_head_rdn = imm.rm_link(self.selector.peer, self.peer.rdn)
        
        if self.selector.rdn in imm.selectors:
            imm.selectors[self.selector.rdn].peer = link_head_rdn
        
        imm.rm_domain(self.dest.rdn) 
    
    
    def to_string(self):
        pass
             
                

class RouteTable(object):
    def __init__(self, imm):
        self.imm = imm
        
        self.records=[]
        record_id = 1
        for selector in self.imm.selectors.values():
            
            link = self.imm.links[selector.peer]
            priority=1
            
            while True:
                domain_dest = self.imm.domains[selector.destination]
                
                record = RouteRecord(record_id,
                                     selector, 
                                     domain_dest, 
                                     link,
                                     priority)
                
                record_id += 1
                 
                self.records.append(record)
                
                if link.next == NULL_VALUE: 
                    break 
                else:
                    link = self.imm.links[link.next]
                    priority +=1
                    
        self.last_record_id = record_id
        
    def to_string(self, f="TABLE"):
        if f == "TABLE":
            return self.to_table()
        else:
            return self.to_text()
        
    
    def to_table(self):
        head = "| id |  app  |" +" "*20 + "dest" + " "*20 + "|" + " "*20 + "peer" + " "*20 + "| priority \n"
        
        line_separator = "|" + "-"*len(head) + "|\n"
        
        str_ = "Route Table:  \n"
        str_ += line_separator + head + line_separator

        for record in self.records:
            str_ += ("|%4d|%7s|%-44s|%-44s|%10d\n"
                        %(record.record_id, ' '.join([TO_APP_NAME[each] for each in record.app]),
                        record.dest.to_string(),
                        self.imm.domains[record.peer.data].to_string(),
                        record.priority)
                    )
            
            str_ += line_separator
             
        return str_

    def to_text(self):
        line_separator = "" + "-"*32 + "\n"
        
        str_ = "Route Table Text:  \n"

        for record in self.records:
            str_ += line_separator 
            str_ += "id:       " + str(record.record_id) + '\n'
            str_ += "app:      " + (' '.join([TO_APP_NAME[each] for each in record.app])) + "\n"
            str_ += "dest:     " + record.dest.to_string() + '\n'
            str_ += "peer:     " + self.imm.domains[record.peer.data].to_string() + '\n'
            str_ += "priority: " + str(record.priority) +'\n'
            str_ += "\n"
             
        return str_

    def rm(self, app, dest, peer):
                
        # find
        for record in self.records:
            domain_d = record.dest
            domain_p = self.imm.domains[record.peer.data]
            if (record.app == app and 
                (domain_d.host, domain_d.realm) == dest and
                (domain_p.host, domain_p.realm) == peer ):
                self.rm_one_record(record)
                
    def add(self, app, dest, peer):
        
        d1 = self.imm.add_domain(dest[0], dest[1])
        
        d2 = self.imm.add_domain(peer[0], peer[1])
        
        link = self.imm.add_link(d2)
        
        selector = self.imm.add_selector(app, d1, link)
        
        self.last_record_id += 1
        record = RouteRecord(self.last_record_id, selector, d1, link, 3)
        
        self.records.append(record)
        
                
    def rm_one_record(self, record):
        record.rm(self.imm)
        
        # adjust priority of remaining record
        self.records.remove(record)        
    
    def rm_by_id(self, record_id):
        for record in self.records:
            if record.record_id == record_id:
                self.rm_one_record(record)
                return
        
        print "ERROR: no record found with id " + str(record_id)
        
             
def run_command(command):
    p = subprocess.Popen(command,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')




def list_route_table(output_format):
    imm = IMM()
    imm.load()
    route_table = RouteTable(imm)
    print route_table.to_string(output_format)    

def add(args):
    imm = IMM()
    imm.load()
    if not args.host:
        host = 'wildcard'
    else:
        host = args.host
        
    if not args.realm:
        print "please give the realm value"
        return False
    
    imm.add_domain(host, args.realm)

def rm(args):
    imm = IMM()
    imm.load()
    if not args.host:
        host = 'wildcard'
    else:
        host = args.host
        
    if not args.realm:
        print "please give the realm value"
        return False
    
    imm.rm_domain(host, args.realm)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cmd",  choices=('list', 'add', 'rm'))
    parser.add_argument("--host")
    parser.add_argument("--realm")
    parser.add_argument("--format", default="TABLE")
    args = parser.parse_args()

    if args.cmd == "list" :
        list_route_table(args.format)
    elif args.cmd == "add" :
        add(args)
    elif args.cmd == "rm":
        rm(args)
    else:
        parser.print_help()
    
