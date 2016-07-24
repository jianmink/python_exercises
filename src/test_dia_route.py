#!/usr/bin/env python

import unittest
from dia_route_ctr import *


class DataMama(object):
    def __init__(self):
        pass
    
    def get_one_selector(self):
        return  """
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

    def get_one_domain(self):
        return """
        immlist otpdiaDomain=domain_hss 
        Name                                               Type         Value(s)
        ========================================================================
        realm                                              SA_STRING_T  hss.com 
        otpdiaDomain                                       SA_STRING_T  otpdiaDomain=domain_hss 
        host                                               SA_STRING_T  hss1
        SaImmAttrImplementerName                           SA_STRING_T  C-diameter 
        SaImmAttrClassName                                 SA_STRING_T  OtpdiaDomain 
        SaImmAttrAdminOwnerName                            SA_STRING_T  <Empty>
        """
    
    def get_one_link_node(self):
        return """
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

    def create_route_table_with_one_record(self):
        s = Selector()
        s.parse(self.get_one_selector().split('\n'))
        
        n = Link()
        n.parse(self.get_one_link_node().split('\n'))
        
        d = Domain()
        d.parse(self.get_one_domain().split('\n'))
        
        imm = IMMDB() 
        imm.selectors = {s.rdn:s}
        imm.links = {n.rdn:n}
        imm.domains = {d.rdn:d}
        rt = RouteTable(imm)
        
        return rt
        
        

class TestLoadImmInfo(unittest.TestCase):
    dm = DataMama()
    
    def test_load_one_selector(self):
        s = Selector()
        s.parse(self.dm.get_one_selector().split('\n'))
        print s.to_string()
        self.assertEqual('16777265',s.application_id)
        self.assertEqual('otpdiaCons=con_hss', s.peer)
        self.assertEqual('otpdiaDomain=domain_hss', s.destination)
        self.assertEqual('otpdiaSelector=selector_1', s.rdn)
        
    
    def test_load_one_link_node(self):
        n = Link()
        n.parse(self.dm.get_one_link_node().split('\n'))
        self.assertEqual('<Empty>', n.next)
        self.assertEqual('otpdiaDomain=domain_hss', n.data)
        
    def test_load_one_domain(self):
        d = Domain()
        d.parse(self.dm.get_one_domain().split('\n'))
        self.assertEqual('hss1', d.host)
        self.assertEqual('hss.com', d.realm)
    
        
class TestRouteTable(unittest.TestCase):
    dm = DataMama()
    
    def test_list_route_table(self):
        rt = self.dm.create_route_table_with_one_record()
        print rt.to_string()
        
    def test_rm_one_record(self):
        rt = self.dm.create_route_table_with_one_record()
        rt.rm("16777265", ("hss1", "hss.com"), ("hss1", "hss.com"))
        print rt.to_string()
        
        
             
        
        