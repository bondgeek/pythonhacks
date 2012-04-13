# demo.pyx

from libc.math cimport sin

cdef double f(double x):
    return sin(x*x)

def myfunc(x):
    return f(x)

def fib(n):
    """Print the Fibonacci series up to n"""
    a, b = 0, 1
    while b < n:
        print b,
        a, b = b, a + b

    
