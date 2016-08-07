import subprocess
import time
import argparse
import copy
import ast


NULL_VALUE = "<Empty>"
WILDCARD_SYMBOL = "*"
IMMCFG_SLEEP_TIME = 0
LOWEST_PRI = 999

SERVICE_DN="otpdiaService=epc_aaa,otpdiaProduct=IPWorksAAA"


# todo list
# support multi-homing

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
    
    def add_otpdia_host(self, remote):
        cmd = ('immcfg -c OtpdiaHost %s -a address=%s -a port=%s' 
               %(remote.rdn, remote.ip, remote.port))
        
        self.run_command(cmd)              
    
    def add_otpdia_transport_tcp(self, transport):
        rdn = transport.rdn
         
        if not transport.remote:
            cmd = ('immcfg -c OtpdiaTransportTcp %s -a address=%s -a port=%s -a host=%s -a service=%s' 
                  %(rdn, transport.local_ip, transport.local_port, transport.host, SERVICE_DN))
            
            self.run_command(cmd)
        else:
            cmd =('immcfg -c OtpdiaTransportTcp %s -a address=%s -a port=%s -a host=%s -a connect_to=%s -a service=%s'
                 %(rdn, transport.local_ip, transport.local_port, transport.host, transport.remote.rdn, SERVICE_DN))
            self.run_command(cmd)

    def add_otpdia_transport_sctp(self, transport):
        rdn = transport.rdn
         
        if not transport.remote:
            cmd = ('immcfg -c OtpdiaTransportEsctp %s -a address=%s -a port=%s -a host=%s -a service=%s' 
                  %(rdn, transport.local_ip, transport.local_port, transport.host, SERVICE_DN))
            
            self.run_command(cmd)
        else:
            cmd =('immcfg -c OtpdiaTransportEsctp %s -a address=%s -a port=%s -a host=%s -a connect_to=%s -a service=%s'
                 %(rdn, transport.local_ip, transport.local_port, transport.host, transport.remote.rdn, SERVICE_DN))
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
    def __init__(self, rdn="", local_ip="", local_port="", remote=None, mode='TCP' , host=':all'):
        self.rdn = rdn
        self.local_ip   = local_ip
        self.local_port = local_port
        self.remote = remote
        self.host = host
        self.mode = mode
        
    def to_string(self):
        if self.local_port != '0': 
            return ("Listening %s(%s) \nhost = %s \nmode = %s" %(self.local_ip, self.local_port, self.host, self.mode))
        else:
            return ("Connect from %s(%s) to remote %s \nhost = %s \nmode = %s" %(self.local_ip, 
                                                                    self.local_port, 
                                                                    self.remote.to_string(),
                                                                    self.host,
                                                                    self.mode))

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
            
            if otp_t.get("SaImmAttrClassName") == "OtpdiaTransportTcp":
                t.mode = "TCP"
                t.rdn = otp_t.get("otpdiaTransportTcp") 
            else:
                t.mode = "SCTP"
                t.rdn = otp_t.get("otpdiaTransportEsctp")
            
                
            t.local_ip = otp_t.get("address")
            t.local_port = otp_t.get("port")
            
            remote_rdn = otp_t.get("connect_to")
            if remote_rdn == NULL_VALUE:
                t.remote = None
            else:
                otp_r = self.remote_map[remote_rdn]
                r = Remote(otp_r.get("otpdiaHost"), otp_r.get("address"), otp_r.get("port"))
                t.remote = r
            
            self.transport_list[t.rdn] = t
            
    def load_imm_object(self):
        self.transport_map=self.immcfg.load_imm_object("OtpdiaTransportTcp")
        self.remote_map = self.immcfg.load_imm_object("OtpdiaHost")
            
        self.build()
    
     
    def add_tcp_transport(self, transport):
        
        if self.transport_list.has_key(transport.rdn):
            print "ERROR: cannot create second listening transportTcp"
            return
        
        if transport.remote:
            self.immcfg.add_otpdia_host(transport.remote)
            
        self.immcfg.add_otpdia_transport_tcp(transport)
    
    def add_sctp_transport(self, transport):
        if self.transport_list.has_key(transport.rdn):
            print "ERROR: cannot create second listening transportEsctp"
            return
        
        if transport.remote: 
            self.immcfg.add_otpdia_host(transport.remote) 
        
        self.immcfg.add_otpdia_transport_sctp(transport)
        
    
    def modify_transport(self, transport, ip, port):
        
        if transport.local_ip != ip:
            self.immcfg.modify_imm_object(transport.rdn, 'address', ip)
        
        if transport.local_port != port:
            self.immcfg.modify_imm_object(transport.rdn, 'port', port)
                

    def rm_transport(self, transport):
        self.immcfg.rm_imm_object(transport.rdn)
        
        self.rm_remote(transport.remote)
    
    def rm_remote(self, remote):
        if not remote:
            return 
        
        # rm remote if no more transport refer to it
        count = 0
        for each in self.transport_list.values():
            if each.remote == remote:
                count +=1
                
        if count == 1:
            self.immcfg.rm_imm_object(remote.rdn)
            
    def allocate_transport_rdn(self, mode):
        i = 0
        while True:
            i += 1
            if mode == "TCP":
                rdn = "otpdiaTransportTcp=%d" %(i)
            else:
                rdn = "otpdiaTransportEsctp=%d" %(i)
                         
            if not self.transport_list.has_key(rdn):
                return rdn
                    
