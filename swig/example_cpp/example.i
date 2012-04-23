// example.i
// taken from http://wiki.laptop.org/go/Extending_Python_with_C%2B%2B

%module example

%{
#include "example.h"
%}

%include "example.h"