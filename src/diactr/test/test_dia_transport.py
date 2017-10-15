#!/usr/bin/env python

import sys
sys.path.append("../")
import unittest
from dia_transport_ctr import *

# IMMCFG_SLEEP_TIME = 0

class DataMama(object):
    def __init__(self):
        pass
    
    def create_otpdia_transport_object(self, tcpmode, local_ip, local_port, remote_object_name, host=":all"):
        
        if remote_object_name == NULL_VALUE:
            object_name = "listening"
            remote_rdn = NULL_VALUE
        else:
            object_name = "connect_to_" + remote_object_name
            remote_rdn =   "otpdiaHost="+remote_object_name
        
        class_name = "otpdiaTransport%s" %(tcpmode)
        rdn = (class_name + "=" +object_name)
        
        str_ = ("""
        Name                                               Type         Value(s)
        ========================================================================
        %s                                                 SA_STRING_T  %s
        address                                            SA_STRING_T  %s
        port                                               SA_STRING_T  %s
        connectTo                                          SA_NAME_T    %s           
        host                                               SA_STRING_T  %s  
        SaImmAttrImplementerName                           SA_STRING_T  C-diameter 
        SaImmAttrClassName                                 SA_STRING_T  %s
        SaImmAttrAdminOwnerName                            SA_STRING_T  <Empty>
        """  % (class_name, rdn, local_ip, local_port, remote_rdn, host, 'O'+class_name[1:])  
        )
        
        n = OtpdiaObject()
        n.parse(str_.split('\n'))
        
        return n
    
    def create_otpdia_host_object(self, object_name, ip, port ):
        str_ = ("""
        Name                                               Type         Value(s)
        ========================================================================
        otpdiaHost                                         SA_STRINIG_T otpdiaHost=%s
        address                                            SA_STRING_T  %s
        port                                               SA_STRING_T  %s 
        SaImmAttrImplementerName                           SA_STRING_T  C-diameter 
        SaImmAttrClassName                                 SA_STRING_T  OtpdiaHost
        SaImmAttrAdminOwnerName                            SA_STRING_T  <Empty>
        """  % (object_name, ip, port)  
        ) 
        
        n = OtpdiaObject()
        n.parse(str_.split('\n'))
        
        return n 
         
    
    def create_single_hss_tcp(self):
        t1 = self.create_otpdia_transport_object("Tcp", "192.168.20.13", "3868", NULL_VALUE, ":all")
        
        r = self.create_otpdia_host_object("hss1","192.168.20.1", "3869")
        t2 = self.create_otpdia_transport_object("Tcp", "192.168.20.13", "0", "hss1", ":all")
                  
        t_map = {t1.get("otpdiaTransportTcp"):t1, t2.get("otpdiaTransportTcp"):t2 }
        r_map = {r.get("otpdiaHost"):r}
         
        imm = IMM(t_map, r_map) 
        tl = TransportList(imm)
        return tl
    
    def create_single_hss_sctp(self):
        t1 = self.create_otpdia_transport_object("SctpE", "192.168.20.13", "3868", NULL_VALUE, ":all")
        
        r = self.create_otpdia_host_object("hss1","192.168.20.1", "3869")
        t2 = self.create_otpdia_transport_object("SctpE", "192.168.20.13", "0", "hss1", ":all")
                  
        t_map = {t1.get("otpdiaTransportSctpE"):t1, t2.get("otpdiaTransportSctpE"):t2 }
        r_map = {r.get("otpdiaHost"):r}
         
        imm = IMM(t_map, r_map) 
        tl = TransportList(imm)
        return tl
        
