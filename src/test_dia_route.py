#!/usr/bin/env python

import unittest
from dia_route_ctr import *



# IMMCFG_SLEEP_TIME = 0

'''
SC-1:~ # immlist -c OtpdiaDomain

<< OtpdiaDomain - CONFIG >>
realm : SA_STRING_T [1] {CONFIG, WRITEABLE, INITIALIZED}
otpdiaDomain : SA_STRING_T [1] {RDN, CONFIG, INITIALIZED}
host : SA_STRING_T [0..*] = Empty {CONFIG, WRITEABLE, MULTI_VALUE}
SC-1:~ # immlist -c OtpdiaCons  

<< OtpdiaCons - CONFIG >>
tail : SA_NAME_T [0] = Empty {CONFIG, WRITEABLE}
otpdiaCons : SA_STRING_T [1] {RDN, CONFIG, INITIALIZED}
head : SA_NAME_T [1] {CONFIG, WRITEABLE, INITIALIZED}
SC-1:~ # immlist -c OtpdiaSelector

<< OtpdiaSelector - CONFIG >>
service : SA_NAME_T [1..*] {CONFIG, WRITEABLE, INITIALIZED, MULTI_VALUE}
peer : SA_NAME_T [1] {CONFIG, WRITEABLE, INITIALIZED}
otpdiaSelector : SA_STRING_T [1] {RDN, CONFIG, INITIALIZED}
dest : SA_NAME_T [0..*] = Empty {CONFIG, WRITEABLE, MULTI_VALUE}
applicationId : SA_UINT32_T [0..*] = Empty {CONFIG, WRITEABLE, MULTI_VALUE}

'''

class DataMama(object):
    def __init__(self):
        pass
    
    def create_link_object(self, domain, next_link_rdn="<Empty>"):
        str_ = ("""
        immlist otpdiaCons=con_hss 
        Name                                               Type         Value(s)
        ========================================================================
        tail                                               SA_NAME_T    %s
        otpdiaCons                                         SA_STRING_T  otpdiaCons=%s_%s 
        head                                               SA_NAME_T    %s (23) 
        SaImmAttrImplementerName                           SA_STRING_T  C-diameter 
        SaImmAttrClassName                                 SA_STRING_T  OtpdiaCons 
        SaImmAttrAdminOwnerName                            SA_STRING_T  <Empty>
        """  % (next_link_rdn, ''.join(domain.hosts), domain.realm, domain.rdn )  
        ) 
        
        n = OtpdiaCons()
        n.parse(str_.split('\n'))
        
        return n
    
    def create_domain_object(self, hosts, realm):
        
        if len(hosts) > 0:
            rdn = "otpdiaDomain=%s_%s" %(",".join(hosts), realm)
            host = " ".join(hosts)
        else:
            rdn = "otpdiaDomain=_%s" %(realm)
            host = "<Empty>"
        
        str_ =  ("""
        immlist otpdiaDomain=domain_hss 
        Name                                               Type         Value(s)
        ========================================================================
        realm                                              SA_STRING_T  %s 
        otpdiaDomain                                       SA_STRING_T  %s 
        host                                               SA_STRING_T  %s
        SaImmAttrImplementerName                           SA_STRING_T  C-diameter 
        SaImmAttrClassName                                 SA_STRING_T  OtpdiaDomain 
        SaImmAttrAdminOwnerName                            SA_STRING_T  <Empty>
        """ %( realm, rdn, host)
        )
        
        d = OtpdiaDomain()
        d.parse(str_.split('\n'))
        return d
     
    def create_selector_object(self, dest, peer):
        str_ = ("""
         immlist otpdiaSelector=selector_1 
            Name                                               Type         Value(s)
            ========================================================================
            service                                            SA_NAME_T    otpdiaService=epc_aaa,otpdiaProduct=AAAServer (45) 
            peer                                               SA_NAME_T    %s (18) 
            otpdiaSelector                                     SA_STRING_T  otpdiaSelector=%s 
            destination                                        SA_NAME_T    %s (23) 
            applicationId                                      SA_UINT32_T  16777265 (0x1000031)
            SaImmAttrImplementerName                           SA_STRING_T  C-diameter 
            SaImmAttrClassName                                 SA_STRING_T  OtpdiaSelector 
            SaImmAttrAdminOwnerName                            SA_STRING_T  <Empty>
        """ %(peer.rdn, dest.realm, dest.rdn )
        )
        
        s = OtpdiaSelector()
        s.parse(str_.split('\n'))
        return s
    
    def create_route_table_w_hss_failover(self):
        d1 = self.create_domain_object(("hss1",), "hss.com")
        d2 = self.create_domain_object(("hss2",), "hss.com")
        d = self.create_domain_object(() , "hss.com")
        
        link_node1 = self.create_link_object(d1, "otpdiaCons=hss2_hss.com")
        link_node2 = self.create_link_object(d2)
        
        s = self.create_selector_object(d, link_node1)
        
        selector_map = {s.rdn:s}
        node_map = {link_node1.rdn:link_node1, link_node2.rdn:link_node2}
        domain_map = {d1.rdn:d1, d2.rdn:d2, d.rdn:d}
        
        imm = IMM(selector_map, node_map, domain_map) 
        rt = RouteTable(imm)
        
        return rt
    
    def create_route_table_w_hss_loadsharing(self):
        
        #host                                               SA_STRING_T  hss3 hss4 
        d1 = self.create_domain_object(("hss1", "hss2"), "hss.com")
        d = self.create_domain_object(() , "hss.com")
        
        link_node1 = self.create_link_object(d1)
        
        s = self.create_selector_object(d, link_node1)
        
        selector_map = {s.rdn:s}
        node_map = {link_node1.rdn:link_node1}
        domain_map = {d1.rdn:d1, d.rdn:d}
        
        imm = IMM(selector_map, node_map, domain_map)
        rt = RouteTable(imm)
        
        return rt
        
        
