
import unittest

class SearchNode:
    def __init__(self):
        self.sub_nodes={}
        self.v=None
        self.records={}
    
    def add(self, dn, naptr):
        print "add- %s  \t%s" %(dn, naptr)
        self.add_r(dn,naptr, -1)
    
    def add_r(self, dn, naptr, ix):
        ix+=1;
        
        # leaf node
        if ix == len(dn):
            if not self.records.has_key(dn):
                self.records[dn]=[]
                           
            self.records[dn].append(naptr)
            return
        
        # inner node   
        c = int(dn[ix]) 
        if not self.sub_nodes.has_key(c):
            self.sub_nodes[c]=SearchNode()
            self.sub_nodes[c].v=c
        
        self.sub_nodes[c].add_r(dn, naptr,ix)

    def dump(self,level=0):
        
        if level==0: print "-------------------------------------------------------"
        if level==0: print "-------------------------------------------------------"
        
        print "\t"*level,
        print "node( ", self.v,",",self.records, ")"
        
        for each in self.sub_nodes.keys():
            self.sub_nodes[each].dump(level+1)
            
        if level==0: print "-------------------------------------------------------"
        if level==0: print "-------------------------------------------------------"
            
        
        

class EnumFESearchDemo:   
    def __init__(self):
        self.root = SearchNode()
    
    def add(self, key, value):
        self.root.add(key, value)
  
  
    #longest match
    def find(self, dn):
        result = {}
        
        root = self.root
        for each in dn:
            x=int(each)
            if not root.sub_nodes.has_key(x): break
                
            root= root.sub_nodes[x]
            if len(root.records)>0: result= root.records
        
        print "find(" ,dn,") ", result
        return result
        
  
    def dump(self):
        self.root.dump()
        
    
class TestMyTree(unittest.TestCase):
    def testMySearch(self):
        demo=EnumFESearchDemo()
        demo.add('0','naptr-1')
        demo.add('01','naptr-2')
        demo.add('01','naptr-3')
        demo.add('1','naptr-4')
        demo.add('123','naptr-5')
        
        
#         print demo.toString()
        demo.dump()
        demo.find('1')
        demo.find('12345')
        demo.find('127')
        demo.find('523')
        