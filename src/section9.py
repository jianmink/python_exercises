#!/usr/bin/env python

import unittest

def filter_all_comments(filename):
    result=[]
    f = open(filename)
    for each in f:
        each=each.strip()
        if each[0]!='#':
            result.append(each)
    f.close()
    return result
            
def print_top_lines(filename,n):
    count=1
    result =[]
    f = open(filename)
    for each in f:
        if count > n:
            break
        result.append(each)
        count+=1
    f.close()
    return result

def count_lines(filename):
    with open(filename) as f:
        return sum(1 for __ in f)

def score(n):
    if n>=90:
        return 'A'
    elif n>=80:
        return 'B'
    elif n>70:
        return 'C'
    elif n>60:
        return 'D'
    else:
        return 'F'

def generate_scores_from_list(list_n):
    return [score(x) for x in list_n]

def generate_scores_from_file(filename):
    with open(filename) as f:
        for each_line in f:
            scores=[int(x) for x in each_line.strip().split(',')]
            return generate_scores_from_list(scores)

class Test_section8(unittest.TestCase):
    def test_filter(self):
        result=filter_all_comments('section8.txt')
        self.assertEqual(['hello','world!'], result)
    
    def test_print(self):
        result=print_top_lines('section8.txt',1)
        self.assertEqual(['hello\n'], result )
    
    def test_file_info(self):
        self.assertEqual(3, count_lines('section8.txt'))
        
    def test_score(self):
        self.assertEqual('B',score(80))

    def test_scores(self):
        self.assertEqual(['A','B'],generate_scores_from_list([95,85]))

    def test_scores_file(self):
        self.assertEqual(['B','A'],generate_scores_from_file('section8_scores.txt'))
        
if __name__ == '__main__':
    unittest.main()