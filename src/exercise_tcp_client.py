#!/usr/bin/env python

from socket import *

import unittest

class TestRE(unittest.TestCase):
    def test_pass(self):
        self.assertTrue(True)
        

def tcp_client(port=12345):
    host='localhost'
#     port=12345
    print port
    addr=(host, port)
    cs=socket(AF_INET,SOCK_STREAM)
    cs.connect(addr)
    
    buffer_size=1024
    
    while True:
        data=raw_input('>')
        if not data:
            break
        print 'send: ',data
        cs.send('%s\r\n' %(data))
        response=cs.recv(buffer_size)
        print 'recv: ',response.strip()
    
    cs.close()
    
def udp_client():
    host='localhost'
    port=12350
    remote_addr=(host, port)
    
    cs=socket(AF_INET, SOCK_DGRAM)
    buffer_size=1024
    
    while True:
        data=raw_input('>')
        if not data:
            break
        print 'sendto: ', data, ' to ', remote_addr
        cs.sendto(data,remote_addr)
        response, remote  =cs.recvfrom(buffer_size)
        print "recvfrom: ", response, " from ", remote
    cs.close()

if __name__=='__main__':
    import sys
    if len(sys.argv)>1  and sys.argv[1]=='udp':
        udp_client()
    else:
        if len(sys.argv)>2:
            tcp_client(int(sys.argv[2]))
        else:
            tcp_client()
    