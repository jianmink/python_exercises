#!/usr/bin/env python
import dpkt, pcap

def main():
    pc = pcap.pcap()
    pc.setfilter('icmp')
    for ts, pkt in pc:
        print `dpkt.ethernet.Ethernet(pkt)`


if __name__ == '__main__':
    main()

        
        
        
    
