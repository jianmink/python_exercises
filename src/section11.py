#!/usr/bin/env python

import unittest


def skip(func):
    def wrapper():
        print "\nskip %s\n" %(func.__name__)
    return wrapper

from functools import partial
import Tkinter

def button():
    root = Tkinter.Tk()
    MyButton = partial(Tkinter.Button, root,
                       fg='white', bg='blue')
    b1 = MyButton(text='Button 1')
    b2 = MyButton(text='Button 2')
    qb = MyButton(text='QUIT', bg='red',
                command=root.quit)
    b1.pack()
    b2.pack()
    qb.pack(fill=Tkinter.X, expand=True)
    root.title('PFAs!')
    root.mainloop()

@skip 
def my_func():
    return "my_func() invoked!"

class Test_section11(unittest.TestCase):
    
    def test_skip_decorator(self):
        self.assertEqual(None, my_func())
    
    @unittest.skip("...")
    def test_button(self):
        button()
        
    def test_map(self):
        func=lambda a,b:(a,b)
        self.assertEqual([(1,'abc'),(2,'def'),(3,'ghi')], 
                          map(func, [1,2,3],['abc', 'def','ghi'])) 
    
    def test_zip(self):
        self.assertEqual([(1,'abc'),(2,'def'),(3,'ghi')], 
                          zip([1,2,3],['abc', 'def','ghi'])) 
        
        
if __name__=="__main__":
    unittest.main() 