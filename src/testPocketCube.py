#!/usr/bin/env python
from BFS import *
    
class TestBFSAlogrithm(unittest.TestCase):
    def setUp(self):
        self.inst=BFS()

    def test_BFS_level_0(self):
        adj = None
        level, parent = self.inst.BFS_search('a', adj) 
        self.assertEqual(0, level['a'])

    def test_BFS_level_1(self):
        adj = {'a': ('b',)}
        level, parent = self.inst.BFS_search('a', adj) 
        self.assertEqual(1, level['b'])
    
    def test_BFS_level_3(self):
        adj = {'a': ('b','c'),
               'b': ('d',)}
        level, parent = self.inst.BFS_search('a', adj) 
        self.assertEqual(1, level['b'])    
        self.assertEqual('a', parent['b'])
        
class TestPlane(unittest.TestCase):
    def test_eq(self):
        a = Plane()
        b = Plane()
        self. assertEqual(a,b)
    def test_not_eq(self):
        a = Plane()
        b = Plane(p=1,c=1)
        self. assertNotEqual(a,b)

class TestCubier(unittest.TestCase):
    def test_eq(self):
        a = Cubier()
        b = Cubier()
        self.assertEqual(a,b)
    
    def test_not_eq(self):
        a = Cubier()
        b = Cubier((0,1,0))
        self.assertNotEqual(a,b)
        
class TestVertex(unittest.TestCase):
    def test_eq(self):
        a = Vertex()
        b = Vertex()
        self.assertEqual(a, b)
        
    def test_not_eq(self):
        a = Vertex((Cubier(),))
        b = Vertex((Cubier((0,1,0)),))
        self.assertNotEqual(a, b)

#class TestCube(unittest.TestCase):      
#    def test_cube_n_2(self):
#        cube=PocketCube(n=2)
#        cube.create_BFS_search_tree()
#        ref= reduce(lambda a,b : a*b, range(1,9)) * pow(3,7) /24
#        self.assertEqual(ref,cube.get_num_vertex())
#        self.assertEqual(0,cube.get_num_edge())
         
if __name__ == '__main__':
    unittest.main()