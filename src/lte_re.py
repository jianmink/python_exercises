#!/usr/bin/env python

from timeline import *
import re

CPU_FREQUENCY_IN_MHZ=2600

task_name_map={"rach": "OPID_PRACH_OVERALL",
                "dl": "OPID_DL_PROCESS",
                "srs": "OPID_SRS_PROCESS",
                "pusch": "OPID_PUSCH_PROCESS",
                "pucch": "OPID_PUCCH_PROCESS"
                }

offset_to_air_interface={"rach": 1,
                          "dl": 3,
                          "srs": 0,
                          "pusch":0,
                          "pucch":0
                              }

run_data_filename='task_run_4_test.log' 

def set_filename(filename):
    global run_data_filename
    run_data_filename=filename

def get_frame_start_time():
    ''' us '''
    pattern = 'Subframe_Boundary: (\d+), sfn=\d+, subframe=0'
    with open(run_data_filename, 'r') as f:
        for eachline in f:
            m = re.search(pattern, eachline)
            if m is not None:
                print m.groups()
                return float(m.groups()[0])/CPU_FREQUENCY_IN_MHZ
    

def get_task_start_and_end_time(task_name,fn,sfn):
    pattern = "%s: (\d+) - (\d+), sfn=%d, subframe=%d" %(task_name_map[task_name],fn,sfn)
    with open(run_data_filename, 'r') as f:
        for eachline in f:
            m =re.search(pattern, eachline)
            if m is not None:
                print m.groups()
                start_time=m.groups()[0]
                end_time=m.groups()[1]
                return float(start_time)/CPU_FREQUENCY_IN_MHZ, float(end_time)/CPU_FREQUENCY_IN_MHZ
        
def get_packet_fn(packet_type, sfn_ai, subframe_ai):
    max_sfn=4096
    max_subframe=10
    sfn = (sfn_ai + (subframe_ai + offset_to_air_interface[packet_type])/max_subframe)%max_sfn
    subframe= (subframe_ai + offset_to_air_interface[packet_type]) %max_subframe
    return sfn, subframe
    
            