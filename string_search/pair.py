
import unittest


#given numbers[], find (number[i], number[j]) that number[i] + number[j] = S
def find_pair_bruteforce(s, X):
    r = []
    for i in range(len(s)):
        for j in range(i,len(s)):
            if s[i]+s[j] == X: r.append((s[i],s[j])) 
    
    return r

def find_pair_py(s,X): 
    return [(a, X-a) for a in s if a<X-a and X-a in s ]


#precondition: list is in order, no duplicate number 
def find_pair(s, X):
    r = []
    i,j = 0, len(s) - 1
    while i < j:
        if s[i] + s[j] == X:
            r.append((s[i], s[j]))  
#             i+=1
#             j-=1
                     
            p,q = s[i],s[j] 
            while i<j and s[i] == p: 
                i += 1
            while i<j and s[j] == q:
                j -= 1
            
        elif s[i] + s[j] < X:
            i += 1
        else:
            j -= 1
                
    return r


class TestPair(unittest.TestCase):
    def test_bt(self):
        self.assertEqual(find_pair_bruteforce((1,2,3,4,5), 5),
                         [(1,4),(2,3)])
    
    def test_bt_py(self):
        self.assertEqual(find_pair_py((1,2,3,4,5), 5),
                         [(1,4),(2,3)])
        
    
    def test_unique(self):
        self.assertEqual(find_pair((1,2,3,4,5,6,7,8),7),
                         [(1,6),(2,5),(3,4)])

    def test_not_unique(self):
        self.assertEqual(find_pair((2,2,4,4,4,6,6),8),
                         [(2,6),(4,4)])
