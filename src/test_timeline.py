#!/usr/bin/env python

import unittest
from timeline import * 


a = background_color_set[1]
b = background_color_set[0]

class Test_time_list(unittest.TestCase):

    def test_basic_format(self):
        time_a = ((2.1, 2.5),) 
        expect = [0., 1., 2., 2.1, 2.5, 3.]
        self.assertEqual(expect,
                        create_colorbar((time_a,), ['b', 'r'], 3)[0])

    def test_1_taskset(self):
        time_a = ((2., 2.7),)
        expect=([0., 1., 2., 2.7, 3.],
                [b,a,'g',b])
        self.assertEqual(expect, create_colorbar((time_a,), color_map=('g','y'), frames=3))

    def test_2_taskset_no_overlap_format_1(self):
        time_a = ((0., .7),)
        time_b = ((3.1,3.4),)
        expect = ([0.,.7, 1., 2., 3., 3.1,3.4, 4.],
                  ['g',b,a,b,a,'y',a])
        self.assertEqual(expect,
                         create_colorbar((time_a, time_b), color_map=('g','y'),frames=4))
    
    def test_2_taskset_no_overlap_format_2(self):
        time_a = ((0., .7),)
        time_b = ((0.7, 1.),)
        expect = ([0.,.7, 1.],
                  ['g','y'])
        
        self.assertEqual(expect,
                         create_colorbar((time_a, time_b), color_map=('g','y'),frames=1))

     
    def test_basic_overlap_format_1(self):
        time_a = ((0., .7),)
        time_b = ((.1, .4),)
        expect = ([0., .1, .4, .7, 1.],
                  ['g',overlap_color,'g',b])
        self.assertEqual(expect,
                         create_colorbar((time_a, time_b), color_map=('g','y'),frames=1))
      

    def test_basic_overlap_format_2(self):
        time_a = ((0., .3),)
        time_b = ((.1, .8),)
        expect = ([0., .1, .3, .8, 1.],
                  ['g',overlap_color,'y',b])
        self.assertEqual(expect,
                         create_colorbar((time_a, time_b), color_map=('g','y'),frames=1))
        
    def test_basic_overlap_format_3(self):
        time_a = ((.1, .8),)
        time_b = ((0., .3),)
        expect = ([0., .1, .3, .8, 1.],
                  ['y',overlap_color,'g',b])
        
        result=create_colorbar((time_a, time_b), 
                                         color_map=('g','y'),frames=1)
        
        for i in range (len(expect[0])):
            self.assertAlmostEqual(expect[0][i],result[0][i])
        
        self.assertSequenceEqual(expect[1],result[1])
        

    def test_basic_overlap_format_4(self):
        time_a = ((.1, .4),)
        time_b = ((0., .7),) 

        expect_b=[0,0.1,0.4,0.7,1.]
        expect_c=['y',overlap_color,'y',b]
        self.assertEqual(expect_b,
                        create_colorbar((time_a, time_b), ['g', 'y'], 1)[0])
        self.assertEqual(expect_c,
                        create_colorbar((time_a, time_b), ['g', 'y'], 1)[1])
        

    def test_overtime_format_1(self):
        time_a = ((0., 1.1),) 
        expect = ['g', 'g', a]
        self.assertEqual(expect,
                        create_colorbar((time_a,), ['g', 'y'], 2)[1])

    def test_overtime_format_2(self):
        time_a = ((.1, 1.2),) 
        expect = [b, 'b', 'b', a]
        self.assertEqual(expect, create_colorbar((time_a,), ['b', 'g'], 2)[1])

    def test_overtime_format_3(self):
        time_a = ((0. , 1.),) 
        expect = ([0.,1.,2.],
                  ['g', a])
        self.assertEqual(expect,
                        create_colorbar((time_a,), ['g', 'y'], 2))

    def test_overtime_and_overlap_format_1(self):
        time_a = ((0., 1.3),) 
        time_b = ((1.1, 1.6),)
        expect = [0., 1., 1.1, 1.3, 1.6, 2.]
        self.assertEqual(expect,
                        create_colorbar((time_a, time_b), ['b', 'r'], 2)[0])

    def test_overtime_and_overlap_format_2(self):
        time_a = ((0., .7), (4.0, 4.5)) 
        time_b = ((3.1, 4.4),)

        expect = ['b', b, a, b, a, 'g', overlap_color, 'b',b]
        self.assertEqual(expect,
                        create_colorbar((time_a,time_b), ['b', 'g'], 5)[1])
        

if __name__ == '__main__':
    #import sys;sys.argv = ['', '']
    unittest.main()

