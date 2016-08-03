import subprocess
import time
import argparse
import copy
import ast

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
IMMCFG_SLEEP_TIME = 0
LOWEST_PRI = 999

# function list:
# 1. list route table
# 2. list route record in text mode
# 3. rm route record by record id
# 4. add new route record
# 5. modify peer info


# todo list
# validate
# support multiple value of otpdiaSelector.dest 
# support transaction for immcfg cmd, use "immcfg -f ./tmp/dia_route.xml" 
# support shell mode 
# 


ATTRIBUTE_HAS_MULTI_VALUE = ("host", "applicationId") #, "dest",  )

g_imm_cmd_list = None # For debugging

def get_cmd_list():
    global g_imm_cmd_list
    return g_imm_cmd_list

def set_cmd_list(cmd_list):
    global g_imm_cmd_list
    g_imm_cmd_list = copy.deepcopy(cmd_list)
    

class OtpdiaObject(object):
    def __init__(self):
        self.key_value_pairs={}
        pass
    
    def parse(self, text):
        for each in text:
            t = each.split()
            if len(t) < 3: continue
                
            k = t[0].rstrip()
            if k in ATTRIBUTE_HAS_MULTI_VALUE:
                value_list = [each.rstrip() for each in t[2:] if '(' not in each ]                
                self.key_value_pairs[k] = value_list
            else:
                v = t[2].rstrip()    
                self.key_value_pairs[k] = v
                
    def get(self, k):
        return self.key_value_pairs[k]
    

class IMMCFG():
    def __init__(self):
        self.SERVICE_DN="otpdiaService=epc_aaa,otpdiaProduct=AAAServer"
        
        self.immcfg_cmd_list=[]
        
    
    def rm_imm_object(self, rdn):
        self.run_command("immcfg -d " + rdn)
        
    def modify_imm_object(self,rdn,key, value):
        
        if key not in ATTRIBUTE_HAS_MULTI_VALUE:
            if not value or value == NULL_VALUE: value = ''
            self.run_command("immcfg -a %s=%s %s" %(key, value, rdn))
            
        else:
            if len(value) == 0:
                print "ERROR: empty list"
                return
            
            is_first_element = True
            for v in value:
                if v == NULL_VALUE: v = ''
                
                if is_first_element:
                    self.run_command("immcfg -a %s=%s %s" %(key, v, rdn))
                    is_first_element = False
                else:
                    self.run_command("immcfg -a %s+=%s %s" %(key, v, rdn))
                    
    
    def add_otpdiaselector(self, selector):
        rdn = selector.rdn
        cmd = 'immcfg -c OtpdiaSelector %s -a peer=%s -a  service="%s"' %(rdn, selector.link_head.rdn, self.SERVICE_DN )
        self.run_command(cmd)
        
        for each in selector.matcher.app_list:
            cmd = "immcfg -a applicationId+=%s %s" %(each,rdn)
            self.run_command(cmd)
            
        cmd = "immcfg -a destination+=%s %s" %(selector.matcher.dest.rdn,rdn)
        self.run_command(cmd)
        
        
    def add_otpdiacons(self, link_node, pre_link_obj=None, next_link_obj=None):
        
        if not next_link_obj: 
            cmd = "immcfg -c OtpdiaCons %s -a head=%s" %(link_node.rdn, link_node.data.rdn)
        else:
            cmd = "immcfg -c OtpdiaCons %s -a head=%s -a tail=%s" %(link_node.rdn, link_node.data, next_link_obj.rdn)
        
        self.run_command(cmd)
        
        if pre_link_obj: 
            cmd = "immcfg -a tail=%s %s" %(link_node.rdn,pre_link_obj.rdn)
            self.run_command(cmd)
            
    
    def add_otpdiadomain(self, domain):
        rdn, hosts, realm = domain.rdn, domain.host_list, domain.realm
        cmd = "immcfg -c OtpdiaDomain %s -a realm=%s" %(rdn, realm)
        self.run_command(cmd)
        
        for host in hosts:
            if host == NULL_VALUE or not host: 
                continue
            
            cmd = "immcfg -a host+=%s %s" %(host,rdn)
            self.run_command(cmd)
    
    def load_imm_object(self, class_name):
        # immfind and immlist command execute immediately
        dict_={}
        cmd = "immfind -c " + class_name 
        for line in self.run_command_impl(cmd):
            cmd = "immlist "+line
            text = self.run_command_impl(cmd)
            s = OtpdiaObject()
            s.parse(text)
            dict_[line.rstrip()]=s
        
        return dict_
    
    def execute(self):
        global g_imm_cmd_list
        for cmd in self.immcfg_cmd_list:
            print cmd
            self.run_command_impl(cmd)
            
        set_cmd_list(self.immcfg_cmd_list)  # save the cmd list for debugging only
        self.immcfg_cmd_list = []
        
            
    def run_command(self, cmd):
        self.immcfg_cmd_list.append(cmd)
    
    def run_command_impl(self, command, time_wait = IMMCFG_SLEEP_TIME, retry = 1):
        if time_wait != 0: time.sleep(time_wait)
            
        exit_code, output = self.run_command_(command)    
        while exit_code!=0 and retry > 0 :
            retry -= 1
            if output and "ERR_BAD_OPERATIONself" in ''.join(output):
                time.sleep(time_wait)
                exit_code,output = self.run_command_(command)
        
    #     if exit_code != 0:
    #         print "ERROR: exit program after fail to run " + command
    #         exit(1) 
            
        return output
                      
    def run_command_(self, command):
        p = subprocess.Popen(command,
                             shell=True,
                             stdout=subprocess.PIPE,
                             stderr=subprocess.STDOUT)
        
        rtn = ''
        while True:
            out = p.stdout.read(1)
            if out == '' and p.poll() != None:
                break
            if out != '':
                rtn += out
        
        if 'error' in rtn:
            print rtn
        
        return p.returncode, rtn.split('\n')[:-1]



