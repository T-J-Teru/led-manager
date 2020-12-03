#! /usr/bin/python3

import time
import sys

print ("Welcome to 'test1', arguments are: ", str(sys.argv))

count = 0
while True:
    print ("In test1 (%d)" % count)
    count += 1
    time.sleep (5)
