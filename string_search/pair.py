
import unittest

#precondition: list is in order 

def find_pair(s,a):
    r=[]
    i=0 
    j=len(s)-1
    while i < j:
        if s[i]+s[j]==a:
            r.append((s[i],s[j]))
            
            k=1
            while s[i+k]==s[i] and i+k<=j: k+=1
            i+=k
            
            k=1
            while s[j-k]==s[j] and j-k>=i: k+=1 
            j-=1
            
        elif s[i]+s[j]<a:
            i+=1
        else:
            j-=1
                
    return r


class TestPair(unittest.TestCase):
    def test_unique(self):
        s=[1,2,3,4,5,6,7,8]
        a=7
        r=find_pair(s,a)
        self.assertEqual(r,[(1,6),(2,5),(3,4)])

    def test_not_unique(self):
        s=[3,3,3,4,4,4,4]
        a=7
        r=find_pair(s,a)
        self.assertEqual(r,[(3,4)])