class Selector(object):
    def __init__(self):
        self.rdn = ""
        self.matcher = None
        self.link_head = None

class Matcher(object):
    def __init__(self, app_list, dest):
        self.app_list = app_list
        self.dest = dest
                
class LinkNode(object):
    def __init__(self, rdn, data, next_, selector):
        self.rdn = rdn
        self.data = data
        self.next = next_
        self.selector = selector
        
    def get_priority(self):
        node = self.selector.link_head
        
        p = 1
        while node:
            if node.rdn == self.rdn:
                return p
            else:
                node = node.next
                p += 1   
        
        return 0
    
class Domain(object):
    def __init__(self, rdn, host_list, realm):
        self.rdn = rdn
        self.host_list = host_list
        self.realm = realm

    def to_string(self):        
        hosts, realm = self.host_list, self.realm
        if NULL_VALUE in hosts:   hosts = WILDCARD_SYMBOL
        if realm == NULL_VALUE:   realm = WILDCARD_SYMBOL

        return ("host = %s,  realm = %s" %(hosts, realm))

class IMM(object):
    def __init__(self, s_map=None, n_map=None, d_map=None):
        if s_map and n_map and d_map:
            self.selector_map=s_map
            self.node_map=n_map
            self.domain_map=d_map
        else:
            self.selector_map = {}
            self.node_map = {}
            self.domain_map = {}
        
        self.immcfg = IMMCFG()
        
        self.linked_lists = {}
        
        self.build_linked_list()
        
         
    def build_linked_list(self):
        for k in self.selector_map.keys():
            otp_s = self.selector_map[k]
            
            s = Selector()
            self.linked_lists[otp_s.get("otpdiaSelector")] = s
            s.rdn = otp_s.get("otpdiaSelector")
            
            otp_domain = self.domain_map[otp_s.get("destination")]
            d = Domain(otp_domain.get("otpdiaDomain"), otp_domain.get("host"), otp_domain.get("realm"))

            s.matcher = Matcher(otp_s.get("applicationId"), d)
            
            s.link_head=None
            
            node_rdn = otp_s.get("peer")
            is_head = True
            pre_node = None
            
            while self.node_map.has_key(node_rdn):
                otp_link = self.node_map[node_rdn]
                
                otp_domain = self.domain_map[otp_link.get("head")]
                d = Domain(otp_domain.get("otpdiaDomain"), otp_domain.get("host"), otp_domain.get("realm"))
                
                node = LinkNode(otp_link.get("otpdiaCons"), d, None, s)
                
                if is_head:
                    is_head = False
                    s.link_head = node
                else:
                    pre_node.next = node    
                    
                if otp_link.get("tail") == NULL_VALUE:
                    node.next = None
                else:
                    pre_node = node
                
                node_rdn = otp_link.get("tail")
                
    def load_imm_object(self):
        self.selector_map=self.immcfg.load_imm_object("OtpdiaSelector")
        self.node_map = self.immcfg.load_imm_object("OtpdiaCons")
        self.domain_map = self.immcfg.load_imm_object("OtpdiaDomain")
            
        self.build_linked_list()
    
     
    def sizeof_link(self, selector):
        count = 0
        node = selector.link_head
        while node:
            count += 1
            node = node.next
            
        return count
            
    
    def add_linked_list (self, app_list, dest, peer ):
        # assign id/name for new linked list 
        selector_id = 1
        rdn = "otpdiaSelector=%d" %(selector_id)
        while self.linked_lists.has_key(rdn):
            selector_id += 1
            rdn = "otpdiaSelector=%d" %(selector_id)
        
        s = Selector()
        s.rdn = rdn
        
        dest_rdn = "otpdiaDomain=dest_%d.%d" %(selector_id, 1)
        dest_domain = Domain(dest_rdn, dest[0], dest[1])
        
        peer_rdn = "otpdiaDomain=peer_%d.%d" %(selector_id, 1)
        peer_domain = Domain(peer_rdn, peer[0], peer[1])
        
         
        link_rdn = "otpdiaCons=%d.%d" %(selector_id, 1)
        link_node = LinkNode(link_rdn, peer_domain, None, s)

        s.link_head = link_node
        s.matcher = Matcher(app_list, dest_domain )
        
        self.immcfg.add_otpdiadomain(link_node.data)
        self.immcfg.add_otpdiadomain(s.matcher.dest)
        self.immcfg.add_otpdiacons(link_node)
        self.immcfg.add_otpdiaselector(s)
        
        self.linked_lists[s.rdn] = s
        
        return link_node
        
    
    def append_link_node(self,selector, peer):
        
        selector_id = selector.rdn.split('otpdiaSelector=')[1]
        
        # by default: append the new node to the end of linked list
        
        node_id = 0
        while True:
            peer_rdn = "otpdiaDomain=peer_%s.%d" %(selector_id, node_id+1)
            if not self.domain_map.has_key(peer_rdn):
                break;
            node_id += 1
            
        peer_obj = Domain(peer_rdn, peer[0], peer[1])
         
        link_rdn = "otpdiaCons=%s.%d" %(selector_id, node_id + 1)
        link_node = LinkNode(link_rdn, peer_obj, None, selector)
        
        node = selector.link_head
        while node:
            if not node.next:
                node.next = link_node
                break
            else:
                node = node.next
        
        
        self.immcfg.add_otpdiadomain(link_node.data)
        self.immcfg.add_otpdiacons(link_node)
        
        node = link_node.selector.link_head
        pre_node = node
        while node.next:
            pre_node = node
            node = node.next
                
        self.immcfg.modify_imm_object(pre_node.rdn, 'tail', link_node.rdn)
        
        return link_node
    
    def modify_domain(self, rdn, hosts, realm):
        
        self.immcfg.modify_imm_object(rdn, 'host', hosts)
        self.immcfg.modify_imm_object(rdn, 'realm', realm)
        
        
    def update_link_head(self, selector, link_node):
        selector.link_head = link_node
        self.immcfg.modify_imm_object(selector.rdn, "peer", link_node.rdn )
        
        
    def get_pre_link_node(self, link_node):
        prev_node = None
        
        node = link_node.selector.link_head
        while node:
            if node.next == link_node:
                prev_node = node 
                break
        
        return prev_node
        

    def rm_link_node(self, link_node):
        s = link_node.selector
        link_size = self.sizeof_link(s)
        
        if  link_size == 1:
            
            print "INFO: link size is one, so remove the selector"
            
            self.immcfg.rm_imm_object(s.rdn)
            self.immcfg.rm_imm_object(s.matcher.dest.rdn)
            self.immcfg.rm_imm_object(link_node.rdn)
            self.immcfg.rm_imm_object(link_node.data.rdn)
            
            
        elif s.link_head == link_node: # link head
            self.update_link_head(s, link_node.next)
            self.immcfg.rm_imm_object(link_node.rdn)               
            self.immcfg.rm_imm_object(link_node.data.rdn)
            
        else:
            pre_node = self.get_pre_link_node(link_node)
            pre_node.next = link_node.next 
        
            self.immcfg.modify_imm_object(pre_node.rdn, "tail", link_node.next)            
            self.immcfg.rm_imm_object(link_node.rdn)
            self.immcfg.rm_imm_object(link_node.data.rdn)
            
            
            
    def find_selector(self, apps, host_list, realm):
        result=[]
        for s in self.linked_lists.values():
            
            if not is_sub_list(apps, s.matcher.app_list):
                continue

            if realm != s.matcher.dest.realm: continue
            
            if not is_sub_list(host_list, s.matcher.dest.host_list): continue
            
            result.append(s)
            
        return result  
    
    def get_selector_id(self):
        result = []
        for s in self.selector_map.values():
            result.append(int(s.rdn[-1]))
        
        if not result:
            return 1
        else: 
            return sorted(result)[-1] + 1
            
                    
