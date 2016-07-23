
import subprocess
import argparse

TO_APP_NAME = {
'16777250':"STA",
'16777265':"SWX",
'16777272':"S6B",
'16777264':"SWM",
'16777217':"SH",
'99887766':"SWM+"
               }


NULL_VALUE = "<Empty>"
WILDCARD_SYMBOL = "*"

class Selector(object):
    """
    immlist otpdiaSelector=selector_1 
    Name                                               Type         Value(s)
    ========================================================================
    service                                            SA_NAME_T    otpdiaService=epc_aaa,otpdiaProduct=AAAServer (45) 
    peer                                               SA_NAME_T    otpdiaCons=con_hss (18) 
    otpdiaSelector                                     SA_STRING_T  otpdiaSelector=selector_1 
    destination                                        SA_NAME_T    otpdiaDomain=domain_hss (23) 
    applicationId                                      SA_UINT32_T  16777265 (0x1000031)
    SaImmAttrImplementerName                           SA_STRING_T  C-diameter 
    SaImmAttrClassName                                 SA_STRING_T  OtpdiaSelector 
    SaImmAttrAdminOwnerName                            SA_STRING_T  <Empty>
    """
    
    def __init__(self):
        self.application_id = 0
        self.destination = None
        self.peer = None
        self.service = ""
        
    def parse(self, text):
        key_value_pairs={}
        for each in text:
            t = each.split()
            if len(t) > 2:
                key_value_pairs[t[0].rstrip()]=t[2].rstrip()
            
        self.application_id = key_value_pairs['applicationId']
        self.service = key_value_pairs['service']
        self.destination = key_value_pairs['destination']
        self.peer = key_value_pairs['peer']
        
        return self

    def to_string(self):
        return ("service='%s'\n"
        "applicationId='%s'\n"
        "destination='%s'\n"
        "peer='%s'\n" %(self.service, self.application_id, self.destination, self.peer))
        
    
class Link(object):
    """
    immlist otpdiaCons=con_hss 
    Name                                               Type         Value(s)
    ========================================================================
    tail                                               SA_NAME_T    <Empty>
    otpdiaCons                                         SA_STRING_T  otpdiaCons=con_hss 
    head                                               SA_NAME_T    otpdiaDomain=domain_hss (23) 
    SaImmAttrImplementerName                           SA_STRING_T  C-diameter 
    SaImmAttrClassName                                 SA_STRING_T  OtpdiaCons 
    SaImmAttrAdminOwnerName                            SA_STRING_T  <Empty>
    """
    def __init__(self):
        self.data = None
        self.next = None 
        
    def parse(self, text):
        key_value_pairs={}
        for each in text:
            t = each.split()
            if len(t) > 2:
                key_value_pairs[t[0].rstrip()]=t[2].rstrip()
            
        self.data = key_value_pairs['head']
        self.next = key_value_pairs['tail']

        return self
    
    def to_string(self):
        return ("data='%s'\n"
        "next='%s'\n" %(self.data, self.next))
        

class Domain(object):
    """
    immlist otpdiaDomain=domain_hss 
    Name                                               Type         Value(s)
    ========================================================================
    realm                                              SA_STRING_T  hss.com 
    otpdiaDomain                                       SA_STRING_T  otpdiaDomain=domain_hss 
    host                                               SA_STRING_T  <Empty>
    SaImmAttrImplementerName                           SA_STRING_T  C-diameter 
    SaImmAttrClassName                                 SA_STRING_T  OtpdiaDomain 
    SaImmAttrAdminOwnerName                            SA_STRING_T  <Empty>
    """
    def __init__(self):
        self.realm = ""
        self.host = ""
    
    def parse(self, text):
        key_value_pairs={}
        for each in text:
            t = each.split()
            if len(t) > 2:
                key_value_pairs[t[0].rstrip()]=t[2].rstrip()
            
        self.realm = key_value_pairs['realm']
        self.host = key_value_pairs['host']

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
        

