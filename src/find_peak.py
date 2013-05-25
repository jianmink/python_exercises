#!/usr/bin/env python


import unittest
import time
# import random

def find_peak(elements):
    ''' find first peak from the 1 dimension array'''   
    start_timestamp=time.time()
    
    length=len(elements)
    
    peak=-1
    
    for i in range(length):
        big_than_right=True
        big_than_left=True
        if i+1 <length:  
            big_than_right=elements[i]>=elements[i+1]
        
        if i-1 >=0:
            big_than_left=elements[i]>=elements[i-1]
            
        if big_than_right and big_than_left:
            peak=i
            break
        
    end_timestamp=time.time()
    print "find_peak",length, "elapsed time: %f" %(end_timestamp-start_timestamp)," s"
    
    return peak


def find_peak_plus(elements):
    start_timestamp=time.time()
    peak=find_peak_plus_imp(elements, 0, len(elements)-1)
    end_timestamp=time.time()
    print "find_peak_plus",len(elements), "elapsed time: %f" %(end_timestamp-start_timestamp)," s"
    return peak


def find_peak_plus_imp(elements, start, end):
    ''' T(n) = T(n/2) + 1 '''
    
    if start > end:
        return -1;
    
    if start == end:
        return start
    
    n = (end+start)/2
    
    if n-1 >=start and elements[n] < elements[n-1]:
        return find_peak_plus_imp(elements, start, n-1)
    elif n+1<=end and elements[n] < elements[n+1]:
        return find_peak_plus_imp(elements, n+1, end)
    else:
        return n
    

class TestFindPeak(unittest.TestCase):

    def setUp(self):
        pass

    def test_find_peak(self):
        elements = [1,2,3,4,5,9,8,7,6,0]
        peak=find_peak(elements)
        self.assertTrue(elements[peak]==9)
   
    @unittest.skip("...")       
    def test_peak_is_first_element(self):
        elements = [9,2,3]
        peak=find_peak(elements)
        self.assertTrue(elements[peak]==9)
    
    @unittest.skip("...")    
    def test_peak_is_last_element(self):
        elements = [2,3,9]
        peak=find_peak(elements)
        self.assertTrue(elements[peak]==9)
        
    def test_find_peak_from_long_array(self):
        elements=[]
        for i in range(100000):
            elements.append(i)
        peak=find_peak(elements)
        self.assertEqual(99999,peak)
  
    def test_find_peak_plush(self):
        elements = [1, 2, 3, 4, 5, 9, 8, 7, 6, 0]
        peak = find_peak_plus(elements)
        self.assertEqual(elements[peak],9)
    
    def test_find_peak_plus_from_long_array(self):
        elements=[]
        for i in range(100000):
            elements.append(i)
        peak=find_peak_plus(elements)
        self.assertEqual(99999,peak)
  
        
if __name__ == '__main__':
    unittest.main()