def is_sub_list(listA, listB):
    for each in listA: 
        if each not in listB: return False
        
    return True

class RouteRecord(object):
    '''
        Each route record can be mapped to one IMM OtpdiaCons object!!! 
        
        Additional information:
        1) record id
            The unique id for each record in the routing table
        2) priority
            It refers to the position in the linked list
    
    '''
    def __init__(self, record_id, link_node):
        self.link_node = link_node
        self.record_id = record_id
                        
    def to_string(self):
        m  = self.link_node.selector.matcher
        
        str_= ""
        str_ += "id:       " + str(self.record_id) + '\n'
        str_ += "app:      " + (' '.join([TO_APP_NAME[each] for each in m.app_list])) + "\n"
        str_ += "dest:     " + m.dest.to_string() + '\n'
        str_ += "peer:     " + self.link_node.data.to_string() + '\n'
        str_ += "priority: " + str(self.link_node.get_priority()) +'\n'
        str_ += "\n"
        return str_
             
                

class RouteTable(object):
    def __init__(self, imm):
        self.imm = imm
        
        self.records={}
        record_id = 0
        
        for rdn in self.imm.linked_lists.keys():
            
            linked_list = self.imm.linked_lists[rdn]
            
            link_node = linked_list.link_head 
            
            while link_node:
                
                record_id += 1
                record = RouteRecord(record_id,
                                     link_node)
                
                 
                k = self.hash(linked_list.matcher.app_list, 
                              linked_list.matcher.dest.host_list, linked_list.matcher.dest.realm,
                              link_node.data.host_list, link_node.data.realm)
                
                self.records[k] = record
                
                link_node = link_node.next 
                    
        self.last_record_id = record_id
    
    def hash(self, apps, dest_hosts, dest_realm, peer_host, peer_realm):
        k =  ''.join(apps)
        k += ''.join(dest_hosts)
        k += dest_realm
        k += ''.join(peer_host)
        k += peer_realm
        return k
        
          
    def to_string(self, f="TABLE"):
        if f == "TABLE":
            return self.to_table()
        else:
            return self.to_text()
        
    
    def sort(self):
        tmp = {}
        for record in self.records.values():
            # sort by record id
            tmp[record.record_id] = record
            
        return tmp
    
    
    def find_record(self, record_id):
        for record in self.records.values():
            if int(record.record_id) == record_id:
                return record
        return None    
    
    def to_table(self):
        head = "| id |  apps  |" +" "*20 + "dest" + " "*20 + "|" + " "*20 + "peer" + " "*20 + "| priority \n"
        
        line_separator = "|" + "-"*len(head) + "|\n"
        
        str_ = "Route Table:  \n"
        str_ += line_separator + head + line_separator

        tmp = self.sort()
            
        for k in sorted(tmp.keys()):
            record = tmp[k]
            
            m = record.link_node.selector.matcher
            
            str_ += ("|%4d|%8s|%-44s|%-44s|%10d\n"
                        %(record.record_id, ' '.join([TO_APP_NAME[each] for each in m.app_list]),
                        m.dest.to_string(),
                        record.link_node.data.to_string(),
                        record.link_node.get_priority())
                    )
            
            str_ += line_separator
             
        return str_

    def to_text(self):
        line_separator = "" + "-"*32 + "\n"
        
        str_ = "Route Table Text:  \n"

        tmp = self.sort()
            
        for k in sorted(tmp.keys()):
            record = tmp[k]
            str_ += line_separator 
            str_ += record.to_string()
            str_ += "\n"
             
        return str_
                
    def add(self, apps, dest, peer, priority=LOWEST_PRI):
        
        k = self.hash(apps, dest[0], dest[1], peer[0], peer[1])
        if self.records.has_key(k):
            print "ERROR: record already exist"
            return
        
        result = self.imm.find_selector(apps, dest[0], dest[1])
        
        if len(result) == 0:
            print "case 1: add new linked list"

            self.last_record_id +=1
            record_id = self.last_record_id
            
            node = self.imm.add_linked_list(apps, dest, peer)

            record = RouteRecord(record_id, node)
            self.records[k] = record
            
            
        elif len(result) == 1: 
            print "case 2: add link node into exist linked list"

            self.last_record_id +=1
            record_id = self.last_record_id
            
            selector = result[0]
            link_node = self.imm.append_link_node(selector, peer)
            
            record = RouteRecord(record_id, link_node)
            self.records[k] = record
            
            
        else:
            # case 3: to do 
            print "ERROR: more than one candidate linked list!!!"
            return 
            
            
        self.imm.immcfg.execute()
                   
    
    def rm(self, record_id):
        
        record = self.find_record(record_id)
        
        if record:
            self.imm.rm_link_node(record.link_node)
            
            for each in self.records.keys():
                if self.records[each] ==  record:
                    self.records.pop(each)
                    break
        else:
            print "ERROR: no record found with id " + str(record_id)
            return
            
        
        self.imm.immcfg.execute()
        

    def modify(self, record_id, field, value):
        
        record = self.find_record(record_id)
        
        if not record:
            print "ERROR: record not exit with record id as %d" %(record_id)
            return
        
        
        if field == 'peer':
            self.imm.modify_domain(record.link_node.rdn, value[0], value[1])
        
        else:
            print "WARNING, todo modify %s" %(field) 
            return      


        self.imm.immcfg.execute()
    
        

