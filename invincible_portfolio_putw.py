# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 10:22:27 2020

@author: TerryLaw
"""

from datetime import datetime
import json

import ffn
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import matplotlib.gridspec as gridspec


prices = ffn.get('GLD, PUTW, TLT', start='2005-01-01')

prices = prices.reset_index()
prices['portfolio'] = 100
prices['gld_rb'] = 0
prices['putw_rb'] = 0
prices['tlt_rb'] = 0
prices['portfolio_rb'] = 100

symbols = ['gld', 'putw', 'tlt']


for i in prices.index:
    if i == 0:
        for symbol in symbols:
            prices.loc[i, symbol + '_rb'] = prices[symbol][0]

        prices.loc[i, 'portfolio_rb'] = 100
        
    else:
        pct_change = (prices['putw'][i] / prices['putw_rb'][i-1]) -1
        pct_change += ((prices['tlt'][i] / prices['tlt_rb'][i-1]) -1) * 0.3
        pct_change += ((prices['gld'][i] / prices['gld_rb'][i-1]) -1) * 0.3
        
        prices.loc[i, 'portfolio'] = prices['portfolio_rb'][i-1] * (1+ pct_change)
        
        if(i != len(prices)-1 and prices.Date[i].month % 3 == 0 and prices.Date[i+1].month % 3 == 1):
            for symbol in symbols:
                prices.loc[i, symbol + '_rb'] = prices[symbol][i]

            prices.loc[i, 'portfolio_rb'] = prices['portfolio'][i]
        else:
            for symbol in symbols:
                prices.loc[i, symbol + '_rb'] = prices[symbol + '_rb'][i-1]

            prices.loc[i, 'portfolio_rb'] = prices['portfolio_rb'][i-1]




weekday = datetime.today().weekday()


prices.to_csv('out/invincible_portfolio_putw_' + str(weekday) + '.csv')
prices.to_csv('quote/invincible_portfolio_putw.csv')
prices.to_json('quote/invincible_portfolio_putw.json', orient='index')
prices.tail(2).to_json('quote/invincible_portfolio_putw_latest.json', orient='records')


prices.set_index('Date', inplace=True)

# returns = prices.loc[:, ['spy', 'gld', 'tlt', 'portfolio']].to_returns().dropna()
# print(returns.corr().as_format('.2f'))

perf = prices.loc[:, ['gld', 'putw', 'tlt', 'portfolio']].calc_stats()

                

fig = plt.figure(constrained_layout=True, figsize=(10, 5))
spec = fig.add_gridspec(ncols=1, nrows=2, height_ratios=[3, 1])

ax1 = fig.add_subplot(spec[0, 0])
ax1.plot(prices['portfolio'], label='Portfolio', linewidth=2)
ax1.legend(loc='upper left')
ax1.grid(True)

ax2 = fig.add_subplot(spec[1, 0])
ax2.plot(perf['portfolio'].prices.to_drawdown_series(), label='Drawdown')
ax2.legend(loc='lower left')
ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
ax2.grid(True)


plt.savefig('out/invincible_portfolio_putw_' + str(weekday) + '.png')
plt.close()



for symbol in symbols:
    perf[symbol].stats.to_csv('out/' + symbol + '_stats_' + str(weekday) + '.csv')
    perf[symbol].stats.to_json('quote/' + symbol + '_stats.json')
    perf[symbol].return_table.to_csv('out/' + symbol + '_monthly_returns_' + str(weekday) + '.csv')
    perf[symbol].return_table.to_json('quote/' + symbol + '.json', orient='index')


perf['portfolio'].stats.to_csv('out/invincible_portfolio_putw_stats_' + str(weekday) + '.csv')
perf['portfolio'].stats.to_json('quote/invincible_portfolio_putw_stats.json')
perf['portfolio'].return_table.to_csv('out/invincible_portfolio_putw_monthly_returns_' + str(weekday) + '.csv')
perf['portfolio'].return_table.to_json('quote/invincible_portfolio_putw_monthly_returns.json', orient='index')
