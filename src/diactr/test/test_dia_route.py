#!/usr/bin/env python

import unittest

import sys
sys.path.append("..")

from dia_route_ctr import *
from mock import MagicMock

from datamama import DataMama
        
        
class TestRouteTable(unittest.TestCase):
    dm = DataMama()
         
    def test_hss_failover(self):
        print "\n test_list_rt_for_hss_failover"
        rt = self.dm.create_route_table_w_hss_failover()
          
        self.assertEqual(2, len(rt.records))
        self.assertEqual(1, len(rt.imm.selector_map.values()))
          
        s = rt.imm.selector_map.values()[0]
        self.assertEqual("otpdiaDomain=_hss.com", s.get("destination"))
                  
        print rt.to_string("TEXT")
          
    def test_list_rt_for_hss_loadsharing(self):
        print "\n test_list_rt_for_hss_loadsharing"
          
        rt = self.dm.create_route_table_w_hss_loadsharing()
          
        self.assertEqual(1, len(rt.records))
        self.assertEqual(1, len(rt.imm.selector_map.values()))
          
        s = rt.imm.selector_map.values()[0]
        self.assertEqual("otpdiaCons=hss1hss2_hss.com", s.get("peer"))
#         self.assertEqual(1, s.link_size)
                  
        print rt.to_string("TABLE")
          
                
    def test_rm_record_with_low_priority(self):
        print "\n test_rm_record_with_low_priority"
         
        cmd_list = ["immcfg -a tail= otpdiaCons=hss1_hss.com",
            "immcfg -d otpdiaCons=hss2_hss.com",
            "immcfg -d otpdiaDomain=hss2_hss.com"]
 
        rt = self.dm.create_route_table_w_hss_failover()
        
        real = rt.imm.immcfg
        real.execute = MagicMock()
        
        rt.rm(2)
 
        self.assertEqual(cmd_list, real.get_cmd_list())
        real.execute.assert_called_once()
       
    def test_rm_record_with_high_priority(self):
           
        print "\n test_rm_record_with_high_priority"
           
        cmd_list = ["immcfg -a peer=otpdiaCons=hss2_hss.com otpdiaSelector=hss.com",
                    "immcfg -d otpdiaCons=hss1_hss.com",
                    "immcfg -d otpdiaDomain=hss1_hss.com"]
 
        rt = self.dm.create_route_table_w_hss_failover()
        real = rt.imm.immcfg
        real.execute = MagicMock()
        
        rt.rm(1)
        print rt.to_string()
        self.assertEqual(cmd_list, real.get_cmd_list())
          
    def test_rm_linked_list(self):
        print "\n test_rm_linked_list"
         
        cmd_list = ["immcfg -d otpdiaSelector=hss.com",
            "immcfg -d otpdiaDomain=_hss.com",
            "immcfg -d otpdiaCons=hss1hss2_hss.com",
            "immcfg -d otpdiaDomain=hss1hss2_hss.com"]
 
        rt = self.dm.create_route_table_w_hss_loadsharing()
        real = rt.imm.immcfg
        real.execute = MagicMock()
        rt.rm(1)
 
        self.assertEqual(cmd_list, real.get_cmd_list()) 
      
    def test_add_one_linked_list(self):
          
        print "\n test_add_one_linked_list"
          
        imm = IMM()
        rt = RouteTable(imm)
        real = rt.imm.immcfg
        real.execute = MagicMock()
                 
        rt.add(['16777265',],  ([NULL_VALUE,], 'hss.com'), (['hss1'], 'hss.com'))
          
        cmd_list = ["immcfg -c OtpdiaDomain otpdiaDomain=peer_1.1 -a realm=hss.com",
                    "immcfg -a host+=hss1 otpdiaDomain=peer_1.1",
                    "immcfg -c OtpdiaDomain otpdiaDomain=dest_1.1 -a realm=hss.com",
                    "immcfg -c OtpdiaCons otpdiaCons=1.1 -a head=otpdiaDomain=peer_1.1",
                    'immcfg -c OtpdiaSelector otpdiaSelector=1 -a peer=otpdiaCons=1.1 -a  service="otpdiaService=epc_aaa,otpdiaProduct=IPWorksAAA"',
                    "immcfg -a applicationId+=16777265 otpdiaSelector=1",
                    "immcfg -a destination+=otpdiaDomain=dest_1.1 otpdiaSelector=1"
                    ]
          
        self.assertEqual(cmd_list, real.get_cmd_list())
          
         
    def test_add_link_node(self):
         
        print "\n test_add_link_node"
         
        imm = IMM()
        rt = RouteTable(imm)
        rt.add(['16777265',],  ([NULL_VALUE,], 'hss.com'), (['hss2'], 'hss.com'))
         
        real = rt.imm.immcfg
        real.execute = MagicMock()         
        cmd_list = [
        "immcfg -c OtpdiaDomain otpdiaDomain=peer_1.1 -a realm=hss.com",
        "immcfg -a host+=hss1 otpdiaDomain=peer_1.1",
        "immcfg -c OtpdiaCons otpdiaCons=1.1 -a head=otpdiaDomain=peer_1.1",
        "immcfg -a tail=otpdiaCons=1.1 otpdiaCons=1.1"
        ]
 
         
        rt.add(['16777265',],  ([NULL_VALUE,], 'hss.com'), (['hss1'], 'hss.com'))
         
        self.assertEqual(cmd_list,real.get_cmd_list())
         
         
    def test_append_record_with_multiple_hss(self):
           
        print '\n test_append_record_with_multiple_hss'
        
        cmd_list = [ 
        "immcfg -c OtpdiaDomain otpdiaDomain=peer_1.1 -a realm=hss.com",
        "immcfg -a host+=hss3 otpdiaDomain=peer_1.1",
        "immcfg -a host+=hss4 otpdiaDomain=peer_1.1",
        "immcfg -c OtpdiaDomain otpdiaDomain=dest_1.1 -a realm=gw.com",
        "immcfg -c OtpdiaCons otpdiaCons=1.1 -a head=otpdiaDomain=peer_1.1",
        'immcfg -c OtpdiaSelector otpdiaSelector=1 -a peer=otpdiaCons=1.1 -a  service="otpdiaService=epc_aaa,otpdiaProduct=IPWorksAAA"',
        "immcfg -a applicationId+=16777265 otpdiaSelector=1",
        "immcfg -a applicationId+=16777250 otpdiaSelector=1",
        "immcfg -a destination+=otpdiaDomain=dest_1.1 otpdiaSelector=1"
            
        ]
           
        rt = self.dm.create_route_table_w_hss_failover()
        real = rt.imm.immcfg
        real.execute = MagicMock()
           
        rt.add(['16777265','16777250'], ([NULL_VALUE,], 'gw.com'), (['hss3','hss4'], 'hss.com') )
        print rt.to_string(f="TEXT")
          
          
        self.assertEqual(cmd_list, real.get_cmd_list())
           
 
    def test_remove_host_of_peer(self):
         
        print "\n test_remove_host_of_peer"
        
        cmd_list = [
        "immcfg -a host=hss1 otpdiaDomain=hss1hss2_hss.com",
        "immcfg -a realm=hss.com otpdiaDomain=hss1hss2_hss.com"
        ]
         
        rt = self.dm.create_route_table_w_hss_loadsharing()
        real = rt.imm.immcfg
        real.execute = MagicMock()
         
        rt.modify(1, 'peer',  (['hss1'], 'hss.com'))
         
        self.assertEqual(1, len(rt.records))
        
        self.assertEqual(cmd_list, real.get_cmd_list())
         
         
    def test_add_host_of_peer(self):
         
        print "\n test_add_host_of_peer"
         
        rt = self.dm.create_route_table_w_hss_loadsharing()
        real = rt.imm.immcfg
        real.execute = MagicMock()
        
        rt.modify(1, 'peer',  (['hss1', 'hss2', 'hss3'], 'hss.com'))
         
         
        cmd_list = ["immcfg -a host=hss1 otpdiaDomain=hss1hss2_hss.com",
                    "immcfg -a host+=hss2 otpdiaDomain=hss1hss2_hss.com",
                    "immcfg -a host+=hss3 otpdiaDomain=hss1hss2_hss.com",
                    "immcfg -a realm=hss.com otpdiaDomain=hss1hss2_hss.com"]

        self.assertEqual(cmd_list, real.get_cmd_list())

if __name__ == "__main__":
    unittest.main()
    