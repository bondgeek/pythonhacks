#!/usr/bin/env python
'''
Using generators
'''

def fib(num=1):
    '''generator for first n fibonacci series'''
    yield 1
    f, pf, n = (1, 0, 1)
    while n < num:
        yield f + pf
        f, pf, n = (f+pf, f, n+1)

