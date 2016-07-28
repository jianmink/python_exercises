import subprocess
import time
import argparse

TO_APP_NAME = {
'16777250':"STa",
'16777265':"SWx",
'16777272':"S6b",
'16777264':"SWm",
'16777217':"Sh",
'99887766':"SWm+"
               }

TO_APP_ID = {
"STa":'16777250',
"SWx":'16777265',
"S6b": '16777272',
"SWm": '16777264',
"Sh":  '16777217',
"SWm+": '99887766'
               }

NULL_VALUE = "<Empty>"
WILDCARD_SYMBOL = "*"
IMMCFG_SLEEP_TIME = 0.1

# function list:
# 1. list route table
# 2. list route record in text mode
# 3. rm route record by record id
# 4. add route record

# todo list
# support multiple value of otpdiaSelector.dest 
# support transaction for immcfg cmd
# support shell mode
# support add/remove hss/dra into/from load-sharing group
# support change priority of failover group
# refresh record id and priority 


ATTRIBUTE_HAS_MULTI_VALUE = ("host", "applicationId") #, "dest",  )


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
        
         
    
class OtpdiaSelector(OtpdiaObject):   
    '''
        Rename the attribute to make the meaning clear.
        
        original name in IMM class |  name in python OtpdiaCons class 
             peer                  |     link_head
    '''
    
    def parse(self, text):
        self.key_value_pairs={}
        super(OtpdiaSelector,self).parse(text)
            
        self.applicationId = self.key_value_pairs['applicationId']
        self.service = self.key_value_pairs['service']
        self.destination = self.key_value_pairs['destination']
        self.link_head = self.key_value_pairs['peer']
        self.rdn = self.key_value_pairs['otpdiaSelector']
        
        return self

    def to_string(self):
        return ("service='%s'\n"
        "applicationId='%s'\n"
        "destination='%s'\n"
        "peer='%s'\n" %(self.service, self.applicationId, self.destination, self.link_head))
        
    
class OtpdiaCons(OtpdiaObject): 
    '''
        Rename the attribute to make the meaning clear.
        
        original name in IMM class |  name in python OtpdiaCons class 
             head                  |     data
             tail                  |     next
    '''
           
    def parse(self, text):
        self.key_value_pairs={} 
        super(OtpdiaCons,self).parse(text)
                    
        self.data = self.key_value_pairs['head']
        self.next = self.key_value_pairs['tail']
        self.rdn =  self.key_value_pairs['otpdiaCons']

        return self
    
    def to_string(self):
        return ("data='%s'\n"
        "next='%s'\n" %(self.data, self.next))
        

class OtpdiaDomain(OtpdiaObject):    
    def parse(self, text):
        self.key_value_pairs={}
        super(OtpdiaDomain,self).parse(text)
            
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
            return OtpdiaSelector()
        elif class_name == "OtpdiaCons":
            return OtpdiaCons()
        elif class_name == "OtpdiaDomain":
            return OtpdiaDomain()
        else:
            return None

