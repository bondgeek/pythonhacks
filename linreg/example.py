from scipy import linspace, polyval, polyfit, sqrt, stats, randn

import matplotlib.pyplot as plt

# Sample data creation
n = 500
t = linspace(-5, 5, n)

# parameters 
#   y = m * x + b
m, b = .8, -4
y = polyval((m, b), t)

# noise it up
yn = y + randn(n)

# linear regression with -polyfit
#   yr = mr * x + br + err

mr, br = polyfit(t, yn, 1)

yr = polyval((mr, br), t)    

# standard error
err = sqrt( sum((yr - yn)**2/(n-1)) )

# compare with scipy.stats.linregress
(m_s, b_s, r_sqrd, p_val, stderr) = stats.linregress(t, yn)

#output
plt.title("linear regression example")
plt.plot(t, y, 'g.--')
plt.plot(t, yn, 'k.')
plt.plot(t, yr, 'r.-')
plt.legend(('original', 'plus noise', 'regress'), loc='upper left')

plt.show()

print("plt.close() to close graph")
print("\npolyfit regression")
print("\n m %s b %s stderr %s" % (mr, br, err))
print("\nstats.linregress")
print("\n m %s b %s stderr %s r^2 %s pval %s" % 
      (m_s, b_s, stderr, r_sqrd, p_val))

