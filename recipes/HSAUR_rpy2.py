#!/usr/bin/env python
'''
Working through examples from Everitt & Hothorn's Handbook of Statistical Analysis in R (HSAUR)
using rpy2, and other stuff...
'''
import numpy as np
import rpy2
import rpy2.robjects as robjects

print("rpy2 version: %s" % rpy2.__version__)

RWorkSpace = robjects.globalEnv

r = robjects.r

r.library("HSAUR")

r.data("Forbes2000", package="HSAUR")

dimforbes = r.dim(r.Forbes2000)
print dimforbes

#different ways of accessing object
r.dim(r.Forbes2000)[0]
# 2000

r.dim(r['Forbes2000'])[1]
# 8

print("\nWho was number 1? (emphasis on 'was')")
for n, name in enumerate(r.Forbes2000.colnames()):
    print("%s: %s" %  (name, r.Forbes2000[n][0]))

print("\nNow to summarize sales data")
sales_sum = r.summary(r.Forbes2000[4])

for v, colname in enumerate(sales_sum.names):
    print("%s: %f" % (colname, sales_sum[v]))

print("...or, \n%s\n" % sales_sum)

r.table('Forbes2000$assets > 1000')


# Construct a data.frame
RIntVector = robjects.IntVector
RStrVector = robjects.StrVector

v_int = RIntVector(range(10)) 
v_alphas = RStrVector([x for x in r('letters')][-10:])

mydata = {'values': v_int, 'letters': v_alphas}

dataf = r['data.frame'](**mydata)
print("A dataframe")
print(dataf)

#loading source file that contains function definitions
r.source("/Users/bartmosley/sandbox/RMySQLExamples/classexamples.R")
c_obj = r.cartesianxy(3, 5)
d_origin = r.fromorigin(c_obj)

print d_origin[0]

