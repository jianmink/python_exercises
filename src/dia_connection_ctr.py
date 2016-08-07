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
# 1. 


# todo list
# list
# rm
# add
# modify


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
                    
    
    def add_otpdiatransport(self, transport):
        rdn = transport.rdn
        
        if transport.port == '0':
            cmd = 'immcfg -c OtpdiaTransportTcp %s -a address=%s -a port=%s -a host=%s' %(rdn, transport.ip, transport.port, transport.host)
            self.run_command(cmd)
        else:
            cmd =('immcfg -c OtpdiaTransportTcp %s -a address=%s -a port=%s -a host=%s -a connect_to=%s'
                 %(rdn, transport.ip, transport.port, transport.host, transport.remote.rdn))
            self.run_command(cmd)
            
    def add_otpdiahost(self, remote):
        rdn, ip, port = remote.rdn, remote.ip, remote.port
        cmd = "immcfg -c OtpdiaHost %s -a ip=%s -a port=%s" %(rdn, ip, port)
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



class Transport(object):
    def __init__(self, local_ip="", local_port="", remote=None, host=':all'):
        self.rdn = ""
        self.local_ip   = local_ip
        self.local_port = local_port
        self.connect_to = remote
        self.host = host
        
    def to_string(self):
        if self.local_port == '0': 
            return ("Listening %s(%s) at host %s" %(self.local_ip, self.local_port), self.host)
        else:
            return ("Connect from %s(%s) at host %s to remote %s" %(self.local_ip, 
                                                                    self.local_port, 
                                                                    self.host, 
                                                                    self.remote.to_string()))
            

class Remote(object):
    def __init__(self, rdn, ip, port):
        self.rdn = rdn
        self.ip   = ip
        self.port = port

    def to_string(self):        
        return ("%s(%s)" %(self.ip, self.port))

class IMM(object):
    def __init__(self, t_map=None, r_map=None):
        if t_map and r_map:
            self.transport_map=t_map
            self.remote_map=r_map
        else:
            self.transport_map = {}
            self.remote_map = {}
        
        self.immcfg = IMMCFG()
        
        self.transport_list={}
        
        self.build()
        
         
    def build(self):
        
        for k in self.transport_map.keys():
            otp_t = self.transport_map[k]
            
            t = Transport()
            t.rdn = otp_t.get("otpdiaTransportTcp")
            t.local_ip = otp_t.get("address")
            t.local_port = otp_t.get("port")
            
            connect_to = otp_t.get("connect_to")
            if connect_to != NULL_VALUE:
                t.connect_to = None
            else:
                otp_r = self.remote_map[connect_to]
                r = Remote(otp_r.get("otpdiaHost"), otp_r.get("address"), otp_r.get("port"))
                t.connect_to = r
            
            self.transport_list[t.rdn] = t
                
    def load_imm_object(self):
        self.transport_map=self.immcfg.load_imm_object("OtpdiaTransportTcp")
        self.remote_map = self.immcfg.load_imm_object("OtpdiaHost")
            
        self.build()
    
     
   
    def append_transport(self,transport, peer=None):
        
#         selector_id = selector.rdn.split('otpdiaSelector=')[1]
#         
#         # by default: append the new node to the end of linked list
#         
#         node_id = 0
#         while True:
#             peer_rdn = "otpdiaDomain=peer_%s.%d" %(selector_id, node_id+1)
#             if not self.domain_map.has_key(peer_rdn):
#                 break;
#             node_id += 1
#             
#         peer_obj = Domain(peer_rdn, peer[0], peer[1])
#          
#         link_rdn = "otpdiaCons=%s.%d" %(selector_id, node_id + 1)
#         link_node = LinkNode(link_rdn, peer_obj, None, selector)
#         
#         node = selector.link_head
#         while node:
#             if not node.next:
#                 node.next = link_node
#                 break
#             else:
#                 node = node.next
#         
#         
#         self.immcfg.add_otpdiadomain(link_node.data)
#         self.immcfg.add_otpdiacons(link_node)
        
        return None
    
    def modify_domain(self, rdn, hosts, realm):
        
        self.immcfg.modify_imm_object(rdn, 'host', hosts)
        self.immcfg.modify_imm_object(rdn, 'realm', realm)
                

    def rm_transport(self, link_node):
        pass
            
            
#             
#     def find_selector(self, apps, host_list, realm):
#         result=[]
#         for s in self.linked_lists.values():
#             
#             if not is_sub_list(apps, s.matcher.app_list):
#                 continue
# 
#             if realm != s.matcher.dest.realm: continue
#             
#             if not is_sub_list(host_list, s.matcher.dest.host_list): continue
#             
#             result.append(s)
#             
#         return result  
    
