#!/usr/bin/env python
'''
Use regex to tokenize a string expression. 

adapted from:
http://effbot.org/zone/xml-scanner.htm
'''
import re

reg_token = re.compile(r"""
    \s*                 #skip whitespace
    ([0-9\.]+|          #one or more digits or '.'
                         aka floats or ints
    \w+|                #words
    [+\-*/!^%&|]{1,2}|  #operators
    .)                  #any character except newline
    """, 
    re.VERBOSE)

def tokenize(expr):
    '''
    Returns a list of tokens for an expression string.
    Allows operators +-*/!^%&| 
    Treats doubled operator e.g., **, ++ as single token
    '''
    def v_token(obj):
        try:
            if '.' in obj:
                return float(obj)
            else:
                return int(obj)
        except:
            return obj
    
    return [v_token(tkn.group()) for tkn 
                        in reg_token.finditer(expr)]

expr = ["(3+7)*90",            # basic
        "(3+7.1)*90",   	   # has floats
        "(3+7.1)*90*alpha",    # has variables
        "(3+7.1)*90*alpha, g", # invalid
        "(5.0 - 3.2)/6*9",
        "b = 2 + a*10",
        "x = \n x**2",
        "i++",
        ""
        ]

for exp in expr:
    tkns = tokenize(exp)
    print("\nExpression: %s\nTokens: %s " % (exp, tkns)) 

    
    
    #for t in tokenize(exp):
        #our function returns legit tokens
        #print("%10s : %s" % (t, type(t)))