def is_sub_list(listA, listB):
    for each in listA: 
        if each not in listB: return False
        
    return True

class Record(object):
    def __init__(self, record_id, transport):
        self.transport = transport
        self.record_id = record_id
                        
    def to_string(self):
        str_= ""
        str_ += "id:         " + str(self.record_id) + '\n'
        str_ += self.transport.to_string() +'\n'
        str_ += "\n"
        return str_
             
                

class TransportList(object):
    def __init__(self, imm):
        self.imm = imm
        
        self.records={}
        record_id = 0
        
        for rdn in self.imm.transport_list.keys():
            
            record_id += 1
            transport = self.imm.transport_list[rdn]

            c = Record(record_id, transport)
            
            self.records[rdn] = c
                    
        self.last_record_id = record_id
    
          
    def to_string(self, f="TEXT"):
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
        head = "| id |" +" "*10 +"local "+" "*10 + "|" + " "*10 + "remote" + " "*10 + "|   mode  " + "\n"
        
        line_separator = "|" + "-"*len(head) + "|\n"
        
        str_ = "Transport List:  \n"
        str_ += line_separator + head + line_separator

        tmp = self.sort()
            
        for k in sorted(tmp.keys()):
            record = tmp[k]
            
            t = record.transport
            r = t.remote
            
            local_str = "%s(%s)" %(t.local_ip, t.local_port)
            
            if r == None:
                remote_str = ""
            else:
                remote_str = "%s(%s)" %(r.ip, r.port)
            
            str_ += ("|%-4d|  %-24s|  %-24s|%8s\n"
                        %(record.record_id, 
                        local_str,
                        remote_str,
                        t.mode)
                    )
            
            str_ += line_separator
             
        return str_

    def to_text(self):
        line_separator = "" + "-"*32 + "\n"
        
        str_ = "Transport List:  \n"

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
        
         
        if field == 'local':
            local_ip = value[0]
            local_port = value[1]
            self.imm.modify_transport(record.transport,local_ip, local_port)
         
        else:
            print "WARNING, todo modify %s" %(field) 
            return      


        self.imm.immcfg.execute()
    
    def add(self, mode, local, remote=None):
        
        if remote:
            rdn = "otpdiaHost=" +":".join(remote)
            r = Remote(rdn,remote[0], remote[1])
        
        if mode == "TCP":
            class_name = "otpdiaTransportTcp"
            func = self.imm.add_tcp_transport
        elif mode == "SCTP":
            class_name = "otpdiaTransportEsctp"
            func = self.imm.add_sctp_transport
        else:
            print "ERROR: unknown mode " + mode
            return 
        
        if not remote:
            print local, remote
            # listening transport is unique
            t = Transport("%s=listening" %(class_name), 
                          local[0], local[1] )
            func(t)
            
        else:
            rdn = self.imm.allocate_transport_rdn(mode)
            t = Transport(rdn, local_ip=local[0], local_port=local[1], remote=r, mode=mode)
            func(t)

            
        self.imm.immcfg.execute()
            

def list_route_table(output_format):
    imm = IMM()
    imm.load_imm_object()
    cl = TransportList(imm)
    print cl.to_string(output_format)    

def add(args):
    
    imm = IMM()
    imm.load_imm_object()


def modify(args):
    if not args.record:
        print "please provide the id of route record to be modified"
        print "use list cmd to print the route table"
        return 
 
                    
def rm(args):
    if not args.record:
        print "please provide the id of route record to be removed"
        print "use list cmd to print the route table"
        return 

    imm = IMM()
    imm.load_imm_object()
    cl = TransportList(imm)
    
    
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
    
