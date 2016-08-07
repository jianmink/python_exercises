#!/usr/bin/env python

import unittest
from dia_connection_ctr import *

# IMMCFG_SLEEP_TIME = 0

class DataMama(object):
    def __init__(self):
        pass
    
    def create_otpdia_transport_object(self, tcpmode="Tcp", local_ip, local_port, remote_object_name, host=":all"):
        
        if remote_object_name == NULL_VALUE:
            object_name = "listening"
        else:
            object_name = "connect_to_" + remote_object_name  
        
        
        str_ = ("""
        Name                                               Type         Value(s)
        ========================================================================
        otpdiaTransport%s                                  SA_STRING_T  %s
        address                                            SA_STRING_T  %s
        port                                               SA_STRING_T  %s 
        connect_to                                         SA_NAME_T    %s           
        host                                               SA_STRING_T  %s  
        SaImmAttrImplementerName                           SA_STRING_T  C-diameter 
        SaImmAttrClassName                                 SA_STRING_T  OtpdiaTransportTcp 
        SaImmAttrAdminOwnerName                            SA_STRING_T  <Empty>
        """  % (tcpmode, object_name, local_ip, local_port, remote_object_name, host)  
        ) 
        
        n = OtpdiaObject()
        n.parse(str_.split('\n'))
        
        return n
    
    def create_otpdia_host_object(self, object_name, ip, port ):
        str_ = ("""
        Name                                               Type         Value(s)
        ========================================================================
        otpdiaHost                                         SA_STRINIG_T %s
        address                                            SA_STRING_T  %s
        port                                               SA_STRING_T  %s 
        SaImmAttrImplementerName                           SA_STRING_T  C-diameter 
        SaImmAttrClassName                                 SA_STRING_T  OtpdiaHost 
        SaImmAttrAdminOwnerName                            SA_STRING_T  <Empty>
        """  % (object_name, ip, port)  
        ) 
        
        n = OtpdiaObject()
        n.parse(str_.split('\n'))
        
    
#     def create_peer_object(self, hosts, realm):
#         
#         if len(hosts) > 0:
#             rdn = "otpdiaDomain=%s_%s" %("".join(hosts), realm)
#             host = " ".join(hosts)
#         else:
#             rdn = "otpdiaDomain=_%s" %(realm)
#             host = "<Empty>"
#         
#         str_ =  ("""
#         immlist otpdiaDomain=domain_hss 
#         Name                                               Type         Value(s)
#         ========================================================================
#         realm                                              SA_STRING_T  %s 
#         otpdiaDomain                                       SA_STRING_T  %s 
#         host                                               SA_STRING_T  %s
#         SaImmAttrImplementerName                           SA_STRING_T  C-diameter 
#         SaImmAttrClassName                                 SA_STRING_T  OtpdiaDomain 
#         SaImmAttrAdminOwnerName                            SA_STRING_T  <Empty>
#         """ %( realm, rdn, host)
#         )
#         
#         d = OtpdiaObject()
#         d.parse(str_.split('\n'))
#         return d
#      
    
#     def create_listening_transport(self):
#         d1 = self.create_domain_object(("hss1",), "hss.com")
#         d2 = self.create_domain_object(("hss2",), "hss.com")
#         d = self.create_domain_object(() , "hss.com")
#         
#         link_node1 = self.create_link_object(d1, "otpdiaCons=hss2_hss.com")
#         link_node2 = self.create_link_object(d2)
#         
#         s = self.create_selector_object(d, link_node1)
#         
#         selector_map = {s.get("otpdiaSelector"):s}
#         node_map = {link_node1.get("otpdiaCons"):link_node1, link_node2.get("otpdiaCons"):link_node2}
#         domain_map = {d1.get("otpdiaDomain"):d1, d2.get("otpdiaDomain"):d2, d.get("otpdiaDomain"):d}
#         
#         imm = IMM(selector_map, node_map, domain_map) 
#         rt = RouteTable(imm)
#         
#         return rt
#     
#     def create_connect_to_transport(self):
#         
#         #host                                               SA_STRING_T  hss3 hss4 
#         d1 = self.create_domain_object(("hss1", "hss2"), "hss.com")
#         d = self.create_domain_object(() , "hss.com")
#         
#         link_node1 = self.create_link_object(d1)
#         
#         s = self.create_selector_object(d, link_node1)
#         
#         selector_map = {s.get("otpdiaSelector"):s}
#         node_map = {link_node1.get("otpdiaCons"):link_node1}
#         domain_map = {d1.get("otpdiaDomain"):d1, d.get("otpdiaDomain"):d}
#         
#         imm = IMM(selector_map, node_map, domain_map)
#         rt = RouteTable(imm)
#         
#         return rt
        
        
class TestConnection(unittest.TestCase):
    dm = DataMama()
          
    def test_list_connection(self):
        print "\n test_list_connection"
          
        rt = self.dm.create_route_table_w_hss_loadsharing()
          
        self.assertEqual(1, len(rt.records))
        self.assertEqual(1, len(rt.imm.selector_map.values()))
          
        s = rt.imm.selector_map.values()[0]
        self.assertEqual("otpdiaCons=hss1hss2_hss.com", s.get("peer"))
#         self.assertEqual(1, s.link_size)
                  
        print rt.to_string()
          
#     def test_rm_connection(self):
#         print "\n test_rm_record_with_low_priority"
#          
#         cmd_list = ["immcfg -a tail= otpdiaCons=hss1_hss.com",
#             "immcfg -d otpdiaCons=hss2_hss.com",
#             "immcfg -d otpdiaDomain=hss2_hss.com"]
#  
#         rt = self.dm.create_route_table_w_hss_failover()
#         rt.rm(2)
#  
#         self.assertEqual(1, len(rt.records))
#         self.assertEqual(cmd_list, get_cmd_list())
#     
#          
#     def test_add_connection(self):
#          
#         print "\n test_add_link_node"
#          
#         imm = IMM()
#         rt = RouteTable(imm)
#          
#         rt.add(['16777265',],  ([NULL_VALUE,], 'hss.com'), (['hss2'], 'hss.com'))
#          
#         cmd_list = [
#         "immcfg -c OtpdiaDomain otpdiaDomain=peer_1.1 -a realm=hss.com",
#         "immcfg -a host+=hss1 otpdiaDomain=peer_1.1",
#         "immcfg -c OtpdiaCons otpdiaCons=1.1 -a head=otpdiaDomain=peer_1.1",
#         "immcfg -a tail=otpdiaCons=1.1 otpdiaCons=1.1"
#         ]
#  
#          
#         rt.add(['16777265',],  ([NULL_VALUE,], 'hss.com'), (['hss1'], 'hss.com'))
#         print rt.to_string()
#          
#         self.assertEqual(cmd_list, get_cmd_list())
#          
#  
#     def test_modify_connection(self):
#          
#         print "\n test_remove_host_of_peer"
#         
#         cmd_list = [
#         "immcfg -a host=hss1 otpdiaDomain=hss1hss2_hss.com",
#         "immcfg -a realm=hss.com otpdiaDomain=hss1hss2_hss.com"
#         ]
#          
#         rt = self.dm.create_route_table_w_hss_loadsharing()
#          
#         rt.modify(1, 'peer',  (['hss1'], 'hss.com'))
#          
#         print rt.to_string()
#          
#         self.assertEqual(1, len(rt.records))
#         
#         self.assertEqual(cmd_list, get_cmd_list())
         



if __name__ == "__main__":
    unittest.main()
    