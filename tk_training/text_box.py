from Tkinter import *
from time import sleep
from threading import Thread, Lock
import datetime



init_flag=1 
def draw(f,i):
    
    global init_flag
    if init_flag:   
        string_box=Text(f, bg='white', fg='blue', bd=1,relief=SUNKEN,width=20, height=1)   
        string_box.grid(row=0,column=0)
    
        Text(f, bg='white', fg='grey', relief=SUNKEN,width=1, height=1)   \
        .grid(row=1,column=0)
     
        pattern_box=Text(f, bg='white', fg='grey', bd=1,relief=SUNKEN,width=1, height=1)   
        pattern_box.grid(row=2,column=0,sticky=W)
        init_flag=0
 
 
    string_box.delete(1.0, END)           
    string_box.insert(1.0,"a|b|c|d|e|f|g")
 
    pattern_box.delete(1.0, END)           
    pattern_box.insert(1.0,"d|e|f")
    pattern_box.configure(width=len("d|e|f"))
    

 
def main():
    top = Tk()
 
    top.title("string match")
#    top.minsize(350,400)
    top.geometry("350x200+400+500")
    
    f = Frame(top)  
    f.grid(row=3,column=0,columnspan=3, rowspan=3, pady=4, padx=5, sticky=E+W+S+N)

 
    draw(f,i=2)
    mainloop()
 
 
if __name__ == '__main__':
    main()