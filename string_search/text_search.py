#!/usr/bin/env python
import unittest
import logging as log 
logger = log.getLogger('root')
FORMAT = "[%(filename)s:%(lineno)3s - %(funcName)10s() ] %(message)s"
log.basicConfig(format=FORMAT, level=log.DEBUG)

def force_search(s,p):
    log.info('search 1st "%s" from "%s"'%(p,s))
    i=0
    count=0

    while i+len(p)<=len(s): 
        j=0
        while j<len(p):
            count+=1           
            if s[i+j]==p[j]: j+=1
            else: break      
        if j==len(p):
            log.debug("perf: %d" %(count))
            return i
        
        i+=1
    
    log.debug("perf: %d"%(count))
    return -1

def is_equal(a,b):
    if len(a)!=len(b):
        return False
    
    for i in range(len(a)):
        if a[i]!=b[i]:
            return False
    
    return True

def generate_kmp_partial_match_tab(p):
    '''
        patrial match Table:
        "ab_ab_"
         012345
        Tab[5]=2, where p[:2]=p[3:5], Tab[5]= len(p[:2])
        
        patrial match help the substring search algorithm, 
        because it help to bypass the elements already compared.
        
        For example, 
            for substring start with index 'm', if P[5] != s[m+5], it needs to move 'm' forward.  
            As the partrial match table tell us, s[m+3:m+5]==p[:2], 
                so move 'm' 3 steps forward, and compare p[3] with s[m'] 
    '''   
    len_p=len(p)
    if len_p==1:
        return [-1]
    elif len_p==2:
        return [-1,0]
    
    Tab=[0 for _ in range(len(p))]
    Tab[0]=-1
    Tab[1]=0
        
    # i: table 
    # j: next candidate element in pattern   
    i=2
    j=0
    while i <len(p):
        if p[i-1] == p[j]:
            Tab[i]=Tab[i-1]+1
            i+=1
            j+=1
        elif j >0:
            j=Tab[j]
        else:
            Tab[i]=0
            i+=1
    print Tab
    return Tab     
  
def kmp_search(s,p):
    '''
        m: start of sub-string
        i: current index in pattern.
        O(n), <2n
    '''
    
    Tab=generate_kmp_partial_match_tab(p)
    log.info('search 1st "%s" from "%s"'%(p,s))
    m,i=0,0
    count=0

    while m + i <len(s) :
        log.debug("%s, %s",p[i:],s[m+i:])
        count+=1
        if s[m+i]==p[i]:
            if i == len(p)-1:
                log.debug("perf: %d" %(count))
                return m
            i+=1
        else:
            m+=i-Tab[i]
            if i>0:
                i=Tab[i]
            else:
                i=0
                    
    log.debug("X perf: %d"%(count))
    return -1
         
def force_search_w_wildcard(s,p):
    '''
    so dirty!!!
    '''
    log.info('search 1st "%s" from "%s"'%(p,s))
    i=0
    count=0
    while i+len(p)<=len(s):
#        ss=() 
        j=0
        ss=[]
        w=[]
        while j<len(p) and i+len(ss)<len(s):
            log.debug("%s,%s,%s i=%d,j=%d",s[i:],ss,w,i,j)
            count+=1 
            if p[j]=='*':
                w.append([i+len(ss),i+len(ss)])
                j+=1  
            else: 
                k= i+len(ss)        
                if s[k]==p[j]:
                    ss.append(p[j]) 
                    j+=1
                elif p[j-1]=='*':
                    ss.append(s[k])
                    index=len(w)-1
                    w[index][1]+=1
                elif len(w)>0:
                    #back track
                    # todo
                    index=len(w)-1
                    w[index][1]=k
                    
                else:
                    break                          
        
        if j==len(p):
            log.debug("perf: %d" %(count))
            log.info("substring: %s",ss)
            return i
        
        i+=1
    
    log.debug("fail- perf: %d"%(count))
    return -1               

class test_text_search(unittest.TestCase):
    def setUp(self):
        log.info("\n----------------------------\n")  
    
    @unittest.skip('')    
    def test_force_search(self):
        s="123_12_1234"
        p="1234"
        x=force_search(s,p)
        self.assertEqual(7, x)

#     @unittest.skip('')    
    def test_kmp_search(self):
        s="113_12_1134"
        p="1134"
        x=kmp_search(s,p)
        self.assertEqual(7,x)
    
    @unittest.skip('')    
    def test_kmp_patrial_match_table(self):
        
        p="1234123"
        tab=generate_kmp_partial_match_tab(p)
        print tab
        exp_tab=[-1,0,0,0,0,1,2]
        self.assertEqual(exp_tab,tab)
    
    @unittest.skip('')    
    def test_wild_card_search(self):
        s="cabccbacbacab"
        p="ab*ba*c"
#        s="cabbc"
#        p="ab*c"
        force_search_w_wildcard(s,p)
#        s="cabccbacbacab"
#        p="ab*ba*c"
#        force_search_w_wildcard(s,p)
                
    
if __name__ == '__main__':
    unittest.main()
