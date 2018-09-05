import numpy as np
import matplotlib.pyplot as plt
import scipy
from scipy.stats import powerlaw

requests = np.random.exponential(scale=1.0, size=None)
f = open('powerlaw1.csv', 'w')

a = [1]


for i in a:
    r = scipy.stats.powerlaw.rvs(i, loc = 0, scale = 1000, size = 20000)
    print np.absolute(r)
    plt.plot(np.sort(np.absolute(r)), range(0,20000))


r = scipy.stats.powerlaw.rvs(10, loc = 0, scale = 1000, size = 20000)

for i in r:
    f.write(str(int(i)) + "\n")


