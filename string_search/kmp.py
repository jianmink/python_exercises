import unittest
import logging as log 
logger = log.getLogger('root')
FORMAT = "[%(filename)s:%(lineno)3s - %(funcName)10s() ] %(message)s"
log.basicConfig(format=FORMAT, level=log.DEBUG)

def gen_kmp_prefix_table(p):
    table=[]
    # table[q] = max{k: k<q and Pk -] Pq}
    
    # table[0] = 0
    table.append(0)
    
    k=0
    for q in range(1,len(p)):
        
        # check if p[...:q] is any prefix of p 
        while k>0 and p[k]!=p[q]:
            k=table[k]
        
        # p[...:q+1] is a prefix of p    
        if p[k]==p[q]:
            k+=1
            
        # table[q]= k    
        table.append(k)
    return table

def kmp(s, p,table):
    
    # initial state is 0
    q=0
    
    # scan the text one by one
    for i in range(len(s)):
        
        # check edge s[i] in state q and all the ancestor 
        while q>0 and p[q]!=s[i]:
            q=table[q]
        
        # edge s[i] is right forward in state q    
        if p[q]==s[i]:
            q+=1
            
        # enter the accepted state
        if q==len(p):
            log.info("match s[%02d:%02d] := %s", i-len(p)+1, i, s[i-len(p)+1:i+1] )
            # enter initial state to start another match
            q=0
        

class TestKmp(unittest.TestCase):
    def test_prefix_table(self):
        p='ababaca'
        r=gen_kmp_prefix_table(p)
        e=[0,0,1,2,3,0,1]
        self.assertEqual(e, r)
    
    def test_kmp(self):
        p='ababaca'
        s='abcababacabbbababacaaa'
        t=gen_kmp_prefix_table(p)
        kmp(s,p,t)