

import re
import unittest

class MyRe(object):
    def __init__(self):
        pass
    
    def ex_1_2(self,str_):
        r=re.compile('(\w+) (\w+)')
        m=r.match(str_)
        if m is not None:
            return m.group(1), m.group(2)
    
    def ex_1_2_split(self,str_):
        p=', |(?= (?:\d{5}|\[A-Z]{2})) '
        return re.split(p, str_)
        

class TestRe(unittest.TestCase):
    def test_ex_1_2(self):
        inst=MyRe()
        f,l=inst.ex_1_2("michael jordon")
        self.assertEqual(f,'michael')
        self.assertEqual(l,'jordon')

    def test_ex_1_2_split(self):
        inst=MyRe()
        s=inst.ex_1_2_split('Mountain View, CA 94040')
        self.assertEqual(['Mountain View', 'CA', '94040'], s)