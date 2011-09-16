import numpy as np

from alprion.db.marketdb import Timeseries

from bgpy.QL import toPyDate

import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

sdata = Timeseries.by_ticker("USSW", "10Y", begin=20110101, mode='l')

fig = plt.figure()
ax = fig.add_subplot(121)
ax.plot([dt for dt, v in sdata], [v for dt, v in sdata], 'b-')
ax.set_title('first chart!')
fig.autofmt_xdate()


N = len(sdata)
ind = np.arange(N)

def format_date(x, pos=None):
    ind = np.clip(int(x+0.5), 0, N-1)
    return sdata[ind][0].strftime('%Y-%m-%d')

ax2 = fig.add_subplot(122)
ax2.plot(ind, [v for dt, v in sdata], 'b-', label='10Y')
ax2.xaxis.set_major_formatter(ticker.FuncFormatter(format_date))
ax2.set_title('chart 2')
ax2.set_xlabel('xlabel')
ax2.set_ylabel('ylabel')
ax2.legend(loc=0, frameon=False, title='legend')
ax2.grid(True)

fig.autofmt_xdate()