#     def get_selector_id(self):
#         result = []
#         for s in self.selector_map.values():
#             result.append(int(s.rdn[-1]))
#         
#         if not result:
#             return 1
#         else: 
#             return sorted(result)[-1] + 1
#             
                    
def is_sub_list(listA, listB):
    for each in listA: 
        if each not in listB: return False
        
    return True

class Connection(object):
    def __init__(self, record_id, transport):
        self.transport = transport
        self.record_id = record_id
                        
    def to_string(self):
        str_= ""
        str_ += "id:         " + str(self.record_id) + '\n'
        str_ += "local_ip:   " + self.transport.local_ip + "\n"
        str_ += "local_port: " + self.transport.local_port + '\n'
        str_ += "remote_ip:  " + self.transport.remote.ip + '\n'
        str_ += "remote_port:" + self.transport.remote.port +'\n'
        str_ += "\n"
        return str_
             
                

class ConnectionList(object):
    def __init__(self, imm):
        self.imm = imm
        
        self.records={}
        record_id = 0
        
        for rdn in self.imm.transport_list.keys():
            
            record_id += 1
            transport = self.imm.transport_list[rdn]

            c = Connection(record_id, transport)
            
            self.records[rdn] = c
                    
        self.last_record_id = record_id
    
          
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
        head = "| id |" +" "*10 +"local "+" "*10 + "|" + " "*10 + "remote" + " "*10 + "|\n"
        
        line_separator = "|" + "-"*len(head) + "|\n"
        
        str_ = "Connection List:  \n"
        str_ += line_separator + head + line_separator

        tmp = self.sort()
            
        for k in sorted(tmp.keys()):
            record = tmp[k]
            
            str_ += ("|%4d|%-26s|%-26s|%10s\n"
                        %(record.record_id, 
                        "",
                        "",
                        "TCP")
                    )
            
            str_ += line_separator
             
        return str_

    def to_text(self):
        line_separator = "" + "-"*32 + "\n"
        
        str_ = "Connection List Text:  \n"

        tmp = self.sort()
            
        for k in sorted(tmp.keys()):
            record = tmp[k]
            str_ += line_separator 
            str_ += record.to_string()
            str_ += "\n"
             
        return str_
                
    def rm(self, record_id):
        
        record = self.find_record(record_id)
        
        if record:
            self.imm.rm_transport(record.transport)
            
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
        
#         
#         if field == 'peer':
#             self.imm.modify_domain(record.link_node.data.rdn, value[0], value[1])
#         
#         else:
#             print "WARNING, todo modify %s" %(field) 
#             return      


#         self.imm.immcfg.execute()
    
        

def list_route_table(output_format):
    imm = IMM()
    imm.load_imm_object()
    cl = ConnectionList(imm)
    print cl.to_string(output_format)    

def add(args):
    
    imm = IMM()
    imm.load_imm_object()
#     route_table = RouteTable(imm)
#     
#     app = args.apps
#     if not app:
#         print "please provide apps, e.g. SWx"
#         return 
#     
#     appid = [TO_APP_ID[app],]
#     
#     dest = ast.literal_eval(args.dest)
#     peer = ast.literal_eval(args.peer)
#     
#     
#     if dest[0][0] == '*' or dest[0][0] == '':
#         dest[0][0] = NULL_VALUE
#     
#     print appid, dest, peer
#     
#     route_table.add(appid, dest, peer )

def modify(args):
    if not args.record:
        print "please provide the id of route record to be modified"
        print "use list cmd to print the route table"
        return 

#     imm = IMM()
#     imm.load_imm_object()
#     route_table = RouteTable(imm)
#     
#     peer = ast.literal_eval(args.peer)
#     print peer
#     
#     if args.peer:
#         route_table.modify(int(args.record), 'peer', peer)
    
                    
def rm(args):
    if not args.record:
        print "please provide the id of route record to be removed"
        print "use list cmd to print the route table"
        return 

    imm = IMM()
    imm.load_imm_object()
    cl = ConnectionList(imm)
    
    
    cl.rm(int(args.record))

if __name__ == "__main__":
        
    '''
    Example:
        python ./dia_route_ctr.py --cmd list
        python ./dia_route_ctr.py --cmd add --localip --localport --remoteip --remoteport  --tcpmode        
        python ./dia_route_ctr.py --cmd modify --record 1 
        python ./dia_route_ctr.py --cmd rm --record 1
    '''
    
    parser = argparse.ArgumentParser()
    parser.add_argument("--cmd",  choices=('list', 'add', 'rm', 'modify'))
    
    # for add cmd
    parser.add_argument("--localip", type=str)
    parser.add_argument("--localport", type=str)
    parser.add_argument("--remoteip", type=str)
    parser.add_argument("--remoteport", type=str)
    
    # for rm cmd
    parser.add_argument("--record")
    
    # for list cmd
    parser.add_argument("--format", default="TEXT")
    
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
    