class IMMCFG():
    def __init__(self):
        self.SERVICE_DN="otpdiaService=epc_aaa,otpdiaProduct=AAAServer"
    
    def rm_imm_object(self, rdn, time_wait=0):
        cmd_rm = "immcfg -d " + rdn
        print cmd_rm
        
        if time_wait != 0: time.sleep(time_wait)
        
        output = run_command(cmd_rm)
        if output and "ERR_BAD_OPERATIONself" in ''.join(output):
            if time_wait != 0: time.sleep(time_wait)
            run_command(cmd_rm)
        
        for each in output:
            print each
        
    def modify_imm_object(self,rdn,key, value):
        if value == NULL_VALUE: 
            value = ''
        cmd = "immcfg -a %s=%s %s" %(key, value, rdn)
        print cmd
        
        run_command(cmd)
    
    
    def add_otpdiaselector(self, selector):
        # dest: (host,realm)
        rdn = selector.rdn
        
        cmd_create = 'immcfg -c OtpdiaSelector %s -a peer="%s" -a  service="%s"' %(rdn, selector.peer, self.SERVICE_DN )
        print cmd_create
        run_command(cmd_create)
        
        for each in selector.apps:
            cmd_set = "immcfg -a apps+=%s %s" %(each,rdn)
            print cmd_set
            run_command(cmd_set)
            
        cmd_set = "immcfg -a destination+=%s %s" %(selector.destination,rdn)
        print cmd_set
        run_command(cmd_set)
    
    def add_otpdiacons(self, link, domain):
        cmd_create = "immcfg -c OtpdiaCons %s -a head=%s" %(link.rdn, domain.rdn)
        print cmd_create
        run_command(cmd_create)
    
    
    def add_otpdiadomain(self, domain):
        # cmd example:
        #     immcfg -c OtpdiaDomain otpdiaDomain=domain_hss3 -a realm=ericsson.se
        #     immcfg -a host=hss3 otpdiaDomain=domain_hss3  
        
        rdn = domain.rdn
        hosts = domain.host
        realm = domain.realm
        
        cmd_create = "immcfg -c OtpdiaDomain %s -a realm=%s" %(rdn, realm)
        print cmd_create
        run_command(cmd_create)
        
        for host in hosts:
            cmd_set = "immcfg -a host+=%s %s" %(host,rdn)
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
        
        link_head = self.links[selector.link_head]
        
        link_size = self.sizeof_links(link_head)
        if  link_size == 1:
            print "INFO: link size is one, so remove the selector"
            self.selectors.pop(rdn)
            self.immcfg.rm_imm_object(rdn)
            self.rm_domain(selector.destination)

        else:
            print "INFO: link size is %d" %(link_size)
        
            
    
    def add_selector(self, app, dest, peer):
        s = OtpdiaSelector()
        
        s.applicationId = app
        s.destination = dest.rdn
        s.link_head = peer.rdn
        s.rdn = ("otpdiaSelector=%s_%s" %(''.join(dest.host), dest.realm) )
        
        if s.rdn not in self.selectors.keys():
            self.selectors[s.rdn] = s
            self.immcfg.add_otpdiaselector(s)
        
        
        return s
        
            
    def add_domain(self, hosts, realm):
        
        d = OtpdiaDomain()
        
        if len(hosts) == 0 or hosts[0] == NULL_VALUE or hosts[0] == WILDCARD_SYMBOL:
            d.rdn = ("otpdiaDomain=_%s" %(realm))
        else:
            d.rdn = ("otpdiaDomain=%s_%s" %(''.join(hosts), realm))
        
        d.host = hosts
        d.realm = realm
        
        if d.rdn in self.domains.keys():
            return self.domains[d.rdn]
        
        self.domains[d.rdn] = d
        
        self.immcfg.add_otpdiadomain(d)
        
        return d
        
         
    def add_link(self, domain):
        n = OtpdiaCons()
        
        n.rdn =("otpdiaCons=%s_%s" %(''.join(domain.host), domain.realm))
        n.next = NULL_VALUE
        n.data = domain.rdn
        
        if n.rdn in self.links.keys():
            return self.links[n.rdn]
        
        self.links[n.rdn] = n
        self.immcfg.add_otpdiacons(n, domain)
        
        return n
    
    
    def rm_domain(self, rdn):
        
        if rdn in self.domains.keys():
            self.domains.pop(rdn)
        
        self.immcfg.rm_imm_object(rdn)
        
    def rm_link(self, selector, rdn):
        
        h_rdn = selector.link_head
        
        if self.sizeof_links(self.links[h_rdn]) == 1:
            node = self.links.pop(rdn)
            self.immcfg.rm_imm_object(rdn)
            
            self.rm_domain(node.data)
            
        elif h_rdn == rdn: # link head
            node = self.links.pop(rdn)
            
            self.immcfg.modify_imm_object(selector.rdn, "peer", node.next )
            
            self.immcfg.rm_imm_object(rdn, IMMCFG_SLEEP_TIME)
                
            self.rm_domain(node.data)
            
            selector.peer = node.next
        # else
        else:
            pre_node = None
            for each in self.links.values():
                if each.next == rdn:
                    pre_node = each 
                    break
            
            node = self.links.pop(rdn)
        
            self.immcfg.modify_imm_object(pre_node.rdn, "tail", NULL_VALUE )
            
            # issue: Validation error (BAD_OPERATION) reported by implementer 'C-diameter', if immcfd -d immediatelly 
            # the workaround is to sleep and retry
            self.immcfg.rm_imm_object(rdn, IMMCFG_SLEEP_TIME)
            
            self.rm_domain(node.data)
        
            pre_node.next = node.next 
            

