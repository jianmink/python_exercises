#!/usr/bin/env python

def palindromic(the_str):
    "bob"
    for i in range(len(the_str)):
        if the_str[i]!=the_str[len(the_str)-i-1]:
            return False
            
    return True

def buggy():
    num_str=raw_input('enter a number:')
    num_num=int(num_str)
    
    non_fac_list=range(1,num_num+1)
    print "BEFORE:", repr(non_fac_list)
    
    i=0
    while i<len(non_fac_list):
        print "--> ", non_fac_list[i]
        if num_num% non_fac_list[i]==0:
            del non_fac_list[i]
        else:    
            i=i+1
    
    print "AFTER:",repr(non_fac_list)

digit_2_text= {0:'zero', 1:'one', 2:'two', 3:'three', 4:'four', 5:'five', 6:'six', 7:'seven', 8:'eight', 9:'nine',
              10:'ten', 11:'eleven', 12:'twelfth', 13:'thirteen', 14:'forteen', 15:'fifteen',16:'sixteen',17:'seventeen',18:'eighteen',19:'nineteen',
              20:'tweenty', 30:'thirty', 40:'forty', 50:'fifty', 60:'sixty', 70:'seventy', 80:'eighty', 90:'ninety'}

unit=['','','_hundred', '_thousand']

#todo: ugly solution >_<
def exercise_6_8(num):
    num_list=[]
    num_cp=num
    while num!=0:
        if num>=10:
            num_list.append(num%10)
            num=num/10
        else:
            num_list.append(num)
            num=0
            
    str_num=''
    i=len(num_list)-1
    while i >=0:
        if i!=len(num_list)-1:
            str_num+='-'
        
        digit=num_list[i]
        if i>1:
            if int(digit)==0:
                str_num+='and'
            else:
                str_num+=digit_2_text[digit]+unit[i]
        elif i==1:
            if int(digit)==0:
                str_num+='and'
            elif int(digit)==1:
                str_num+=digit_2_text[num_cp%100]
                break
            else:
                str_num+=digit_2_text[num_cp%100-(num_cp%10)]   
        else:
            str_num+=digit_2_text[digit]         
        i=i-1

    print str_num


if __name__=='__main__':
    print palindromic('bob')
    print palindromic('alice')
    print palindromic('taat')
    print palindromic('')
#     buggy()
    exercise_6_8(108)
    exercise_6_8(118)
    exercise_6_8(128)
    exercise_6_8(1028)
    