class RouteTable(object):
    def __init__(self,selectors,links,domains):
        
        self.selectors=selectors
        self.links=links
        self.domains=domains
        
    def to_string(self):
        head = "| app |" +" "*15 + "dest" + " "*15 + "|" + " "*15 + "peer" + " "*15 + "| priority \n"
        line_separator = "|" + "-"*len(head) + "|\n"
        
        str = "Route Table:  \n"
        str += line_separator + head + line_separator
                
        route_items=[]
        for selector in self.selectors.values():
            link = self.links[selector.peer]
            priority=1
            while True:
                if link.data != "<Empty>":
                    domain = self.domains[link.data]                
                    peer_str = domain.to_string()
                
                dest = self.domains[selector.destination]
                
                route_items.append([selector.application_id,dest.to_string(),
                                    peer_str, priority])
                priority +=1
                if link.next == "<Empty>": 
                    break 
                else:
                    link = self.links[link.next]
            
                
        
        for item in route_items:
            str += ("|%5s|%-34s|%-34s|%10d\n"
                %(TO_APP_NAME[item[0]],item[1],item[2],item[3]))
            str += line_separator
        
        return str


def run_command(command):
    p = subprocess.Popen(command,
                         shell=True,
                         stdout=subprocess.PIPE,
                         stderr=subprocess.STDOUT)
    return iter(p.stdout.readline, b'')

def load_selector():
    selectors={}
    command = "immfind | grep otpdiaSelector"
    for line in run_command(command):
        cmd = "immlist "+line
        
        text = run_command(cmd)
        s = Selector().parse(text)
        selectors[line.rstrip()]=s
        
    return selectors
        
def load_link():
    links={}
    command = "immfind | grep otpdiaCons"
    for line in run_command(command):
        cmd = "immlist "+line
        
        text = run_command(cmd)
        s = Link().parse(text)
        links[line.rstrip()]=s
        
    return links

def load_domain():
    domains={}
    command = "immfind | grep otpdiaDomain"
    for line in run_command(command):
        cmd = "immlist "+line
        
        text = run_command(cmd)
        s = Domain().parse(text)
        domains[line.rstrip()]=s
        
    return domains

def load_route_info_from_imm():
#     command = "immfind | grep 'otpdiaSelector\|otpdiaCons\|otpdiaDomain' | xargs -t -n1 immlist" 
    
    return load_selector(), load_link(), load_domain()
    
    

def create_route_table(selectors, link, domains):
    return RouteTable(selectors,link,domains)
    
    
def add_otpdia_domain(host, realm):
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
    
def rm_otpdia_domain(host, realm):
    rdn = "otpdiaDomain=con_to_domain_"+host+"_"+realm
    cmd_rm_domain = "immcfg -d "+rdn
    print cmd_rm_domain
    
    run_command(cmd_rm_domain)


def add_otpdia_con(host, realm):
    # cmd example:
    #     immcfg -c OtpdiaDomain otpdiaDomain=domain_hss3 -a realm=ericsson.se
    #     immcfg -a host=hss3 otpdiaDomain=domain_hss3  
    
    domain_rdn = "otpdiaDomain=domain_" + host+"_" + realm
    rdn =  "otpdiaCons=con_to_domain_" + host+"_" + realm
    
    cmd_create_otpdia_con = "immcfg -c OtpdiaCons %s -a head=%s" %(rdn, domain_rdn)
#     cmd_set_host = "immcfg -a host=%s %s" %(host,rdn)
    
    print cmd_create_otpdia_con
    run_command(cmd_create_otpdia_con)
    
def rm_otpdia_con(host, realm):
    rdn = "otpdiaDomain=con_to_domain_"+host+"_"+realm
    cmd_rm_con = "immcfg -d " + rdn
    print cmd_rm_con
    
    run_command(cmd_rm_domain)

def list():
    selectors, links, domains = load_route_info_from_imm()
    route_table = create_route_table(selectors,links,domains)
    print route_table.to_string()    

def add(args):
    if not args.host:
        host = 'wildcard'
    else:
        host = args.host
        
    if not args.realm:
        print "please give the realm value"
        return False
    
    add_otpdia_domain(host, args.realm)

def rm(args):
    if not args.host:
        host = 'wildcard'
    else:
        host = args.host
        
    if not args.realm:
        print "please give the realm value"
        return False
    
    rm_otpdia_domain(host, args.realm)

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("--cmd",  choices=('list', 'add', 'rm'))
    parser.add_argument("--host")
    parser.add_argument("--realm")
    args = parser.parse_args()

    if args.cmd == "list" :
        list()
    elif args.cmd == "add" :
        add(args)
    elif args.cmd == "rm":
        rm(args)
    else:
        parser.print_help()
    