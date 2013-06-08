#!/usr/bin/env python
from curses.ascii import isalpha, isupper
from random import choice
import unittest

def palindromic(the_str):
    " bob "
    for i in range(len(the_str)):
        if the_str[i]!=the_str[len(the_str)-i-1]:
            return False
            
    return True

def exercise_6_7(num_str):
    '''  this method generate a list and then remove
    some elements with a implicit rule.  
    '''
    if num_str == None:
        num_str=raw_input('enter a number:')
    num_num=int(num_str)
    
    non_fac_list=range(1,num_num+1)
    print "BEFORE:", repr(non_fac_list)
    
    i=0
    while i<len(non_fac_list):
        if num_num% non_fac_list[i]==0:
            del non_fac_list[i]
        # Note: del will make none_fac_list[i] refer to the next element.
        else:    
            i=i+1
    
    print "AFTER:",repr(non_fac_list)

digit_2_text= {0:'zero', 1:'one', 2:'two', 3:'three', 4:'four', 5:'five', 6:'six', 7:'seven', 8:'eight', 9:'nine',
              10:'ten', 11:'eleven', 12:'twelfth', 13:'thirteen', 14:'forteen', 15:'fifteen',16:'sixteen',17:'seventeen',18:'eighteen',19:'nineteen',
              20:'twenty', 30:'thirty', 40:'forty', 50:'fifty', 60:'sixty', 70:'seventy', 80:'eighty', 90:'ninety'}

unit=['','',' hundred', ' thousand']

def exercise_6_8(num):
    " print the text for a number"
    num_copy=num
    
    # get the list of all digits
    num_list=[]
    for each in str(num):
        num_list.append(int(each))
    
    list_size=len(num_list)

    number_text='' 
    for i, digit in enumerate(num_list):
        # 1008 --> 1 thousand and eight
        # skip redundant 'and'
        if digit==0:
            if num_list[i-1]!=0:
                number_text+=' and'
            continue
        
        # e.g 1008,  digit_index of '8' is 0, and digit_index of '1' is 3 
        digit_index = list_size-1-i         
        # add space except the first digit
        if i!=0:
            number_text+=' '
            # add 'and' except the last digit
            if digit_index!=0:
                number_text+='and '
        
        # hundred, thousand
        if digit_index>1:
            number_text+=digit_2_text[digit]+unit[digit_index]
        elif digit_index==1:
            if digit==1: # 10 ~ 19
                number_text+=digit_2_text[num_copy%100]
                break
            else:  # 20 ~ 90
                number_text+=digit_2_text[num_copy%100-(num_copy%10)]   
        else:
            number_text+=digit_2_text[digit]         

    return number_text


def reverse_upper_low(the_str):
    new_str=''
    for d in the_str:
        if isalpha(d):
            if isupper(d):
                new_str+=d.lower()
            else:
                new_str+=d.upper()
        else:
            new_str+=d
    print new_str


game_choices={'r':'rock', 'p':'paper', 's':'scissors'}
measure = {'r':0, 'p':1, 's':2}
game_result= {0:'tie', 1:'win', 2:'lost'}
def Rochambeau():

    while(1):
        print "(r)ock"
        print "(p)aper"
        print "(s)cissors"
        
        try:
            your_guess=raw_input('> ')
        except (EOFError, KeyboardInterrupt, IndexError):
            your_guess = 'x'
        
        if your_guess=='' or your_guess not in 'rpsx':
            print "invalid input, try again!"
            continue
        
        if your_guess == 'x':
            print "exit the game!"
            break
         
        
        computer_guess = choice('rps') 
        print 'your guess:    ', game_choices[your_guess]
        print 'computer guess:', game_choices[computer_guess]
        
        delta = (measure[your_guess] - measure[computer_guess]+3)%3
        print '                %s!' %(game_result[delta])
        


class TestExerciese(unittest.TestCase):
    def test_exerceise_6_8_1008(self):
        self.assertEqual("one thousand and eight", exercise_6_8(1008)) 

    def test_exerceise_6_8_1128(self):
        self.assertEqual("one thousand and one hundred and twenty eight", 
                         exercise_6_8(1128)) 


if __name__=='__main__':
    unittest.main()
#     print palindromic('bob')
#     print palindromic('alice')
#     print palindromic('taat')
#     print palindromic('')
#     exercise_6_7('12')
#     print exercise_6_8(108)
#     print exercise_6_8(118)
#     print exercise_6_8(1128)
#     print exercise_6_8(1008)
#     reverse_upper_low('Mr.Bob')
    #Rochambeau()
    
