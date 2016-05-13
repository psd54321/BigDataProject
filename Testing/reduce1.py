#!/usr/bin/env python
import sys

def reducer():
    for line in sys.stdin:
        print '%s' %(line)

if __name__=='__main__':
    reducer()
