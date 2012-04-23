# demo.pyx

from libc.math cimport sin

cdef double sin_c(double x):
    return sin(x)

def myfunc(x):
    return sin_c(x)

def fib(n):
    """Print the Fibonacci series up to n"""
    a, b = 0, 1
    while b < n:
        print b,
        a, b = b, a + b

    
