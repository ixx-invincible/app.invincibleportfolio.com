# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 10:22:27 2020

@author: TerryLaw
"""

from datetime import datetime

import ffn
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import matplotlib.gridspec as gridspec


prices = ffn.get('SPY, TLT, GLD', start='2005-01-01')

prices = prices.reset_index()
prices['portfolio'] = 100
prices['spy_shares'] = 0
prices['gld_shares'] = 0
prices['tlt_shares'] = 0


for i in prices.index:
    if i == 0:
        prices.loc[i, 'spy_shares'] = prices['portfolio'][i] / 3 / prices['spy'][i]
        prices.loc[i, 'tlt_shares'] = prices['portfolio'][i] / 3 / prices['tlt'][i]
        prices.loc[i, 'gld_shares'] = prices['portfolio'][i] / 3 / prices['gld'][i]
        
    else:
        prices.loc[i, 'portfolio'] = prices['spy_shares'][i-1] * prices['spy'][i] + prices['gld_shares'][i-1] * prices['gld'][i] + prices['tlt_shares'][i-1] * prices['tlt'][i]
        
        if(prices.Date[i].month % 3 == 0 and prices.Date[i+1].month % 3 == 1):
            prices.loc[i, 'spy_shares'] = prices['portfolio'][i] / 3 / prices['spy'][i]
            prices.loc[i, 'tlt_shares'] = prices['portfolio'][i] / 3 / prices['tlt'][i]
            prices.loc[i, 'gld_shares'] = prices['portfolio'][i] / 3 / prices['gld'][i]
        else:
            prices.loc[i, 'spy_shares'] = prices.loc[i-1, 'spy_shares']
            prices.loc[i, 'tlt_shares'] = prices.loc[i-1, 'tlt_shares']
            prices.loc[i, 'gld_shares'] = prices.loc[i-1, 'gld_shares']
            
            

prices.to_excel('out/permanent_portfolio.xlsx')


prices.set_index('Date', inplace=True)

returns = prices.loc[:, ['spy', 'gld', 'tlt', 'portfolio']].to_returns().dropna()


#print(returns.corr().as_format('.2f'))

perf = prices.loc[:, ['spy', 'gld', 'tlt', 'portfolio']].calc_stats()
#print(perf.display())



fig = plt.figure(constrained_layout=True, figsize=(10, 5))
spec = fig.add_gridspec(ncols=1, nrows=2, height_ratios=[3, 1])

ax1 = fig.add_subplot(spec[0, 0])
# ax1.plot(df['gld_twr'], label='GLD', linewidth=1)
# ax1.plot(df['spy_twr'], label='SPY', linewidth=1)
# ax1.plot(df['tlt_twr'], label='TLT', linewidth=1)
ax1.plot(prices['portfolio'], label='Portfolio', linewidth=2)
ax1.legend(loc='upper left')
# ax1.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax1.grid(True)

ax2 = fig.add_subplot(spec[1, 0])
ax2.plot(perf['portfolio'].prices.to_drawdown_series(), label='Drawdown')
ax2.legend(loc='lower left')
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax2.grid(True)


plt.savefig('out/permanent_portfolio.png')
plt.close()


perf['portfolio'].return_table.to_excel('out/permanent_portfolio_monthly_returns.xlsx')