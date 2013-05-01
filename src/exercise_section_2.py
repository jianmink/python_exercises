#!/usr/bin/env python


def user_input(func):
    while 1:
        the_str=raw_input(":>")
        if 'exit' == the_str:
            break
        func(the_str)


def echo(the_str):
    print the_str 
    
def q_2_4_a():
    user_input(echo)

def toInt(the_str):
    print int(the_str)
def q_2_4_b():
    user_input(toInt)

def q_2_5_a():
    count=0
    i=0
    while i<=10:
        count+=i
        i+=1
    print count

def q_2_5_b():
    count =0
    for i in range(0,11):
        count +=i
    print count
    

def print_char(the_str):
    for c in the_str:
        print c
def q_2_7_a():
    user_input(print_char)

def print_char_w_while_loop(the_str):
    i=0
    while i<len(the_str):
        print the_str[i]
        i+=1 
def q_2_7_b():
    user_input(print_char_w_while_loop)    
    
    
def q_2_8_a():
    count =0
    numbers=[]
    print "please input 5 numbers"
    for i in range(0,5):
        numbers.append(int(raw_input('q_2_8_a :> ')))
    
    for i in numbers:
        count +=i
    print count 
    
def menu():
    while 1:
        print "-----menu-----"
        print "(1) count"
        print "(X) exit"
        case = raw_input("your case selection $> ")
        if case == '1':
            q_2_8_a()
        elif case == 'X':
            break
        else:
            print "please input the correct case number or 'X' to exit!"
        
    
if __name__=='__main__':
    menu()
#     print "python -c 'from exercise_1 import *; ...'"
#     print 'q_2_4_a()'
#     print 'q_2_4_b()'
        