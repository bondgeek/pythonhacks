'''

Examples based on E.O. Thorp[1997],
"The Kelly Criterion in Blackjack, Sports Betting and The Stock Market"

'''

#from numpy import diag, matrix, inf
import numpy as np
import scipy.optimize as scio
import openopt as oo

# single security with borrowing / lending at risk free rate, r
# the exponential growth rate of wealth is given by
#
# g(f) = Exp[ ln(V/V0) ]
#      = r + f(m-r) - s**2 f**2 / 2.
#


variance = 0.007876323
m = .05312
r = .0152
mr = (m-r)  #excess return
print("\n\nrisk-free: %s\nsecurity drift: %s\nvariance: %s" %
      (r, m, variance))

print("\nSolve with fmin")
# we want the maximimum, so take the negative for fmin
obj_fun = lambda f, mr, s: -(f*mr - (s*f*f/2.))

f_opt = scio.fmin(obj_fun, [.5], args=(mr, variance), disp=False)

print("\nCompare to known solution:\n closed-form: %s  fmin: %s" %
      (mr / variance, f_opt[0]))

print("\nSolve with OpenOpt.QP ")
H = np.diag([variance])
f = [-mr]
r = oo.QP(H, f).solve('qlcp')

print("\nQP solution: %s " % r.xf[0])

print("\n\nPortfolio Example")
covar = np.matrix('0.007876324	0.005286073; 0.005286073	0.003838901')
m1 = .05312
m2 = .048515
r = .0152
f = [-(m1-r), -(m2-r)]
r2 = oo.QP(covar, f).solve('qlcp')

print("\nPortfolio solution:  \nsec1 = %s sec2 = %s " % (r2.xf[0], r2.xf[1]))
