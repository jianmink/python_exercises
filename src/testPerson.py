#!/usr/bin/env python
import unittest

from gameOfLife import game_of_Life_rules

class TestGameOfLife(unittest.TestCase):

    def setUp(self):
        pass

    def test_dummy(self):
        self.assertEqual(1, 1)
        
    def test_rule_1_die_w_0_live_nbs(self):
        self.assertFalse(game_of_Life_rules(1,0))
        
    def test_rule_2_live_w_3_live_nbs(self):
        self.assertTrue(game_of_Life_rules(1,3))
     
    def test_rule_2_live_w_2_live_nbs(self):
        self.assertTrue(game_of_Life_rules(1,2))
     
    def test_rule_4_revive_w_3_live_nbs(self):
        self.assertTrue(game_of_Life_rules(0,3))
     
    def test_rule_4_die_w_1_live_nbs(self):
        self.assertFalse(game_of_Life_rules(0,1))
         
if __name__ == '__main__':
    unittest.main()