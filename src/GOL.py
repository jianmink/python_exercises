import unittest
import copy
import os
import time


def gol(m,n):
    if len(n)==0:
        for h in m.keys(): m[h]='dead'
        return
    
    m_=copy.deepcopy(m)
    
    for h in m.keys():
        x = len([k for k in n[h] if m_.has_key(k) and m_[k]=='live'])
            
        if m[h]=='live' and (x == 2 or x ==3):
                m[h]='live'
        elif m[h]=='dead' and x==3:
            m[h]='live'
        else: 
            m[h]='dead'

class TestGOL(unittest.TestCase):
    def testOneDeadOne(self):
        m={'a':'dead'}
        n={}
        gol(m,n)
        self.assertEqual({'a':'dead'}, m)
        
    def testOneLiveOne(self):
        m={'a':'live'}
        n={}
        gol(m,n)
        self.assertEqual({'a':'dead'}, m)
        
    def testTwoLiveOnesInNeighborhood(self):
        m={'a':'live', 'b':'live'}
        n={'a':['b',], 'b':['a',]}
        gol(m,n)
        self.assertEqual({'a':'dead', 'b':'dead'}, m)    
    
    def test3LiveOnesInNeighborhood(self):
        m={'a':'live', 'b':'live', 'c':'live'}
        n={'a':['b','c'], 'b':['a','c'], 'c':['a','b']}
        gol(m,n)
        self.assertEqual({'a':'live', 'b':'live','c':'live'}, m)    

    def test4(self):
        m={'a':'live', 'b':'dead', 'c':'live','d':'live'}
        n={'a':['b','c'], 'b':['a','c','d'], 'c':['a','b'], 'd':['b']}
        gol(m,n)
        self.assertEqual({'a':'dead', 'b':'live', 'c':'dead','d':'dead'}, m)
        
class Game():
    """ game """
    def __init__(self):
        self.m = {}
        self.n={}
    
    def init(self,matrix):
        self.x = len(matrix)
        self.y = len(matrix[0])
        
        for x, item in enumerate(matrix):
            for y, sub_item in enumerate(item):
                self.n[(x,y)]=[]
                self.n[(x,y)].extend([(x-1,y-1),(x,y-1),(x+1,y-1),
                                      (x-1,y),          (x+1,y),
                                      (x-1,y+1),(x,y+1),(x+1,y+1)])
                
                if sub_item == 1:
                    self.m[(x,y)]='live'
                else:
                    self.m[(x,y)]='dead'
    
    def run(self,times):
        self.printf(self.to_matrix())
        
        matrix=[]
        for _ in range(times):
            gol(self.m,self.n)
            matrix=self.to_matrix()
            self.printf(matrix)
            time.sleep(0.5)
        
        return matrix
        
    def to_matrix(self):
        board=[[0]*self.y for _ in range(self.x)]
        
        for i in range(self.x):
            for j in range(self.y): 
                if self.m[(i,j)] =='live': board[i][j]=1
            
        return board
    
    def to_string(self,matrix):
        str_=''
        for item in matrix:
            str_+= "   "
            for subitem in item:
                if subitem == 1:
                    str_+= '* '
                else:
                    str_+= '  '
            str_+='\n'
        return str_
        
    
    def printf(self, matrix):
        os.system("clear")
        print 
        print '*'*self.y+' game of life '+'*'*self.y
        print 
        print self.to_string(matrix),
        print
        print '*'*self.y+' game of life '+'*'*self.y  

class TestGame(unittest.TestCase):

    @unittest.skip('...')
    def test_game_batch_init(self):
        game=Game()
        game.init([ [0,1,0]])
        self.assertEqual([[0,1,0]],game.to_matrix())

    
    def test_flower(self):
        game=Game()
        game.init([ [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0],
                         [0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0],
                         [0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0],
                         [0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0],
                         [0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0],
                         [0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0],
                         [0,0,1,0,0,0,0,1,0,1,0,0,0,0,1,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,1,1,1,0,0,0,1,1,1,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
                         [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0]
                         ])
        
#         game.printf(game.to_matrix())
#         game.to_matrix()
        game.run(100)

if __name__ == '__main__':
    unittest.main()
