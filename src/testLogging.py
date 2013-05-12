#!/usr/bin/env python

import logging 
import logging.config


import unittest


class TestLogger(unittest.TestCase):

    def setUp(self):
        pass

    def test_dummy(self):
        self.assertEqual(1, 1)
        
        
    def test_simple_logger(self): 
        logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.DEBUG)
        logging.info(" simple logger.info")
        
        
    def test_logger(self):
        # create logger
        logger = logging.getLogger('simple_example')
        logger.setLevel(logging.DEBUG)
        
        # create console handler and set level to debug
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        
        # create formatter
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        
        # add formatter to ch
        ch.setFormatter(formatter)
        
        # add ch to logger
        logger.addHandler(ch)
        
        # 'application' code
        logger.debug('debug message')
        logger.info('info message')
        logger.warn('warn message')
        logger.error('error message')
        logger.critical('critical message')



    def test_logger_file(self):
        logging.config.fileConfig('logging.conf')

        # create logger
        logger = logging.getLogger('logger_file')
        
        # 'application' code
        logger.debug('debug message')
        logger.info('info message')
        logger.warn('warn message')
        logger.error('error message')
        logger.critical('critical message')

if __name__ == "__main__":
    unittest.main()

    