import matplotlib.pyplot as plt
import numpy as np

from scipy.optimize import leastsq

# Parametric function: 'v' is the parameter vector, 'x' the independent varible
fp = lambda v, x: v[0]/(x**v[1])*np.sin(v[2]*x)


# Noisy function (used to generate data to fit)
v_real = [1.5, 0.1, 2.]
fn = lambda x: fp(v_real, x)

# Error function
e = lambda v, x, y: fp(v, x) - y

# Generate noisy data to fit
n = 30
xmin = .1
xmax = 5
x = np.linspace(xmin, xmax, n)
y = fn(x) + np.random.rand(len(x))*.2*(fn(x).max()-fn(x).min())


# initial parameter values
v0 = [3., 1, 4.]

# Fit
v, success = leastsq(e, v0, args=(x, y), maxfev=10000)

## Plot
def plot_fit():
    print 'Estimated parameters: ', v
    print 'Real parameters: ', v_real

    X = np.linspace(xmin, xmax, n*5)
    plt.plot(x, y, 'ro', X, fp(v, X))

plot_fit()
plt.show()

