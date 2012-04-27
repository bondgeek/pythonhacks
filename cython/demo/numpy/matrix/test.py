import numpy as np
import matrix

print("\nStart")
a = np.array([1., 2., 3., -8])

print("initializing")
x = matrix.summer(a)

print("size: %s" % x.size)
print("items:\n%s" % x.items)
