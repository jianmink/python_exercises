#!/usr/bin/env python

import unittest

import sys

sys.path.append("..")

from dia_route_ctr import *

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
        """  % (next_link_rdn, ''.join(domain.get("host")), domain.get("realm"), domain.get("otpdiaDomain") )  
        ) 
        
        n = OtpdiaObject()
        n.parse(str_.split('\n'))
        
        return n
    
    def create_domain_object(self, hosts, realm):
        
        if len(hosts) > 0:
            rdn = "otpdiaDomain=%s_%s" %("".join(hosts), realm)
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
        
        d = OtpdiaObject()
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
        """ %(peer.get("otpdiaCons"), dest.get("realm"), dest.get("otpdiaDomain") )
        )
        
        s = OtpdiaObject()
        s.parse(str_.split('\n'))
        return s
    
    def create_route_table_w_hss_failover(self):
        d1 = self.create_domain_object(("hss1",), "hss.com")
        d2 = self.create_domain_object(("hss2",), "hss.com")
        d = self.create_domain_object(() , "hss.com")
        
        link_node1 = self.create_link_object(d1, "otpdiaCons=hss2_hss.com")
        link_node2 = self.create_link_object(d2)
        
        s = self.create_selector_object(d, link_node1)
        
        selector_map = {s.get("otpdiaSelector"):s}
        node_map = {link_node1.get("otpdiaCons"):link_node1, link_node2.get("otpdiaCons"):link_node2}
        domain_map = {d1.get("otpdiaDomain"):d1, d2.get("otpdiaDomain"):d2, d.get("otpdiaDomain"):d}
        
        imm = IMM(selector_map, node_map, domain_map) 
        rt = RouteTable(imm)
        
        return rt
    
    def create_route_table_w_hss_loadsharing(self):
        
        #host                                               SA_STRING_T  hss3 hss4 
        d1 = self.create_domain_object(("hss1", "hss2"), "hss.com")
        d = self.create_domain_object(() , "hss.com")
        
        link_node1 = self.create_link_object(d1)
        
        s = self.create_selector_object(d, link_node1)
        
        selector_map = {s.get("otpdiaSelector"):s}
        node_map = {link_node1.get("otpdiaCons"):link_node1}
        domain_map = {d1.get("otpdiaDomain"):d1, d.get("otpdiaDomain"):d}
        
        imm = IMM(selector_map, node_map, domain_map)
        rt = RouteTable(imm)
        
        return rt
        
    