#!/usr/bin/env python

import unittest
import random


def get_rand_num():
    return random.randint(0,5)

def loops(f, t, i):
    x_list = []
    for x in range(f, t+1, i):
        x_list.append(x)
    return x_list

def get_factors(p):
    return [i for i in range(1,p+1) if p%i==0]

def isprime(p):
    return p==2 or len(get_factors(p))==2

def get_prime_factors(p):
    prime_factors=[]
    for x in get_factors(p):
        while isprime(x) and not p%x:
            prime_factors.append(x)
            p=p/x
    return prime_factors

def isperfect(p):
    return p==sum(x for x in get_factors(p) if x!=p)
  
class exercise_section8(unittest.TestCase):
    @unittest.skip("traditional for loop")
    def test_iterator(self):
        list_names=['mike', 'jerry', 'snoopy']
        for name in list_names:
            print name
            
    def test_iterator_2(self):
        list_names=['mike', 'jerry', 'snoopy']
        fetch = iter(list_names)
        while True:
            try:
                name = fetch.next()
            except StopIteration:
                break;
            print name
    
    @unittest.skip("not always pass")
    def test_iterator_sentinel(self):
        for i in iter(get_rand_num, 0):
            pass
        self.assertNotEqual(0,i)
        
    def test_list_comp(self):
        f = open('../README.md')
        self.assertEqual(3, len([word for each_line in f for word in each_line.split()]))
        f.close()
        
    def test_generator_comp(self):
#         f = open('../README.md')
#         self.assertEqual(3, sum(1 for each_line in f for __ in each_line.split()))
#         f.close()
        self.assertEqual(3, sum(1 for each_line in open('../README.md') for __ in each_line.split()))
    
    def test_loops(self):
        self.assertEqual([2,6,10,14,18,22,26], loops(2,26,4))
        
    def test_7_isprime(self):
        self.assertTrue(isprime(7)) 
    
    def test_14_has_4_factors(self):
        self.assertEqual([1,2,7,14],get_factors(14))

    def test_20_has_prime_factors_2_2_5(self):
        self.assertEqual([2,2,5], get_prime_factors(20))
        
    def test_6_is_perfect_number(self):
        self.assertTrue(isperfect(6))
               
if __name__=='__main__':
    unittest.main()