def list_route_table(output_format):
    imm = IMM()
    imm.load_imm_object()
    route_table = RouteTable(imm)
    print route_table.to_string(output_format)    

def add(args):
    
    imm = IMM()
    imm.load_imm_object()
    route_table = RouteTable(imm)
    
    app = args.apps
    if not app:
        print "please provide apps, e.g. SWx"
        return 
    
    appid = [TO_APP_ID[app],]
    
    dest = ast.literal_eval(args.dest)
    peer = ast.literal_eval(args.peer)
    
    
    if dest[0][0] == '*' or dest[0][0] == '':
        dest[0][0] = NULL_VALUE
    
    print appid, dest, peer
    
    route_table.add(appid, dest, peer )

def modify(args):
    if not args.record:
        print "please provide the id of route record to be modified"
        print "use list cmd to print the route table"
        return 

    imm = IMM()
    imm.load_imm_object()
    route_table = RouteTable(imm)
    
    peer = ast.literal_eval(args.peer)
    print peer
    
    if args.peer:
        route_table.modify(int(args.record), 'peer', peer)
    
                    
def rm(args):
    if not args.record:
        print "please provide the id of route record to be removed"
        print "use list cmd to print the route table"
        return 

    imm = IMM()
    imm.load_imm_object()
    route_table = RouteTable(imm)
    
    
    route_table.rm(int(args.record))

if __name__ == "__main__":
        
    '''
    Example:
        python ./dia_route_ctr.py --cmd list
        python ./dia_route_ctr.py --cmd add --apps 'SWx'  --dest "[['*'],'hss.com']" --peer "[['hss1'],'hss.com']"        
        python ./dia_route_ctr.py --cmd modify --record 1 --peer "[['hss1','hss2'],'hss.com']"
        python ./dia_route_ctr.py --cmd rm --record 1
    '''
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--cmd",  choices=('list', 'add', 'rm', 'modify'))
    
    # for add cmd
    parser.add_argument("--apps")
    parser.add_argument("--dest", type=str)
    parser.add_argument("--peer", type=str)
    
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
    elif args.cmd == 'modify':
        modify(args)
    else:
        parser.print_help()
    
