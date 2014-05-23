
import unittest

def find_pair(s,a):
    r=[]
    i=0 
    j=len(s)-1
    while i < j:
        if s[i]+s[j]==a:
            r.append([i,j])
            j-=1
        elif s[i]+s[j]<a:
            i+=1
        else:
            j-=1
                
    return r


class TestPair(unittest.TestCase):
    def test_find_pair(self):
        s=[1,2,3,4,5,6,7,8]
        a=7
        r=find_pair(s,a)
        self.assertEqual(r,[[0,5],[1,4],[2,3]])
