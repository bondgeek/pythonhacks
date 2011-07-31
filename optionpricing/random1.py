import numpy as np

def gaussian_by_summation():
    
    return sum([np.random.random() for j in range(12)]) - 6.0

def gaussianBoxMuller():
    
    sizeSquared = 1.
    while sizeSquared >= 1.0:
        x, y = np.random.random(2)
        sizeSquared = x*x + y*y
        
    return x*np.sqrt(-2.*np.log(sizeSquared)/sizeSquared)

