#!/usr/bin/env python

import unittest
from timeline import *
import re

CPU_FREQUENCY_IN_MHZ=2600


def get_frame_start_time():
    ''' us '''
    pattern = 'Subframe_Boundary: (\d+), sfn=\d+, subframe=0'
    with open('task_run_4_test.log', 'r') as f:
        for eachline in f:
            m = re.search(pattern, eachline)
            if m is not None:
                print m.groups()
                return float(m.groups()[0])/CPU_FREQUENCY_IN_MHZ
    

task_name_map={"PRACH": "OPID_PRACH_OVERALL"}

def get_task_start_and_end_time(task_name):
    pattern = task_name_map[task_name],": (\d+) - (\d+), sfn=\d+, subframe=\d+"
    with open('task_run_4_test.log', 'r') as f:
        for eachline in f:
            m =re.search(pattern, eachline)
            if m is not None:
                print m.groups()
                start_time=m.groups()[0]
                end_time=m.groups()[1]
                return start_time, end_time
        

class Test_re(unittest.TestCase):
    def test_get_start_time_of_frame(self):
        frame_start_time= get_frame_start_time()
        self.assertEqual(1000,frame_start_time)
        
    def test_get_timeline_of_prach(self):
        frame_start_time= get_task_start_and_end_time("PRACH")
        self.assertEqual(1000,frame_start_time)

