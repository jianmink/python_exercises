#!/usr/bin/env python
import unittest

from zc_sequence import ZCS, ZCS_LTE, acorr


class TestZadoffChuSequence(unittest.TestCase):

    def setUp(self):
        pass

    def test_dummy(self):
        self.assertEqual(1, 1)
    
    def acorr_test(self,n,q,the_shift):
        zcs = ZCS(n,q)
        (I,Q)=acorr(zcs.get_sequence(), zcs.shift(the_shift))
        self.assertAlmostEqual(0, I, None, "bingo", 1e-10)
        self.assertAlmostEqual(0, Q, None, "bingo", 1e-10)
            
    
    def test_root_sequence_5_1_shift_1(self):
        self.acorr_test(5,1,1)
 
    def test_root_sequence_5_2_shift_1(self):
        self.acorr_test(5,1,2)
    
    def test_acorr_5_1_3(self):
        self.acorr_test(5,1,3)

    def test_acorr_5_1_4(self):
        self.acorr_test(5,1,4)

    def test_acorr_5_1_5(self):
        zcs = ZCS(5,1)
        (I,Q)=acorr(zcs.get_sequence(), zcs.shift(5))
        self.assertTrue(I>1 or Q>1)
 
    def test_acorr_63_25_2(self):
        self.acorr_test(63,25,2)

class TestZadoffChuSequenceLTE(unittest.TestCase):

    def setUp(self):
        pass
    
    def acorr_test(self,nzc,u,the_shift):
        zcs = ZCS_LTE(nzc,u)
        (I,Q)=acorr(zcs.get_sequence(), zcs.shift(the_shift))
        self.assertAlmostEqual(0, I, None, "bingo", 1e-8)
        self.assertAlmostEqual(0, Q, None, "bingo", 1e-8)
            
    
    def test_root_sequence_839_129_shift_13(self):
        self.acorr_test(839,129,13)
        
    def test_root_sequence_839_129_shift_839(self):
        zcs = ZCS_LTE(839,129)
        (I,Q)=acorr(zcs.get_sequence(), zcs.shift(839))
        self.assertTrue(I>1 or Q>1)
 

         
if __name__ == '__main__':
    unittest.main()