class RouteRecord(object):
    def __init__(self, record_id, selector, dest, peer, priority):
        
        self.record_id = record_id
        self.selector = selector
        self.apps = selector.applicationId
        self.dest = dest 
        self.peer = peer
        self.priority = priority
    
    def rm_imm_objects(self, imm):
        imm.rm_selector(self.selector.rdn)
        imm.rm_link(self.selector, self.peer.rdn)
        
    def add_imm_objects(self, imm):
        imm.add_domain(self.dest)
        imm.add_domain(self.peer)
        imm.add_link(self.peer)
        imm.add_selector(self.selector)
                
    def to_string(self, imm):
        str_= ""
        str_ += "id:       " + str(self.record_id) + '\n'
        str_ += "app:      " + (' '.join([TO_APP_NAME[each] for each in self.apps])) + "\n"
        str_ += "dest:     " + self.dest.to_string() + '\n'
        str_ += "peer:     " + imm.domains[self.peer.data].to_string() + '\n'
        str_ += "priority: " + str(self.priority) +'\n'
        str_ += "\n"
        return str_
             
                

class RouteTable(object):
    def __init__(self, imm):
        self.imm = imm
        
        self.records=[]
        record_id = 1
        for selector in self.imm.selectors.values():
            
            link = self.imm.links[selector.link_head]
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
        head = "| id |  apps  |" +" "*20 + "dest" + " "*20 + "|" + " "*20 + "peer" + " "*20 + "| priority \n"
        
        line_separator = "|" + "-"*len(head) + "|\n"
        
        str_ = "Route Table:  \n"
        str_ += line_separator + head + line_separator

        for record in self.records:
            str_ += ("|%4d|%7s|%-44s|%-44s|%10d\n"
                        %(record.record_id, ' '.join([TO_APP_NAME[each] for each in record.apps]),
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
            str_ += record.to_string(self.imm)
            str_ += "\n"
             
        return str_

    def rm_by_route_items(self, app, dest, peer):
        # find
        for record in self.records:
            domain_d = record.dest
            domain_p = self.imm.domains[record.peer.data]
            if (record.apps == app and 
                (domain_d.host, domain_d.realm) == dest and
                (domain_p.host, domain_p.realm) == peer ):
                self.rm_record(record)
                
    def add(self, app, dest, peer):
        # add selector.dest
        d1 = self.imm.add_domain(dest[0], dest[1])
        
        # add domain peer 
        d2 = self.imm.add_domain(peer[0], peer[1])
        
        # add link to domain peer
        link = self.imm.add_link(d2)
        
        # add selector 
        selector = self.imm.add_selector(app, d1, link)
        
        self.last_record_id += 1
        record = RouteRecord(self.last_record_id, selector, d1, link, 3)
        
        self.records.append(record)
        
                
    def rm_record(self, record):
        record.rm_imm_objects(self.imm)
        
        # adjust priority of remaining record
        self.records.remove(record)        
    
    def rm_by_id(self, record_id):
        for record in self.records:
            if int(record.record_id) == record_id:
                self.rm_record(record)
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
    
    # SWx 
    # (*, hss.com)  
    # ('hss1', 'hss.com')
    
    imm = IMM()
    imm.load()
    route_table = RouteTable(imm)
    
    app = args.apps
    if not app:
        print "please provide apps, e.g. SWx"
        return 
    
    appid = [TO_APP_ID(app),]
    
    host, realm = args.dest[1:-1].split(',')
    
    if host == '*':
        dest = ([''], realm)
    else:
        dest = ([host,], realm)

    
    host, realm = args.peer[1:-1].split(',')
    
    peer = ([host,], realm)
    
    print appid, dest, peer
    
    route_table.add(appid, dest, peer )
                    
def rm(args):
    imm = IMM()
    imm.load()
    route_table = RouteTable(imm)
    
    if not args.record:
        print "please provide the id of route record to be removed"
        print "use list cmd to print the route table"
        return 
    
    route_table.rm_by_id(int(args.record))

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cmd",  choices=('list', 'add', 'rm'))
    
    # for add cmd
    parser.add_argument("--apps")
    parser.add_argument("--dest")
    parser.add_argument("--peer")
    
    # for rm cmd
    parser.add_argument("--record")
    
    # for list cmd
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
    
