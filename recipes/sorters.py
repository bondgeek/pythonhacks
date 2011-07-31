import operator
from random import random

def sortby1(nlist, n):
    nlist[:] = [(x[n], x) for x in nlist]
    nlist.sort()
    nlist[:] = [val for (key, val) in nlist]
 
def sortby2(nlist ,n):  
    nlist.sort(key=operator.itemgetter(n))
 
def sortby3(nlist, n):
    def __sort_by(n):
        def _sort_by(a, b):
            return cmp(a[n], b[n])
        return _sort_by
    nlist.sort(__sort_by(n))
 
# Same as above but much simpler using lambda
def sortby4(nlist, n):
    nlist.sort(lambda x,y:cmp(x[n], y[n]))

# Home-brewed itemgetter
def sortby5(nlist, n):
    nlist.sort(key=lambda x:x[n])


from bondgeek.utils.devutils.timings import fcompare

testlist1 = [(random(), random()) for i in range(10000)]

print("Sort by first item")
arg1 = (testlist1,0)
flist = [sortby1,sortby2,sortby3,sortby4,sortby5]
fcompare(flist,10,arg1)

print("Sort by second item")
arg2 = (testlist1,1)
fcompare(flist,10,arg2)

'''
In [80]: run sandbox/sorters
Sort by first item
sortby2:   0.2 secs
sortby5:   0.44 secs
sortby4:   0.67 secs
sortby3:   0.69 secs
sortby1:   0.87 secs
Sort by second item
sortby2:   0.21 secs
sortby5:   0.46 secs
sortby4:   0.72 secs
sortby3:   0.75 secs
sortby1:   0.89 secs
'''

