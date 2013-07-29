#!/usr/bin/env python

import unittest
from lte_re import *


    
    
class Test_re(unittest.TestCase):
    def test_get_start_time_of_frame(self):
        self.assertEqual(0,get_frame_start_time())
    
    def test_frame_offset_ai(self):
        self.assertEqual((1,1), get_packet_fn("rach",1,0))
        
    def test_get_timeline_of_prach(self):
        self.assertEqual((50,150),get_task_start_and_end_time("rach", 1,1))

    def test_get_timeline_of_dl(self):
        self.assertEqual((10,950),get_task_start_and_end_time("dl", 1,3))

    def test_get_timeline_of_srs(self):
        self.assertEqual((1050,1050),get_task_start_and_end_time("srs", 1,1))

    def test_get_timeline_of_pucch(self):
        self.assertEqual((2000,3000),get_task_start_and_end_time("pucch", 1,2))
    
        