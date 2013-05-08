#!/usr/bin/env python
" text editor "

import os


def write_text_file():
    while True:
        filename=raw_input("please input the filename, (b) back to previous menu\n>")
        if os.path.exists(filename):
            print "*** file already exist!"
        elif filename== 'b':
            return
        else:
            yes_no = raw_input('add a new file '+ filename+ ' (y/n): ')
            if yes_no == 'y':
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
    f.write('\n'.join(all)+'\n')
    f.close()
    print "DONE!"
    
def read_text_file():
    filename = raw_input("please input the filename> ")
    try:
        f=open(filename, 'r')
    except IOError, e:
        print "*** file open error:", e
    else:    
        for entry in f:
            print entry,
        f.close()


def edit_menu():
    print "---- edit menu ----"
    print "(u)update"
    print "(d)delete"
    print "(a)add"
    print "(s)save"
    print "(b)main menu"
    print "-------------------"  
    return raw_input('> ')

def edit_text_file():
    " line editor of text file "
    while True:
        filename = raw_input("please input the fileanme> ")
        if os.path.exists(filename):
            break;
        else:
            print "file not exist"
    
    try:
        f=open(filename, 'r')
    except IOError, e:
        print "*** file open error", e
    else:        
        texts=f.readlines()
        f.close()
        
    i = 0    
    for text in texts:
        print "%03d:" %(i),text, 
        i+=1
    
    while True:
        choice = edit_menu()
        if choice == 'u':
            entry = raw_input("line num> ")        
            
            if not entry.isdigit():
                continue

            number=int(entry)
            if number >= len(texts) or number < 0:
                print "illegal line number"
            else:
                print texts[number],
                texts[number]=raw_input("new text> ")
        elif choice == 's':
            f=open(filename, 'w')
            for text in texts:
                f.write(text)
                f.write('\n')
            f.close()
        elif choice == 'b':
            break
        #todo : add, delete
        

def main_menu():
    choice=raw_input("--------------- main menu --------------\n"
                     "(r)read \t"
                     "(n)new  \t"
                     "(e)edit \n"
                     "(x)exit \t"
                     "(l)list \t"
                     "(c)clear\n"
                     "----------------------------------------\n"
                     "> ")
    if choice == 'r':
        read_text_file()
    elif choice == 'n':
        write_text_file()
    elif choice == 'e':
        edit_text_file()
    elif choice == 'x':
        return False
    elif choice == 'l':
        os.system('ls -lh | grep -v py')
    elif choice == 'c':
        os.system('clear')
    else:
        pass
    
    return True
    

        
if __name__ == "__main__":
    while main_menu():
        pass
        
            
        