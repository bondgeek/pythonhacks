from scipy import linspace, polyval, polyfit, sqrt, stats, randn

import matplotlib.pyplot as plt

# Sample data creation
n = 50
t = linspace(-5, 5, n)

# parameters 
#   y = m * x + b
m, b = .8, -4
y = polyval((m, b), t)

# noise it up
yn = y + randn(n)

# linear regression with -polyfit
#   yr = mr * x + b + err
mr, br = polyfit(t, yn, 1)
yr = polyval((mr, br), t)    

# standard error
err = sqrt( sum((yr - yn)**2/(n-1)) )

#output

plt.title("linear regression example")
plt.plot(t, y, 'g.--')
plt.plot(t, yn, 'k.')
plt.plot(t, yr, 'r.-')
plt.legend(('original', 'plus noise', 'regress'))

plt.show()
