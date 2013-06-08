#!/usr/bin/env python
import unittest

from gameOfLife import Game

class TestGame(unittest.TestCase):

    def setUp(self):
        pass

    def test_dummy(self):
        self.assertEqual(1, 1)
    
    def test_game_batch_init(self):
        self.game=Game(1,3)
        self.game.init([ [0,1,0] ])
        self.assertEqual([[0,1,0]],self.game.to_matrix())
 
#     def test_game_batch_init_3(self):
#         self.game=Game(3,3)
#         self.game.init([ [0,0,0],[1,1,1],[0,0,0] ])
#         self.assertEqual([[0,1,0],[0,1,0],[0,1,0]],self.game.run(1))  
#         self.assertEqual([[0,0,0],[1,1,1],[0,0,0]],self.game.run(1))
#         self.game.run(10)
    
    def test_flower(self):
        self.game=Game(17,17)
        self.game.init([ [0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0,0],
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
        
        init_matrix=self.game.to_matrix()
        self.game.run(3,True)
        self.assertEqual(init_matrix,self.game.to_matrix())
 
if __name__ == '__main__':
    unittest.main()
