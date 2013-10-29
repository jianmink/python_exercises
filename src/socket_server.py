#!/usr/bin/env python

from SocketServer import (TCPServer as TCP, StreamRequestHandler as SRH)


HOST = ''
PORT = 21567
ADDR = (HOST, PORT)

class MyRequestHandler (SRH):
    def handle(self):
        print '... connected from:', self.client_address
        while True:
            data=self.rfile.readline()
            if not data:
                break 
    #         print "rcv: %s" %(data)
            self. wfile.write('[] %s' %(data.strip()))

tcpServ = TCP(ADDR, MyRequestHandler)
print 'waiting for connnection...'

tcpServ.serve_forever()
    

