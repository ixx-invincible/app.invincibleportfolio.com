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


prices = ffn.get('SPY, TLT, GLD', start='2005-01-01')

prices = prices.reset_index()
prices['portfolio'] = 100
prices['spy_rb'] = 0
prices['gld_rb'] = 0
prices['tlt_rb'] = 0
prices['portfolio_rb'] = 100


for i in prices.index:
    if i == 0:
        prices.loc[i, 'spy_rb'] = prices['spy'][0]
        prices.loc[i, 'tlt_rb'] = prices['tlt'][0]
        prices.loc[i, 'gld_rb'] = prices['gld'][0]
        prices.loc[i, 'portfolio_rb'] = 100
        
    else:
        prices.loc[i, 'portfolio'] = prices['portfolio_rb'][i-1] * ((prices['spy'][i] / prices['spy_rb'][i-1] + prices['tlt'][i] / prices['tlt_rb'][i-1] + prices['gld'][i] / prices['gld_rb'][i-1]) / 3)
        
        if(i != len(prices)-1 and prices.Date[i].month % 3 == 0 and prices.Date[i+1].month % 3 == 1):
            prices.loc[i, 'spy_rb'] = prices['spy'][i]
            prices.loc[i, 'tlt_rb'] = prices['tlt'][i]
            prices.loc[i, 'gld_rb'] = prices['gld'][i]
            prices.loc[i, 'portfolio_rb'] = prices['portfolio'][i]
        else:
            prices.loc[i, 'spy_rb'] = prices.loc[i-1, 'spy_rb']
            prices.loc[i, 'tlt_rb'] = prices.loc[i-1, 'tlt_rb']
            prices.loc[i, 'gld_rb'] = prices.loc[i-1, 'gld_rb']
            prices.loc[i, 'portfolio_rb'] = prices.loc[i-1, 'portfolio_rb']
            

weekday = datetime.today().weekday()


prices.to_csv('out/invincible_portfolio_' + str(weekday) + '.csv')
prices.to_csv('quote/invincible_portfolio.csv')
prices.to_json('quote/invincible_portfolio.json', orient='index')
prices.tail(1).to_json('quote/invincible_portfolio_latest.json', orient='records')


prices.set_index('Date', inplace=True)

returns = prices.loc[:, ['spy', 'gld', 'tlt', 'portfolio']].to_returns().dropna()


#print(returns.corr().as_format('.2f'))

perf = prices.loc[:, ['spy', 'gld', 'tlt', 'portfolio']].calc_stats()

perf['gld'].stats.to_csv('out/gld_stats_' + str(weekday) + '.csv')
perf['spy'].stats.to_csv('out/spy_stats_' + str(weekday) + '.csv')
perf['tlt'].stats.to_csv('out/tlt_stats_' + str(weekday) + '.csv')
perf['portfolio'].stats.to_csv('out/invincible_portfolio_stats_' + str(weekday) + '.csv')

perf['gld'].stats.to_json('quote/gld_stats.json')
perf['spy'].stats.to_json('quote/spy_stats.json')
perf['tlt'].stats.to_json('quote/tlt_stats.json')
perf['portfolio'].stats.to_json('quote/invincible_portfolio_stats.json')


                

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


plt.savefig('out/invincible_portfolio_' + str(weekday) + '.png')
plt.close()


perf['portfolio'].return_table.to_csv('out/invincible_portfolio_monthly_returns_' + str(weekday) + '.csv')
perf['gld'].return_table.to_csv('out/gld_monthly_returns_' + str(weekday) + '.csv')
perf['spy'].return_table.to_csv('out/spy_monthly_returns_' + str(weekday) + '.csv')
perf['tlt'].return_table.to_csv('out/tlt_monthly_returns_' + str(weekday) + '.csv')

perf['portfolio'].return_table.to_json('quote/invincible_portfolio_monthly_returns.json', orient='index')
perf['gld'].return_table.to_json('quote/gld.json', orient='index')
perf['spy'].return_table.to_json('quote/spy.json', orient='index')
perf['tlt'].return_table.to_json('quote/tlt.json', orient='index')