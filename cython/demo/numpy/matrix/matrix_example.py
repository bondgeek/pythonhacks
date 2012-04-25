from numpy import array
from matrix import mysum, mysum2, mysum3

print("\nStart")
a = array([1., 2., 3., -8])
print("\nArray: %s" % a)
print(">>mysum: %s" % mysum(a))
print(">>Array with new first element \n(changed in mysum): %s" % a)

print("\nTest Two, python list")
a = [1., 2., 3., -8]
print("\nArray: %s" % a)
print(">>mysum: %s" % mysum2(a))
print(">>First element not changed (different scope): %s" % a)

print("\nTest Two(a), python list")
a = [1., 2., 3., -8]
print("\nArray: %s" % a)
print(">>mysum: %s" % mysum3(a))
print(">>First element: %s" % a)


print("\nTest Three")
a = array([[1., 2., 3., -8],
           [2., 4., 9., -88]])
print("\nArray: %s" % a)
print(">>mysum: %s" % mysum(a))
print(">>Array with new first element \n(changed in mysum): %s" % a)
