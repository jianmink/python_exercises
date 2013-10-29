#!/usr/bin/env python

import unittest

class section10_tests(unittest.TestCase):
    
    def test_exception(self):
        f = None
        try:
            print "enter the block"
            f = open("./not_exist.file")
        except IOError,diag:
            print "exception happened"
            print diag
        else:
            print "no exception happened"
        finally:
            print "exit the block"
            if f:
                f.close()
                
if __name__ == "__main__":
    unittest.main()