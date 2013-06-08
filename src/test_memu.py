#!/usr/bin/env python

''' test memu template 
    
'''
import os
import time
import sys

from multiprocessing import Process

def run_test(case_no):
    print case_no, "start!"
    os.system("ls -lh&")
    time.sleep(5)
    print case_no, "done!"

def process_log():
    print "process_log start!"
    time.sleep(1)
    print "process_log end!"

def test_menu():
    print "-----------------------------"
    print "(r) run test       "
    print "(l) log processing "
    print "(c) clean screen   "
    print "(x) exit "
    print "-----------------------------"

def check_run_test_status(test_process):
    while test_process.is_alive():
        print "check ... "
        time.sleep(1)
        # check the test result
        # todo ...
    print "test completed"
     
def batch_test(case_no):
    p=Process(target=run_test, args=(case_no,))
    p.start()
    
    check_run_test_status(p)
    time.sleep(1)

def run_something():
    while True:
        case_no = raw_input("case number: ")
        if 'y' == raw_input('run test case' + case_no + '(y/n)? '):
            break
                
    p = Process(target=run_test, args=(case_no,))
    p.start()
    check_run_test_status(p)
    time.sleep(1)

CMDS={'l':process_log, 'r': run_something}

def interactive_test():
    while True:
        test_menu()
        try:
            choice=raw_input('> ')
        except (EOFError, KeyboardInterrupt, IndexError):
            choice = 'x'
        
        if choice =='' or choice not in 'xrlc':
            print "invalid choice:%s, try again!" %(choice)
        elif choice == 'x':
            return 
        elif choice == 'c':
            os.system('clear')
        else:    
            CMDS[choice]()

        
if __name__ == "__main__":
    if len(sys.argv) == 2:
        batch_test(sys.argv[1])
    else:
        interactive_test()
    
