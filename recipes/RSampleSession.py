import matplotlib.pyplot as plt
import rpy2.robjects as robjects

r = robjects.r           # We will reference the R environment 
                         # via the Python name 'r'
                         
r('x <- rnorm(50)')      # creates a variable x in R environment 
x = r.rnorm(50)          # creates an RVector, x,  in Python namespace

y = r.rnorm(x)           # This uses the Python x to create a Python y
y2 = r.rnorm(r.x)        # This uses the R x to create a Python y
r('y <- rnorm(x)')       # This uses the R x to create an R y

r('f <- function(r) {2 * pi * r}')  # creates a function in R

circ = r.f(3)[0]            # returns 18.85


rdf = r['data.frame']
robj = lambda x: [obj for obj in x]

