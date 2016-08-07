#!/usr/bin/env python

import unittest
from dia_connection_ctr import *

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
        connect_to                                         SA_NAME_T    %s           
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
        cl = TransportList(imm)
        return cl
    
    def create_single_hss_sctp(self):
        t1 = self.create_otpdia_transport_object("Esctp", "192.168.20.13", "3868", NULL_VALUE, ":all")
        
        r = self.create_otpdia_host_object("hss1","192.168.20.1", "3869")
        t2 = self.create_otpdia_transport_object("Esctp", "192.168.20.13", "0", "hss1", ":all")
                  
        t_map = {t1.get("otpdiaTransportEsctp"):t1, t2.get("otpdiaTransportEsctp"):t2 }
        r_map = {r.get("otpdiaHost"):r}
         
        imm = IMM(t_map, r_map) 
        cl = TransportList(imm)
        return cl
        
class TestConnection(unittest.TestCase):
    dm = DataMama()
          
    def test_single_hss_tcp(self):
        print "\n test_single_hss_tcp"
          
        cl = self.dm.create_single_hss_tcp()
          
        self.assertEqual(2, len(cl.records))
          
        print cl.to_string()
        print cl.to_string("TABLE")
        
    def test_single_hss_sctp(self):
        print "\n test_single_hss_sctp"
          
        cl = self.dm.create_single_hss_sctp()
          
        self.assertEqual(2, len(cl.records))
          
        print cl.to_string()
        print cl.to_string("TABLE")
          
    def test_rm_listening_transport(self):
        print "\n test_rm_listening_transport"
          
        cmd_list = [
            "immcfg -d otpdiaTransportTcp=listening"]
  
        cl = self.dm.create_single_hss_tcp()
        cl.rm(1)
  
        self.assertEqual(cmd_list, get_cmd_list())

    def test_rm_connect_to_hss1(self):
        print "\n test_rm_connect_to_hss1"
          
        cmd_list = ["immcfg -d otpdiaTransportTcp=connect_to_hss1",
            "immcfg -d otpdiaHost=hss1"]
  
        cl = self.dm.create_single_hss_tcp()
        cl.rm(2)
  
        self.assertEqual(cmd_list, get_cmd_list())
     
          
    def test_add_listening_transport(self):
          
        print "\n test_add_listening_transport"
          
        imm = IMM()
        cl = TransportList(imm)
          
        cl.add("TCP",  local=('192.168.20.13', '3868'))
          
        cmd_list = [
        "immcfg -c OtpdiaTransportTcp otpdiaTransportTcp=listening -a address=192.168.20.13 -a port=3868 -a host=:all -a service=%s" %(SERVICE_DN)
        ]
          
        print cl.to_string()
          
        self.assertEqual(cmd_list, get_cmd_list())
        
        
    def test_add_listening_sctp_transport(self):
          
        print "\n test_add_listening_transport"
          
        imm = IMM()
        cl = TransportList(imm)
          
        cl.add("SCTP", local=('192.168.20.13', '3868'))
          
        cmd_list = [
        "immcfg -c OtpdiaTransportEsctp otpdiaTransportEsctp=listening -a address=192.168.20.13 -a port=3868 -a host=:all -a service=%s" %(SERVICE_DN)
        ]
          
        print cl.to_string()
          
        self.assertEqual(cmd_list, get_cmd_list())


    def test_add_connect_to_hss_transport(self):
          
        print "\n test_add_connect_to_hss_transport"
          
        imm = IMM()
        cl = TransportList(imm)
          
        cl.add("TCP",  local=('192.168.20.13', '0'), remote=('192.168.20.1', '3869'))
          
        cmd_list = [
        "immcfg -c OtpdiaHost otpdiaHost=192.168.20.1:3869 -a address=192.168.20.1 -a port=3869",
        "immcfg -c OtpdiaTransportTcp otpdiaTransportTcp=1 -a address=192.168.20.13 -a port=0 -a host=:all -a connect_to=otpdiaHost=192.168.20.1:3869 -a service=%s" %(SERVICE_DN)
        ]
          
        print cl.to_string()
        print get_cmd_list()
          
        self.assertEqual(cmd_list, get_cmd_list())        
  
    def test_modify_transport(self):
           
        print "\n test_modify_local_ip"
          
        cmd_list = [
        "immcfg -a address=192.168.20.14 otpdiaTransportTcp=listening"
        ]
           
        cl = self.dm.create_single_hss_tcp()
           
        cl.modify(1, 'local',  ('192.168.20.14','3868'))
           
        print cl.to_string()
           
          
        self.assertEqual(cmd_list, get_cmd_list())
          



if __name__ == "__main__":
    unittest.main()
    