#!/usr/bin/env python

''' test memu template 
    
'''
import os
import time

from multiprocessing import Process

def run_test(case_no):
    print "case_no start!"
    os.system("ls -lh&")
    time.sleep(5)
    print "case_no done!"

def process_log():
    print "process_log start!"
    time.sleep(1)
    print "process_log end!"

def test_menu():
    print "-----------------------------"
    print "(r) run  "
    print "(l) log  "
    print "(c) clean screen "
    print "(x) exit "
    print "-----------------------------"

def check_run_test_status(test_process):
    while test_process.is_alive():
        print "check ... "
        time.sleep(1)
        # check the test result
        # todo ...
    print "test completed"
        
def test_main():
    while True:
        test_menu()
        choice=raw_input('> ')
        if choice == 'x':
            return 
        elif choice == 'r':
            p=Process(target=run_test, args=('3020_10UEs',))
            p.start()
            
            check_run_test_status(p)
            
            time.sleep(1)
        elif choice == 'l':
            process_log()
        elif choice == 'c':
            os.system('clear')
        else:
            pass
        
    

if __name__ == "__main__":
    test_main()
    