class TestConnection(unittest.TestCase):
    dm = DataMama()
          
    def test_single_hss_tcp(self):
        print "\n test_single_hss_tcp"
          
        tl = self.dm.create_single_hss_tcp()
          
        self.assertEqual(2, len(tl.records))
          
        print tl.to_string()
        print tl.to_string("TABLE")
        
    def test_single_hss_sctp(self):
        print "\n test_single_hss_sctp"
          
        tl = self.dm.create_single_hss_sctp()
          
        self.assertEqual(2, len(tl.records))
          
        print tl.to_string()
        print tl.to_string("TABLE")
          
    def test_rm_listening_transport(self):
        print "\n test_rm_listening_transport"
           
        cmd_list = [
            "immcfg -d otpdiaTransportTcp=listening,%s" %(SERVICE_DN)]
   
        tl = self.dm.create_single_hss_tcp()
        tl.rm(1)
   
        self.assertEqual(cmd_list, get_cmd_list())
 
    def test_rm_connect_to_hss1(self):
        print "\n test_rm_connect_to_hss1"
           
        cmd_list = ["immcfg -d otpdiaTransportTcp=connect_to_hss1,%s" %(SERVICE_DN),
            "immcfg -d otpdiaHost=hss1,%s" %(PRODUCT_DN)]
   
        tl = self.dm.create_single_hss_tcp()
        tl.rm(2)
   
        self.assertEqual(cmd_list, get_cmd_list())
      
           
    def test_add_listening_transport(self):
            
        print "\n test_add_listening_transport"
            
        imm = IMM()
        tl = TransportList(imm)
            
        tl.add("TCP",  local=('192.168.20.13', '3868'))
            
        cmd_list = [
        "immcfg -c OtpdiaTransportTcp otpdiaTransportTcp=listening,%s -a address=192.168.20.13 -a port=3868 -a host=:all" %(SERVICE_DN)
        ]
            
        print tl.to_string()
            
        self.assertEqual(cmd_list, get_cmd_list())
          
          
    def test_add_listening_sctp_transport(self):
            
        print "\n test_add_listening_transport"
            
        imm = IMM()
        tl = TransportList(imm)
            
        tl.add("SCTP", local=('192.168.20.13', '3868'))
            
        cmd_list = [
        "immcfg -c OtpdiaTransportSctpE otpdiaTransportSctpE=listening,%s -a address=192.168.20.13 -a port=3868 -a host=:all" %(SERVICE_DN)
        ]
            
        print tl.to_string()
            
        self.assertEqual(cmd_list, get_cmd_list())
 
 
    def test_add_connect_to_hss_transport(self):
            
        print "\n test_add_connect_to_hss_transport"
            
        imm = IMM()
        tl = TransportList(imm)
            
        tl.add("TCP",  local=('192.168.20.13', '0'), remote=('192.168.20.1', '3869'))
            
        cmd_list = [
        "immcfg -c OtpdiaHost otpdiaHost=192.168.20.1:3869,%s -a address=192.168.20.1 -a port=3869" %(PRODUCT_DN),
        "immcfg -c OtpdiaTransportTcp otpdiaTransportTcp=1,%s -a address=192.168.20.13 -a port=0 -a host=:all -a connectTo=otpdiaHost=192.168.20.1:3869" 
            %(SERVICE_DN)
        ]
            
        print tl.to_string()
        print get_cmd_list()
            
        self.assertEqual(cmd_list, get_cmd_list())  
         
     
    def test_add_connect_to_hss_transport_sctp(self):
            
        print "\n test_add_connect_to_hss_transport_sctp"
            
        imm = IMM()
        tl = TransportList(imm)
            
        tl.add("SCTP",  local=('192.168.20.13', '0'), remote=('192.168.20.1', '3869'))
            
        cmd_list = [
        "immcfg -c OtpdiaHost otpdiaHost=192.168.20.1:3869,%s -a address=192.168.20.1 -a port=3869" %(PRODUCT_DN),
        "immcfg -c OtpdiaTransportSctpE otpdiaTransportSctpE=1,%s -a address=192.168.20.13 -a port=0 -a host=:all -a connectTo=otpdiaHost=192.168.20.1:3869" 
            %(SERVICE_DN)
        ]
            
        print tl.to_string()
        print get_cmd_list()
            
        self.assertEqual(cmd_list, get_cmd_list())       
               
    
    def test_modify_transport(self):
             
        print "\n test_modify_local_ip"
            
        cmd_list = [
        "immcfg -a address=192.168.20.14 otpdiaTransportTcp=listening,%s" %(SERVICE_DN)
        ]
             
        tl = self.dm.create_single_hss_tcp()
             
        tl.modify(1, 'local',  ('192.168.20.14','3868'))
             
        print tl.to_string()
             
            
        self.assertEqual(cmd_list, get_cmd_list())
            



if __name__ == "__main__":
    unittest.main()
    