


'''
dn_range:
    len:    number of dn digits
    min_dn:  min int value that dn string represents
    max_dn:  max int value that dn string represents  
    e.g. 
    len   : 5
    min_dn: 12300 
    max_dn: 45600

limitation: no overlap between two dn_range 
            that means for each dn, there is at most one matched dn_range for it.
            
'''


# class ScopeMap():
#     def __init__(self):
#         self.maxDn = 0
#         self.searchMap={}
# 
# 
# class SearchImp():
#     def __init__(self):
#         self.scopeMaps=[]
#         for _ in range(18):
#             self.scopeMaps.append(ScopeMap()) 
# 
# 
#     def find(self, dn):


import unittest
import collections

'''
dn_range:
    len:    number of dn digits  
    min_dn: 12300 
    max_dn: 45600

For dn of a certain length,
    no overlap between two dn_range 
'''



class ScopeSearchMultiMapImp():
    def __init__(self):
        self.ranges=collections.OrderedDict()
         
    def append(self,min,max):
        self.ranges[min]=max

    def find(self, dn):
        pass
    
    
    def dump(self):
        print self.ranges

class TestMultiMap(unittest.TestCase):
    def testNoOverLap(self):
        search = ScopeSearchMultiMapImp() 
        search.append(10,(20,90))
        search.append(50,(60,))
        search.append(80,(90,))
        search.dump()
        
#         result=search.find(12)
#         self.assertEqual(result, [(10,20)])


class ScopeSearchImp():
    def __init__(self):
        self.ranges=[]
         
    def append(self,min,max):
        self.ranges.append((min,max))

    def find(self, dn):
        s = {e[1]-e[0]:e for e in self.ranges if (e[0]<=dn and e[1]>=dn)}
        k = min(s.keys())
        return s[k]

    
    def dump(self):
        print self.ranges

Search = ScopeSearchImp
class TestScopeMap(unittest.TestCase):
    def testNoOverLap(self):
        search = Search() 
        search.append(10,20)
        search.append(50,60)
        search.append(80,90)
        
        result=search.find(12)
        self.assertEqual(result, (10,20))

#     def testOverLap1(self):
#         search = Search() 
#         search.append(10,20)
#         search.append(10,60)
#         search.append(80,90)
#         
#         result=search.find(12)
#         self.assertEqual(result, [(10,20)])        
# 
#     def testOverLap2(self):
#         search = Search() 
#         search.append(10,20)
#         search.append(15,20)
#         search.append(80,90)
#         
#         result=search.find(16)
#         self.assertEqual(result, [(15,20)])         
# 
#     def testOverLap3(self):
#         search = Search() 
#         search.append(10,20)
#         search.append(15,25)
#         search.append(80,90)
#         
#         result=search.find(16)
#         self.assertEqual(result, [(10,20)])           
