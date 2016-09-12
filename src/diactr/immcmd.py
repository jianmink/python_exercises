import subprocess
import time
# 
# 
# import sys
# 
# from tabulate import tabulate
from otpdia import OtpdiaObject, ATTRIBUTE_HAS_MULTI_VALUE
# 
# 
# 
# TO_APP_NAME = {
# '16777250':"STa",
# '16777265':"SWx",
# '16777272':"S6b",
# '16777264':"SWm",
# '16777217':"Sh",
# '99887766':"SWm+"
#                }
# 
# TO_APP_ID = {
# "STa":'16777250',
# "SWx":'16777265',
# "S6b": '16777272',
# "SWm": '16777264',
# "Sh":  '16777217',
# "SWm+": '99887766'
#                }

NULL_VALUE = "<Empty>"
WILDCARD_SYMBOL = "*"
IMMCFG_SLEEP_TIME = 0
LOWEST_PRI = 999


class IMMCFG():
    def __init__(self):
        self.SERVICE_DN="otpdiaService=epc_aaa,otpdiaProduct=IPWorksAAA"
        
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
        for cmd in self.immcfg_cmd_list:
            print cmd
            self.run_command_impl(cmd)
            
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
    
    def get_cmd_list(self):
        return self.immcfg_cmd_list

    
