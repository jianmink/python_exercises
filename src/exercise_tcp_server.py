#!/usr/bin/env python

from socket import *

import unittest

class TestRE(unittest.TestCase):
    def test_pass(self):
        self.assertTrue(True)
        

def tcp_server():
    host=''
    port=12345
    addr=(host, port)
    ss=socket(AF_INET,SOCK_STREAM)
    ss.bind(addr)
    ss.listen(2)
    
    buffer_size=1024
    
    while True:
        print "waiting for connection..."
        conn,remote_addr=ss.accept()
        print "connection from ",  remote_addr, " by ", conn.getsockname()
        
        while True:
            data = conn.recv(buffer_size)
            if not data:
                conn.close()
                break;
            response= "[  ] %s" %(data)
            conn.send(response)
    
    ss.close()

def udp_server():
    host='localhost'
    port=12350
    addr=(host, port)
    ss=socket(AF_INET, SOCK_DGRAM)
    ss.bind(addr)
    buffer_size=1024
    while True:
        data,remote_addr=ss.recvfrom(buffer_size)
        ss.sendto('[]: %s' %(data), remote_addr)

if __name__=='__main__':
    import sys
    if len(sys.argv)>1 and sys.argv[1]=='udp':
        udp_server()
    else:    
        tcp_server()
    