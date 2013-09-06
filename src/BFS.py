#!/usr/bin/env python
import unittest
import logging 
import logging.config

color_list = ('y', 'r','g', 'p', 'b','w')

COLOR_X= (0, 1)
COLOR_Y= (2, 3)
COLOR_Z= (4, 5)

# create logger
logging.config.fileConfig('logging.conf')
logger = logging.getLogger('simpleExample')


def my_hash(p, c):
    h = p[0]+p[1]*2+p[2]*4
    h+= c[0]*8 + c[1]*64 + c[2]*812
    return h

def check(cubiers):
    other_cubiers=cubiers
    for one in cubiers:
        for other  in other_cubiers:
            if one!=other:
                h1=my_hash(one,cubiers[one])
                h2=my_hash(other,other_cubiers[other])
                if h1==h2:
                    print "*****"
                    print one, cubiers[one], h1
                    print other, other_cubiers[other], h2
                    print "*****"
 
def my_hash_plus(cubiers):
    hash_v = []
    for each in cubiers:
        hash_v.append(each.__hash__())
    return tuple(hash_v)


class Plane(object):
    def __init__(self,p=0,c=0):
        self.c=c
        self.p=0
    def __eq__(self, other):
        return self.p==other.p and self.c==other.c
                

class Cubier(object):
    def __init__(self, p=(0,0,0), c=(0,0,0)):
        self.planes=[]
        # each cubier has 3 visible planes 
        for i in range(3):
            self.planes.append(Plane(p[i],c[i]))
                            
    def __str__(self):
        return 'todo'
    
    def __hash__(self):
        h=0
        for i in range(3):
            h+= self.planes[i].c*pow(8,i)
        return h
    
    def __eq__(self, other):
        return other.__hash__() == self.__hash__()
    
    def __lt__(self, other):
        return other.__hash__() < self.__hash__()
    

class Vertex(object):
    def __init__(self, cubiers={}):
        self.cubiers= cubiers
#        for each in cubiers:
#            self.cubiers[each.p]=each           
    
    def __str__(self):
        return "Vertex str() todo!"
    
    def __hash__(self):
#        hash_v = []
        h = 0
        i = 0 
        for each in self.cubiers:
#            hash_v.append(self.cubiers[each].__hash__())
            h+= self.cubiers[each].__hash__() * 2480* i
            i+=1
        return h
    
    def __eq__(self, other):
        return self.__hash__()== other.__hash__()
    
#    def __lt__(self, other):
#        
    
    
    def turn_around_x_axis(self,x):
        new_cubiers=self.cubiers.copy()
        new_cubiers[(x,0,0)]= self.cubiers[(x,0,1)] 
        new_cubiers[(x,1,0)]= self.cubiers[(x,0,0)] 
        new_cubiers[(x,1,1)]= self.cubiers[(x,1,0)] 
        new_cubiers[(x,0,1)]= self.cubiers[(x,1,1)]
        return Vertex(new_cubiers) 
    
    def turn_around_x_axis_i(self,x):
    # inverse 
        new_cubiers=self.cubiers.copy()
        new_cubiers[(x,0,1)]= self.cubiers[(x,0,0)] 
        new_cubiers[(x,0,0)]= self.cubiers[(x,1,0)] 
        new_cubiers[(x,1,0)]= self.cubiers[(x,1,1)] 
        new_cubiers[(x,1,1)]= self.cubiers[(x,0,1)]
        return Vertex(new_cubiers) 
        
        
#    def turn_around_y_axis(self,y, cubiers):
#        new_cubiers=cubiers
#        new_cubiers[(0,y,0)]= cubiers[(0,y,1)] 
#        new_cubiers[(1,y,0)]= cubiers[(0,y,0)] 
#        new_cubiers[(1,y,1)]= cubiers[(1,y,0)] 
#        new_cubiers[(0,y,1)]= cubiers[(1,y,1)]
#        return new_cubiers 
#    
#    def turn_around_y_axis_i(y, cubiers):
#        new_cubiers=cubiers
#        new_cubiers[(0,y,1)]= cubiers[(0,y,0)] 
#        new_cubiers[(0,y,0)]= cubiers[(1,y,0)] 
#        new_cubiers[(1,y,0)]= cubiers[(1,y,1)] 
#        new_cubiers[(1,y,1)]= cubiers[(0,y,1)]
#        return new_cubiers 
#        
#    def turn_around_z_axis(z, cubiers):
#        new_cubiers=cubiers
#        new_cubiers[(0,0,z)]= cubiers[(1,0,z)] 
#        new_cubiers[(1,0,z)]= cubiers[(1,1,z)] 
#        new_cubiers[(1,1,z)]= cubiers[(0,1,z)] 
#        new_cubiers[(0,1,z)]= cubiers[(0,0,z)]
#        return new_cubiers 
#        
#    def turn_around_z_axis_i(z, cubiers):
#        new_cubiers=cubiers
#        new_cubiers[(1,0,z)]= cubiers[(0,0,z)] 
#        new_cubiers[(1,1,z)]= cubiers[(1,0,z)] 
#        new_cubiers[(0,1,z)]= cubiers[(1,1,z)] 
#        new_cubiers[(0,0,z)]= cubiers[(0,1,z)]
#        return new_cubiers  
    
 
class PocketCube(object):
    def __init__(self, n=2):
        self.n=n
        self.init_cubiers=[]
        cubiers={}
        for x in range(0, 2):
            for y in range(0,2):
                for z in range(0,2):
                    item = Cubier((x,y,z), (COLOR_Z[z], COLOR_Y[y], COLOR_X[x]))
                    cubiers[(x,y,z)]=item
        self.vertex = Vertex(cubiers)
             
        self.level = {}
        self.parent = {} 
        
#        self.create_BFS_search_tree()                      
                       
        
    def search(self, node):
        children=[]
        adj = []
        for x in range(0,2):
            adj.append(node.turn_around_x_axis(x))
            adj.append(node.turn_around_x_axis_i(x))
#        for y in range(0,2):
#            adj.append(turn_around_y_axis(y, node))
#            adj.append(turn_around_y_axis_i(y, node))
#        for z in range(0,2):
#            adj.append(turn_around_z_axis(z, node))
#            adj.append(turn_around_z_axis_i(z, node))
            
        
        for each in adj:
            if each not in self.level:
                self.level[each]= self.level[node]+1
                children.append(each)
                self.parent[each]=node
        return children 

    def BFS_search(self,s):
        ''' breath first search
            node: start node
        '''  
        print s 
        self.level = {s: 0}
        self.parent = {s:None}
        
        frontier = [s,]
        
        while frontier:
            next = []
            for each_node in frontier:
                next.extend(self.search(each_node))
            frontier=next
        return self.level, self.parent
    
    def create_BFS_search_tree(self):
        print self.BFS_search(self.vertex)[0] 


class BFS(object):
    def __init__(self):
        self.level = {}
        self.parent = {}
        
    def search(self, adj,node):
        children=[]
        if node in adj:
            for each in adj[node]:
                if each not in self.level:
                    self.level[each]= self.level[node]+1
                    children.append(each)
                    self.parent[each]=node
        return children 

    def BFS_search(self,s, adj):
        ''' breath first search
            node: start node
            adj:  {a: (b, c),
                   b: (c)}    
        '''   
        self.level = {s: 0}
        self.parent = {s:None}
        
        frontier = [s,]
        if adj is None:
            return self.level, self.parent
        
        while frontier:
            next = []
            for each_node in frontier:
                next.extend(self.search(adj, each_node))
            frontier=next
        return self.level, self.parent
    
        
#if __name__ == '__main__':
#    unittest.main()