#!/usr/bin/env python
" text editor "

import os


def write_text():
    while True:
        filename=raw_input("please input the filename> ")
        if os.path.exists(filename):
            print "file already exist, please choose another one"
        else:
            break
    
    all=[]
    print "please input the text, '.' itself for exit"
    while True:
        text = raw_input("> ")
        
        if text == '.':
            break
        else:
            all.append(text)
        
    f=open(filename, 'w')
    if f:
        f.write('\n'.join(all)+'\n')
        f.close()
    
def read_text():
    filename = raw_input("please input the filename> ")
    if os.path.exists(filename):
        f=open(filename, 'r')
    else:
        print "file not exist!"
        return
    
    for text in f:
        print text,
    f.close()

def edit_text():
    filename = raw_input("please input the fileanme> ")
    if not os.path.exists(filename):
        print "file not exist"
        return 
    
    
    f=open(filename, 'r')
    texts=f.readlines()
    f.close()
    i = 0
    for text in texts:
        print "%03d:" %(i),text, 
        i+=1
    
    print "please input the line num, '.' itself to exit"
    while True:
        input_item = raw_input("> ")
        if input_item == '.':
            break
        
        number=int(input_item)
        
        if number < len(texts) and number >= 0:
            print texts[number],
        else:
            print "illegal line number"
            continue
        
        print "please input the text"
        texts[number]=raw_input("> ")
        
    f=open(filename, 'w')
    for text in texts:
        f.write(text)
    f.write('\n')
    f.close()
        

        
if __name__ == "__main__":
    while True:
        choice=raw_input("(1)read\n"
                         "(2)write\n"
                         "(3)edit\n"
                         "(0)exit\n"
                         "> ")
        if choice == '1':
            read_text()
        elif choice == '2':
            write_text()
        elif choice == '3':
            edit_text()
        else:
            break
    
        
            
        