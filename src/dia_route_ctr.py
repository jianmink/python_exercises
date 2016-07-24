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


class OtpdiaObject(object):
    def __init__(self):
        pass
    
    def parse(self, text):
        # extract selected key value pairs from 
        for each in text:
            t = each.split()
            if len(t) > 2:
                self.key_value_pairs[t[0].rstrip()] = t[2].rstrip()
        
         
    
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
        if self.host == NULL_VALUE:
            host = WILDCARD_SYMBOL
        else:
            host = self.host
            
        if self.realm == NULL_VALUE:
            realm = WILDCARD_SYMBOL
        else:
            realm = self.realm
            
        return ("(%s , %s)" %(host, realm))



class IMMDB(object):
    def __init__(self):
        self.selectors={}
        self.links={}
        self.domains={}
        
    
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
            
            
    def rm_otpdia_selector(self):
        pass
    
    def add_otpdia_selector(self):
        pass
            
    def add_otpdia_domain(self,host, realm):
        # cmd example:
        #     immcfg -c OtpdiaDomain otpdiaDomain=domain_hss3 -a realm=ericsson.se
        #     immcfg -a host=hss3 otpdiaDomain=domain_hss3  
        
        rdn =  "otpdiaDomain=domain_"+host+"_"+realm
        cmd_create_domain = "immcfg -c OtpdiaDomain %s -a realm=%s" %(rdn, realm)
        cmd_set_host = "immcfg -a host=%s %s" %(host,rdn)
        
        print cmd_create_domain
        run_command(cmd_create_domain)
        
        print cmd_set_host
        run_command(cmd_set_host)
         
    def rm_otpdia_domain(self, host, realm):
        rdn = "otpdiaDomain=con_to_domain_"+host+"_"+realm
        cmd_rm_domain = "immcfg -d "+rdn
        print cmd_rm_domain
        
        run_command(cmd_rm_domain)
    
    
    def add_otpdia_con(self, host, realm):
        # cmd example:
        #     immcfg -c OtpdiaDomain otpdiaDomain=domain_hss3 -a realm=ericsson.se
        #     immcfg -a host=hss3 otpdiaDomain=domain_hss3  
        
        domain_rdn = "otpdiaDomain=domain_" + host+"_" + realm
        rdn =  "otpdiaCons=con_to_domain_" + host+"_" + realm
        
        cmd_create_otpdia_con = "immcfg -c OtpdiaCons %s -a head=%s" %(rdn, domain_rdn)
    #     cmd_set_host = "immcfg -a host=%s %s" %(host,rdn)
        
        print cmd_create_otpdia_con
        run_command(cmd_create_otpdia_con)
        
    def rm_otpdia_con(self, host, realm):
        rdn = "otpdiaDomain=con_to_domain_"+host+"_"+realm
        cmd_rm_con = "immcfg -d " + rdn
        print cmd_rm_con
        
        run_command(cmd_rm_con)


class RouteRecord(object):
    def __init__(self, app, dest, peer, priority):
        self.app = app
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
                
                record = RouteRecord(selector.application_id, 
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
                
                self.records.remove(record)
                
                self.imm.rm_otpdia_selector(record.)
                self.imm.rm_otpdia_domain(record.peer)
                
                
                
                    

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
    
    imm.add_otpdia_domain(host, args.realm)

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
    
    imm.rm_otpdia_domain(host, args.realm)

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
    
