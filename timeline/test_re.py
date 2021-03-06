#!/usr/bin/env python

import unittest
from lte_re import *


logs=("23352:  1F9    360          10:18:57.690396672    19456  FWK_TIMELINE - save_subframe_boundary_timing():363 - Subframe_Boundary: 0, sfn=1, subframe=0, local_time.sfn=1124, local_time.subframe_num=1",
"23353:  1F9    284          10:18:57.690873600   476928  FWK_TIMELINE - DumpTimeLine():286 - OPID_PRACH_OVERALL: 130000 - 390000, sfn=1, subframe=1",
"23354:  1F9    284          10:18:57.691374592   500992  FWK_TIMELINE - DumpTimeLine():286 - OPID_DL_PROCESS: 26000 - 2470000, sfn=1, subframe=3")
    
    
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

    def test_get_log_of_sfn_1(self):
        print get_log_of_sfn("run.log",1124)

    def test_get_timeline_of_srs_2(self):
        self.assertEqual((10,950),get_task_start_and_end_time_2(logs,"dl", 1,3))

#     def test_get_timeline_of_pucch(self):
#         self.assertEqual((2000,3000),get_task_start_and_end_time("pucch", 1,2))
    
        