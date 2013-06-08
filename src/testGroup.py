#!/usr/bin/env python
import unittest

from gameOfLife import Person, Group

class TestGroup(unittest.TestCase):

    def setUp(self):
        self.alu=Group()
        pass

    def test_dummy(self):
        self.assertEqual(1, 1)
    
    def test_group_w_0_live_person(self):
        self.assertEqual(0, self.alu.getLiveMember())
        
    def test_group_add_live_person(self):
        jack=Person()
        self.alu.add_live_member(jack)
        self.assertEqual(1, self.alu.getLiveMember())
        self.assertEqual(0,jack.get_num_live_neighbours())
     
    def test_group_calculate_livenb_of_live_member(self):
        self.alu.add_live_member(Person().set_x_y(0,0))
        self.alu.add_live_member(Person().set_x_y(0,1))
        jack=self.alu.get_person(0,0)
        self.assertEqual(1, jack.get_num_live_neighbours())
        pass

    def test_group_calculate_livenb_of_any_position(self):
        self.alu.add_live_member(Person().set_x_y(0,0))
        self.alu.add_live_member(Person().set_x_y(0,2))
        jack=self.alu.get_person(0,1)
        self.assertEqual(2,jack.get_num_live_neighbours())
        
    
    def test_group_next_generation(self):
        self.alu.add_live_member(Person().set_x_y(0, 0))
        self.alu.add_live_member(Person().set_x_y(0,2))
        self.alu.add_live_member(Person().set_x_y(2,0))
        self.alu.next_round()
        self.assertEqual(1,self.alu.getLiveMember())
        self.assertEqual(0,self.alu.get_person(1,1).get_num_live_neighbours())

if __name__ == '__main__':
    unittest.main()