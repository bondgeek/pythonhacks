import scipy as sp
import numpy as np

n = 100
c, ar = 0., .9

err = np.random.randn(n)

y = []
for j in range(n):
    yj = c/(1.-ar) + sum([ar**i * err[j-i] for i in range(j+1)])
    y.append(yj)

