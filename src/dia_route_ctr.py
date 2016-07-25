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



'''
SC-1:~ # immlist -c OtpdiaDomain

<< OtpdiaDomain - CONFIG >>
realm : SA_STRING_T [1] {CONFIG, WRITEABLE, INITIALIZED}
otpdiaDomain : SA_STRING_T [1] {RDN, CONFIG, INITIALIZED}
host : SA_STRING_T [0..*] = Empty {CONFIG, WRITEABLE, MULTI_VALUE}
SC-1:~ # immlist -c OtpdiaCons  

<< OtpdiaCons - CONFIG >>
tail : SA_NAME_T [0] = Empty {CONFIG, WRITEABLE}
otpdiaCons : SA_STRING_T [1] {RDN, CONFIG, INITIALIZED}
head : SA_NAME_T [1] {CONFIG, WRITEABLE, INITIALIZED}
SC-1:~ # immlist -c OtpdiaSelector

<< OtpdiaSelector - CONFIG >>
service : SA_NAME_T [1..*] {CONFIG, WRITEABLE, INITIALIZED, MULTI_VALUE}
peer : SA_NAME_T [1] {CONFIG, WRITEABLE, INITIALIZED}
otpdiaSelector : SA_STRING_T [1] {RDN, CONFIG, INITIALIZED}
destination : SA_NAME_T [0..*] = Empty {CONFIG, WRITEABLE, MULTI_VALUE}
applicationId : SA_UINT32_T [0..*] = Empty {CONFIG, WRITEABLE, MULTI_VALUE}

'''

ATTRIBUTE_HAS_MULTI_VALUE = ("host",) # "service", "destination", "applicationId" )


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
    def __init__(self):
        self.application_id = 0
        self.destination = None
        self.peer = None
        self.service = ""
        self.key_value_pairs={}
        
    def parse(self, text):
        
        super(Selector,self).parse(text)
            
        self.application_id = self.key_value_pairs['applicationId']
        self.service = self.key_value_pairs['service']
        self.destination = self.key_value_pairs['destination']
        self.peer = self.key_value_pairs['peer']
        self.rdn = self.key_value_pairs['otpdiaSelector']
        
        return self

    def to_string(self):
        return ("service='%s'\n"
        "applicationId='%s'\n"
        "destination='%s'\n"
        "peer='%s'\n" %(self.service, self.application_id, self.destination, self.peer))
        
    
class Link(OtpdiaObject):

    def __init__(self):
        self.data = None
        self.next = None
        self.key_value_pairs={} 
        
    def parse(self, text):
        super(Link,self).parse(text)
                    
        self.data = self.key_value_pairs['head']
        self.next = self.key_value_pairs['tail']
        self.rdn =  self.key_value_pairs['otpdiaCons']

        return self
    
    def to_string(self):
        return ("data='%s'\n"
        "next='%s'\n" %(self.data, self.next))
        

class Domain(OtpdiaObject):
    
    def __init__(self):
        self.realm = ""
        self.host = ""
        self.key_value_pairs={}
    
    def parse(self, text):
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
            
        return ("(%s , %s)" %(host, realm))


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
        
        cmd_set = "immcfg -a app=%s %s" %(app,rdn)
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
    

class IMMDB(object):
    def __init__(self):
        self.selectors={}
        self.links={}
        self.domains={}
        self.immcfg = IMMCFG()
        
    
    def load(self):
        self.selector=self.load_selector()
        self.links = self.load_link()
        self.domains = self.load_domain()
    

    def find_selector(self, rdn):
        return self.selectors[rdn]
    
    def find_link(self, rdn):
        return self.links[rdn]
    
    def find_domain(self,rdn):
        return self.domains[rdn]
    
    def load_selector(self):
        command = "immfind | grep otpdiaSelector"
        for line in run_command(command):
            cmd = "immlist "+line
            
            text = run_command(cmd)
            s = Selector().parse(text)
            self.selectors[line.rstrip()]=s
            
            
    def load_link(self):
        command = "immfind | grep otpdiaCons"
        for line in run_command(command):
            cmd = "immlist "+line
            
            text = run_command(cmd)
            s = Link().parse(text)
            self.links[line.rstrip()]=s
            
    
    def load_domain(self):
        command = "immfind | grep otpdiaDomain"
        for line in run_command(command):
            cmd = "immlist "+line
            
            text = run_command(cmd)
            s = Domain().parse(text)
            self.domains[line.rstrip()]=s
     
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
            # todo: invoke IMM CFG -d command
        else:
            print "INFO: link size is %d" %(link_size)
            
    
    def add_selector(self):
        pass
            
    def add_domain(self,host, realm):
        pass
         
    def add_link(self, host, realm):
        pass
    
    def rm_domain(self, rdn):
        self.immcfg.rm_imm_object(rdn)
        
    def rm_link(self, rdn):
        self.immcfg.rm_imm_object(rdn)


class RouteRecord(object):
    def __init__(self, selector, dest, peer, priority):
        
        self.selector = selector
        
        self.app = selector.application_id
        self.dest = dest 
        self.peer = peer
        self.priority = priority
    
    def to_string(self):
        pass
             
                

class RouteTable(object):
    def __init__(self, imm):
        self.imm = imm
        
        self.records=[]
        for selector in self.imm.selectors.values():
            
            link = self.imm.links[selector.peer]
            priority=1
            
            while True:
                domain_dest = self.imm.domains[selector.destination]
                
                record = RouteRecord(selector, 
                                     domain_dest, 
                                     link,
                                     priority)
                
                self.records.append(record)
                
                if link.next == NULL_VALUE: 
                    break 
                else:
                    link = self.imm.links[link.next]
                    priority +=1
                    
        
    def to_string(self):
        head = "| app |" +" "*15 + "dest" + " "*15 + "|" + " "*15 + "peer" + " "*15 + "| priority \n"
        line_separator = "|" + "-"*len(head) + "|\n"
        
        str_ = "Route Table:  \n"
        str_ += line_separator + head + line_separator

        for record in self.records:
            str_ += ("|%5s|%-34s|%-34s|%10d\n"
                        %(TO_APP_NAME[record.app],
                        record.dest.to_string(),
                        self.imm.domains[record.peer.data].to_string(),
                        record.priority)
                    )
            str_ += line_separator
             
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
        
        d1 = self.imm.add_domain(dest.host, dest.realm)
        
        d2 = self.imm.add_domain(peer.host, peer.realm)
        
        link = self.imm.add_link(d2)
        
        self.imm.add_selector(app, d1, link)
        
                
    def rm_one_record(self, record):
        # todo: adjust priority of remaining node
        # 
        self.records.remove(record)
        
        self.imm.rm_selector(record.selector.rdn)
        self.imm.rm_link(record.peer.rdn)
        self.imm.rm_domain(record.dest.rdn)           
                
                    

def run_command(command):
    p = subprocess.Popen(command,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')




def list_route_table():
    imm = IMMDB()
    imm.load()
    route_table = RouteTable(imm.selectors,imm.link,imm.domains)
    print route_table.to_string()    

def add(args):
    imm = IMMDB()
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
    imm = IMMDB()
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
    args = parser.parse_args()

    if args.cmd == "list" :
        list_route_table()
    elif args.cmd == "add" :
        add(args)
    elif args.cmd == "rm":
        rm(args)
    else:
        parser.print_help()
    
