#!/usr/bin/env python

import unittest

class MoneyFmt(object):
    def __init__(self, v):
        self.value=float(v)
        
    def update(self,v):
        self.value=float(v)
    
    def __repr__(self):
        return repr(self.value)

    def __str__(self):
        the_str=''
        if self.value<0:
            the_str+='-'
        the_str+="$%.2f" %(abs(self.value))
        return the_str
    
    def __nonzero__(self):
        return (abs(self.value)>=0.005)

class MoneyFmt_test(unittest.TestCase):
    def test_init(self):
        cash = MoneyFmt(123)
        self.assertEqual('$123.00', str(cash))

    def test_init_float(self):
        cash = MoneyFmt(123.45)
        self.assertEqual('$123.45', str(cash))
    
    def test_negative(self):
        cash = MoneyFmt(-3)
        self.assertEqual('-$3.00', str(cash))
        
    def test_zero(self):
        cash = MoneyFmt(0.1)
        self.assertTrue(cash)


if __name__ == '__main__':
    unittest.main()