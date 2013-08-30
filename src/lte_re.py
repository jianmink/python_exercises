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
#                 print m.groups()
                return float(m.groups()[0])/CPU_FREQUENCY_IN_MHZ
    

def get_task_start_and_end_time(task_name,fn,sfn):
    pattern = "%s: (\d+) - (\d+), sfn=%d, subframe=%d" %(task_name_map[task_name],fn,sfn)
    with open(run_data_filename, 'r') as f:
        for eachline in f:
            m =re.search(pattern, eachline)
            if m is not None:
#                 print m.groups()
                start_time=m.groups()[0]
                end_time=m.groups()[1]
                return float(start_time)/CPU_FREQUENCY_IN_MHZ, float(end_time)/CPU_FREQUENCY_IN_MHZ

def get_task_start_and_end_time_2(logs,task_name,fn,sfn):
    pattern = "%s: (\d+) - (\d+), sfn=%d, subframe=%d" %(task_name_map[task_name],fn,sfn)
    for eachline in logs:
        m =re.search(pattern, eachline)
        if m is not None:
            start_time=m.groups()[0]
            end_time=m.groups()[1]
            return float(start_time)/CPU_FREQUENCY_IN_MHZ, float(end_time)/CPU_FREQUENCY_IN_MHZ

def get_log_of_sfn(log_filename,sfn):
    ret=[]
    pattern = ".+, sfn=%d,.+[\s]*" %(sfn)
    print pattern
    with open(log_filename, 'r') as f:
        for eachline in f:
            m =re.match(pattern, eachline)
            if m is not None:
                print m.group()
                ret.append(m.group())
    return ret



class time_logs(object):
    NUM_LINES_PER_RECORDS=1000
    def __init__(self):
        self.start_line_num=0
        self.bulk=None
        self.block=[]
        self.sfn=0
        
    def open(self,filename):
        self.f=open(filename, 'r')
    
    def next_bulk(self):
        self.bulk=[]
        for i,each in enumerate(self.f):
            if i<self.start_line_num:
                continue
            elif i==self.start_line_num+self.NUM_LINES_PER_RECORDS+2:
                self.start_line_num=i
                break;
                
            else:
                self.bulk.append(each)
        raise EOFError
    
    
    def next_sfn_block(self):
        pattern = 'Subframe_Boundary: (\d+), sfn=(\d+), subframe=0'
        
        try:
            if self.bulk is None:
                self.next_bulk()
        except EOFError: 
            print "End of file"
            raise EOFError
        
        
        else:
            flag=0
            start_time=0
            for eachline in self.bulk:
                m = re.search(pattern, eachline)
                if m is not None:
                    if flag==1:
                        print "end block"
                        flag=0
                        return self.block
                    else:
                        print "start block"
                        flag=1
                        if ((self.sfn+1)%4096) <= m.groups()[1]:
                            self.sfn =  m.groups()[1]
                            start_time=float(m.groups()[0])/CPU_FREQUENCY_IN_MHZ
                            flag=1
                        else:
                            continue
                else:
                    pattern_task = ": (\d+) - (\d+), sfn=%d, subframe=%d" %(task_name_map[task_name],self.sfn)
                    
            else:
                self.bulk=None
                    
         
    
        
def get_packet_fn(packet_type, sfn_ai, subframe_ai):
    max_sfn=4096
    max_subframe=10
    sfn = (sfn_ai + (subframe_ai + offset_to_air_interface[packet_type])/max_subframe)%max_sfn
    subframe= (subframe_ai + offset_to_air_interface[packet_type]) %max_subframe
    return sfn, subframe
    
            