class TestRouteTable(unittest.TestCase):
    dm = DataMama()
        
    def test_hss_failover(self):
        print "\n test_list_rt_for_hss_failover"
        rt = self.dm.create_route_table_w_hss_failover()
         
        self.assertEqual(2, len(rt.records))
        self.assertEqual(1, len(rt.imm.selector_map.values()))
         
        s = rt.imm.selector_map.values()[0]
        self.assertEqual("otpdiaDomain=_hss.com", s.dest_rdn)
        self.assertEqual(2, s.link_size)
                 
        print rt.to_string("TEXT")
         
    def test_list_rt_for_hss_loadsharing(self):
        print "\n test_list_rt_for_hss_loadsharing"
         
        rt = self.dm.create_route_table_w_hss_loadsharing()
         
        self.assertEqual(1, len(rt.records))
        self.assertEqual(1, len(rt.imm.selector_map.values()))
         
        s = rt.imm.selector_map.values()[0]
        self.assertEqual("otpdiaCons=hss1hss2_hss.com", s.link_head_rdn)
        self.assertEqual(1, s.link_size)
                 
        print rt.to_string()
         
               
    def test_rm_record_with_low_priority(self):
        print "\n test_rm_record_with_low_priority"
         
        rt = self.dm.create_route_table_w_hss_failover()
          
        rt.rm(2)
         
        self.assertEqual(1, len(rt.records))
         
        self.assertEqual(2, len(rt.imm.domain_map))
        self.assertEqual(1, len(rt.imm.node_map))
        self.assertEqual(1, len(rt.imm.selector_map))
           
        s = rt.imm.selector_map.values()[0]
          
        n = rt.imm.node_map.values()[0]
          
        self.assertEqual(n.next, NULL_VALUE)
        self.assertEqual(n.data, 'otpdiaDomain=hss1_hss.com')
        self.assertEqual(s.link_head_rdn, 'otpdiaCons=hss1_hss.com')
        
      
    def test_rm_record_with_high_priority(self):
          
        print "\n test_rm_record_with_high_priority"
          
        rt = self.dm.create_route_table_w_hss_failover()
          
        rt.rm(1)
        print rt.to_string()
          
        self.assertEqual(2, len(rt.imm.domain_map))
        self.assertEqual(1, len(rt.imm.node_map))
        self.assertEqual(1, len(rt.imm.selector_map))
         
          
        print rt.imm.selector_map.values()[0].to_string()
          
        self.assertEqual(rt.imm.node_map.values()[0].next, NULL_VALUE)
        self.assertEqual(rt.imm.node_map.values()[0].data, 'otpdiaDomain=hss2_hss.com')
        self.assertEqual(rt.imm.selector_map.values()[0].link_head_rdn, 'otpdiaCons=hss2_hss.com')
         
        cmd_list = ["immcfg -a peer=otpdiaCons=hss2_hss.com otpdiaSelector=hss.com",
                    "immcfg -d otpdiaCons=hss1_hss.com",
                    "immcfg -d otpdiaDomain=hss1_hss.com"]
        
        self.assertEqual(cmd_list, rt.imm.immcfg.immcfg_cmd_list)
         
    def test_rm_all_records(self):
        
        print "\n test_rm_all_records"
        
        rt = self.dm.create_route_table_w_hss_failover()
          
        rt.rm(1)
        rt.rm(2)
         
        self.assertEqual(0, len(rt.records))
         
    def test_rm_all_records_in_reverse_order(self):
        print "\n test_rm_all_records_in_reverse_order"
        rt = self.dm.create_route_table_w_hss_failover()
          
        rt.rm(2)
        rt.rm(1)
         
        self.assertEqual(0, len(rt.records))
         
     
    def test_rt_size_1_after_add_record(self):
        
        print "\ntest_rt_size_1_after_add_record"
        
        imm = IMM()
        rt = RouteTable(imm)
         
        rt.add(['16777265',],  ([NULL_VALUE,], 'hss.com'), (['hss1'], 'hss.com'))
        tmp = rt.sort()
        
        self.assertEqual(1, len(rt.records))
        self.assertEqual(['16777265',],tmp[1].apps)
        self.assertEqual(1,tmp[1].priority)
        self.assertTrue("otpdiaCons" in tmp[1].link_rdn)
        
        print rt.to_string()
         
        
    def test_rt_size_1_after_add_two_records(self):
        
        print "\n test_rt_size_1_after_add_two_records"
        
        imm = IMM()
        rt = RouteTable(imm)
        
        rt.add(['16777265',],  ([NULL_VALUE,], 'hss.com'), (['hss1'], 'hss.com'))
        rt.add(['16777265',],  ([NULL_VALUE,], 'hss.com'), (['hss2'], 'hss.com'))
        
        print rt.to_string()
        
        self.assertEqual(2, len(rt.records))
        self.assertEqual(1, len(rt.imm.selector_map))
        
        
    def test_rt_size_3_after_add_record(self):
          
        print 'test_rt_size_3_after_add_record'
          
        rt = self.dm.create_route_table_w_hss_failover()
          
        rt.add(['16777265','16777250'], ([NULL_VALUE,], 'gw.com'), (['hss3','hss4'], 'hss.com') )
        print rt.to_string(f="TEXT")
         
         
        self.assertEqual(3, len(rt.records))
          
        self.assertEqual(5, len(rt.imm.domain_map))
        self.assertEqual(3, len(rt.imm.node_map))
        self.assertEqual(2, len(rt.imm.selector_map))
          

    def test_rt_size_1_after_add_hss_to_loadsharing_group(self):
           
        print 'test_rt_size_3_after_add_hss_to_loadsharing_group'
           
        rt = self.dm.create_route_table_w_hss_loadsharing()
           
        rt.add(['16777265',], ([NULL_VALUE,], 'hss.com'), (['hss3'], 'hss.com') )
        print rt.to_string(f="TEXT")
         
        self.assertEqual(2, len(rt.records))
           
        self.assertEqual(3, len(rt.imm.domain_map))
        self.assertEqual(2, len(rt.imm.node_map))
        self.assertEqual(1, len(rt.imm.selector_map))

    def test_remove_host_from_peer(self):
        
        print "\ntest_modify_host_of_peer"
        
        rt = self.dm.create_route_table_w_hss_loadsharing()
        r = rt.find_record(1)
        
        rt.modify(1, 'peer',  (['hss1'], 'hss.com'))
        
        print rt.to_string()
        
        self.assertEqual(1, len(rt.records))
        
        self.assertEqual(['hss1'], r.peer_obj.hosts)
        
    def test_add_host_from_peer(self):
        
        print "\ntest_modify_host_of_peer"
        
        rt = self.dm.create_route_table_w_hss_loadsharing()
        r = rt.find_record(1)
        
        rt.modify(1, 'peer',  (['hss1', 'hss2', 'hss3'], 'hss.com'))
        
        print rt.to_string()
        
        self.assertEqual(1, len(rt.records))
        
        self.assertEqual(['hss1', 'hss2', 'hss3'], r.peer_obj.hosts)
        
        

if __name__ == "__main__":
    unittest.main()
    