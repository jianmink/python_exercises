#!/bin/env python
import time
import sys

i=0
for i in range(10):
    print "\r %d" %(i),
    sys.stdout.flush()
    time.sleep(1)

