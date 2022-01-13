# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 10:22:27 2020

@author: TerryLaw
"""

from datetime import datetime, timezone, timedelta

import ffn
import matplotlib.pyplot as plt
import matplotlib.dates as mdates
import matplotlib.ticker as mtick
import matplotlib.gridspec as gridspec
import yfinance as yfin
yfin.pdr_override()


def calculate_invincible_portfolio():
    if datetime.now(timezone.utc).astimezone().tzinfo.utcoffset(None)==timedelta(seconds=28800):
        prices = ffn.get('GLD, SPY, TLT', start='2005-01-01', end=datetime.today())
    else:
        prices = ffn.get('GLD, SPY, TLT', start='2004-12-31', end=datetime.today())
    
    prices = prices.reset_index()
    prices['portfolio'] = 100
    prices['gld_rb'] = 0
    prices['spy_rb'] = 0
    prices['tlt_rb'] = 0
    prices['portfolio_rb'] = 100

    symbols = ['gld', 'spy', 'tlt']

    for i in prices.index:
        if i == 0:
            for symbol in symbols:
                prices.loc[i, symbol + '_rb'] = prices[symbol][0]

            prices.loc[i, 'portfolio_rb'] = 100
            
        else:
            prices.loc[i, 'portfolio'] = prices['portfolio_rb'][i-1] * ((prices['spy'][i] / prices['spy_rb'][i-1] + prices['tlt'][i] / prices['tlt_rb'][i-1] + prices['gld'][i] / prices['gld_rb'][i-1]) / 3)
            
            # Quarter-end rebalancing
            if(i != len(prices)-1 and prices.Date[i].month % 3 == 0 and prices.Date[i+1].month % 3 == 1):
                for symbol in symbols:
                    prices.loc[i, symbol + '_rb'] = prices[symbol][i]

                prices.loc[i, 'portfolio_rb'] = prices['portfolio'][i]
            else:
                for symbol in symbols:
                    prices.loc[i, symbol + '_rb'] = prices[symbol + '_rb'][i-1]

                prices.loc[i, 'portfolio_rb'] = prices['portfolio_rb'][i-1]

    
    symbols.append('portfolio')
    export(prices, 'invincible_portfolio', symbols)


def calculate_invincible_portfolio2():
    if datetime.now(timezone.utc).astimezone().tzinfo.utcoffset(None)==timedelta(seconds=28800):
        prices = ffn.get('TQQQ, UPRO, TMF, GLD', start='2010-01-01', end=datetime.today())
    else:
        prices = ffn.get('TQQQ, UPRO, TMF, GLD', start='2009-12-31', end=datetime.today())
    
    prices = prices.reset_index()
    prices['portfolio'] = 100
    prices['tqqq_rb'] = 0
    prices['upro_rb'] = 0
    prices['tmf_rb'] = 0
    prices['gld_rb'] = 0
    prices['portfolio_rb'] = 100

    symbols = ['tqqq', 'upro', 'tmf', 'gld']

    for i in prices.index:
        if i == 0:
            for symbol in symbols:
                prices.loc[i, symbol + '_rb'] = prices[symbol][0]

            prices.loc[i, 'portfolio_rb'] = 100
            
        else:
            prices.loc[i, 'portfolio'] = prices['portfolio_rb'][i-1] * (
                    (prices['tqqq'][i] / prices['tqqq_rb'][i-1]) * 0.22 +
                    (prices['upro'][i] / prices['upro_rb'][i-1]) * 0.22 +
                    (prices['tmf'][i] / prices['tmf_rb'][i-1]) * 0.36 +
                    (prices['gld'][i] / prices['gld_rb'][i-1]) * 0.20
                )
            
            # Quarter-end rebalancing
            if(i != len(prices)-1 and prices.Date[i].month % 3 == 0 and prices.Date[i+1].month % 3 == 1):
                for symbol in symbols:
                    prices.loc[i, symbol + '_rb'] = prices[symbol][i]

                prices.loc[i, 'portfolio_rb'] = prices['portfolio'][i]
            else:
                for symbol in symbols:
                    prices.loc[i, symbol + '_rb'] = prices[symbol + '_rb'][i-1]

                prices.loc[i, 'portfolio_rb'] = prices['portfolio_rb'][i-1]

    
    symbols.append('portfolio')
    export(prices, 'invincible_portfolio_tqqq22_upro22_tmf36_gld20', symbols)



def calculate_invincible_portfolio3():
    if datetime.now(timezone.utc).astimezone().tzinfo.utcoffset(None)==timedelta(seconds=28800):
        prices = ffn.get('TQQQ, TLT', start='2010-01-01', end=datetime.today())
    else:
        prices = ffn.get('TQQQ, TLT', start='2009-12-31', end=datetime.today())
    
    prices = prices.reset_index()
    prices['portfolio'] = 100
    prices['tqqq_rb'] = 0
    prices['tlt_rb'] = 0
    prices['portfolio_rb'] = 100

    symbols = ['tqqq', 'tlt']

    for i in prices.index:
        if i == 0:
            for symbol in symbols:
                prices.loc[i, symbol + '_rb'] = prices[symbol][0]

            prices.loc[i, 'portfolio_rb'] = 100
            
        else:
            prices.loc[i, 'portfolio'] = prices['portfolio_rb'][i-1] * ((prices['tqqq'][i] / prices['tqqq_rb'][i-1]) * 0.3 + (prices['tlt'][i] / prices['tlt_rb'][i-1]) * 0.7)
            
            # Quarter-end rebalancing
            if(i != len(prices)-1 and prices.Date[i].month % 3 == 0 and prices.Date[i+1].month % 3 == 1):
                for symbol in symbols:
                    prices.loc[i, symbol + '_rb'] = prices[symbol][i]

                prices.loc[i, 'portfolio_rb'] = prices['portfolio'][i]
            else:
                for symbol in symbols:
                    prices.loc[i, symbol + '_rb'] = prices[symbol + '_rb'][i-1]

                prices.loc[i, 'portfolio_rb'] = prices['portfolio_rb'][i-1]

    
    symbols.append('portfolio')
    export(prices, 'invincible_portfolio_tqqq30_tlt70', symbols)


def calculate_invincible_portfolio4():
    if datetime.now(timezone.utc).astimezone().tzinfo.utcoffset(None)==timedelta(seconds=28800):
        prices = ffn.get('TQQQ, TMF', start='2010-01-01', end=datetime.today())
    else:
        prices = ffn.get('TQQQ, TMF', start='2009-12-31', end=datetime.today())
    
    prices = prices.reset_index()
    prices['portfolio'] = 100
    prices['tqqq_rb'] = 0
    prices['tmf_rb'] = 0
    prices['portfolio_rb'] = 100

    symbols = ['tqqq', 'tmf']

    for i in prices.index:
        if i == 0:
            for symbol in symbols:
                prices.loc[i, symbol + '_rb'] = prices[symbol][0]

            prices.loc[i, 'portfolio_rb'] = 100
            
        else:
            prices.loc[i, 'portfolio'] = prices['portfolio_rb'][i-1] * (
                (prices['tqqq'][i] / prices['tqqq_rb'][i-1]) * 0.55 + 
                (prices['tmf'][i] / prices['tmf_rb'][i-1]) * 0.45
            )
            
            # Quarter-end rebalancing
            if(i != len(prices)-1 and prices.Date[i].month % 3 == 0 and prices.Date[i+1].month % 3 == 1):
                for symbol in symbols:
                    prices.loc[i, symbol + '_rb'] = prices[symbol][i]

                prices.loc[i, 'portfolio_rb'] = prices['portfolio'][i]
            else:
                for symbol in symbols:
                    prices.loc[i, symbol + '_rb'] = prices[symbol + '_rb'][i-1]

                prices.loc[i, 'portfolio_rb'] = prices['portfolio_rb'][i-1]

    
    symbols.append('portfolio')
    export(prices, 'invincible_portfolio_tqqq55_tmf45', symbols)



def calculate_invincible_portfolio5():
    if datetime.now(timezone.utc).astimezone().tzinfo.utcoffset(None)==timedelta(seconds=28800):
        prices = ffn.get('TQQQ, TMF, GLD', start='2010-01-01', end=datetime.today())
    else:
        prices = ffn.get('TQQQ, TMF, GLD', start='2009-12-31', end=datetime.today())
    
    prices = prices.reset_index()
    prices['portfolio'] = 100
    prices['tqqq_rb'] = 0
    prices['upro_rb'] = 0
    prices['tmf_rb'] = 0
    prices['gld_rb'] = 0
    prices['portfolio_rb'] = 100

    symbols = ['tqqq', 'tmf', 'gld']

    for i in prices.index:
        if i == 0:
            for symbol in symbols:
                prices.loc[i, symbol + '_rb'] = prices[symbol][0]

            prices.loc[i, 'portfolio_rb'] = 100
            
        else:
            prices.loc[i, 'portfolio'] = prices['portfolio_rb'][i-1] * (
                    (prices['tqqq'][i] / prices['tqqq_rb'][i-1]) * 0.5 +
                    (prices['tmf'][i] / prices['tmf_rb'][i-1]) * 0.4 +
                    (prices['gld'][i] / prices['gld_rb'][i-1]) * 0.1
                )
            
            # Quarter-end rebalancing
            if(i != len(prices)-1 and prices.Date[i].month % 3 == 0 and prices.Date[i+1].month % 3 == 1):
                for symbol in symbols:
                    prices.loc[i, symbol + '_rb'] = prices[symbol][i]

                prices.loc[i, 'portfolio_rb'] = prices['portfolio'][i]
            else:
                for symbol in symbols:
                    prices.loc[i, symbol + '_rb'] = prices[symbol + '_rb'][i-1]

                prices.loc[i, 'portfolio_rb'] = prices['portfolio_rb'][i-1]

    
    symbols.append('portfolio')
    export(prices, 'invincible_portfolio_tqqq50_tmf40_gld10', symbols)


def calculate_invincible_portfolio6():
    if datetime.now(timezone.utc).astimezone().tzinfo.utcoffset(None)==timedelta(seconds=28800):
        prices = ffn.get('UPRO, TMF, GLD', start='2010-01-01', end=datetime.today())
    else:
        prices = ffn.get('UPRO, TMF, GLD', start='2009-12-31', end=datetime.today())
    
    prices = prices.reset_index()
    prices['portfolio'] = 100
    prices['upro_rb'] = 0
    prices['tmf_rb'] = 0
    prices['gld_rb'] = 0
    prices['portfolio_rb'] = 100

    symbols = ['upro', 'tmf', 'gld']

    for i in prices.index:
        if i == 0:
            for symbol in symbols:
                prices.loc[i, symbol + '_rb'] = prices[symbol][0]

            prices.loc[i, 'portfolio_rb'] = 100
            
        else:
            prices.loc[i, 'portfolio'] = prices['portfolio_rb'][i-1] * (
                    (prices['upro'][i] / prices['upro_rb'][i-1]) * 0.25 +
                    (prices['tmf'][i] / prices['tmf_rb'][i-1]) * 0.25 +
                    (prices['gld'][i] / prices['gld_rb'][i-1]) * 0.50
                )
            
            # Quarter-end rebalancing
            if(i != len(prices)-1 and prices.Date[i].month % 3 == 0 and prices.Date[i+1].month % 3 == 1):
                for symbol in symbols:
                    prices.loc[i, symbol + '_rb'] = prices[symbol][i]

                prices.loc[i, 'portfolio_rb'] = prices['portfolio'][i]
            else:
                for symbol in symbols:
                    prices.loc[i, symbol + '_rb'] = prices[symbol + '_rb'][i-1]

                prices.loc[i, 'portfolio_rb'] = prices['portfolio_rb'][i-1]

    
    symbols.append('portfolio')
    export(prices, 'invincible_portfolio_upro25_tmf25_gld50', symbols)



def export(prices, portfolio, symbols):
    weekday = datetime.today().weekday()

    prices.to_csv('static/' + portfolio + str(weekday) + '.csv')
    prices.to_csv('static/' + portfolio + '_latest.csv')
    prices.to_json('static/' + portfolio + '.json', orient='index')
    prices.tail(2).to_json('static/' + portfolio + '_latest.json', orient='records')



    prices.set_index('Date', inplace=True)

    perf = prices.loc[:, symbols].calc_stats()

    plot_equity_curve(prices, perf, 1, portfolio)
    plot_equity_curve(prices, perf, 3, portfolio)
    plot_equity_curve(prices, perf, 5, portfolio)
    plot_equity_curve(prices, perf, 10, portfolio)
    plot_equity_curve(prices, perf, 20, portfolio)
                    

    for symbol in symbols:
        perf[symbol].stats.to_csv('static/' + symbol + '_stats_' + str(weekday) + '.csv')
        perf[symbol].stats.to_json('static/' + symbol + '_stats.json')
        perf[symbol].return_table.to_csv('static/' + symbol + '_monthly_returns_' + str(weekday) + '.csv')
        perf[symbol].return_table.to_json('static/' + symbol + '.json', orient='index')


    perf['portfolio'].stats.to_csv('static/' + portfolio + '_stats_' + str(weekday) + '.csv')
    perf['portfolio'].stats.to_json('static/' + portfolio + '_stats.json')
    perf['portfolio'].return_table.to_csv('static/' + portfolio + '_monthly_returns_' + str(weekday) + '.csv')
    perf['portfolio'].return_table.to_json('static/' + portfolio + '_monthly_returns.json', orient='index')



def plot_equity_curve(prices, perf, years, portfolio):
    weekday = datetime.today().weekday()

    fig = plt.figure(constrained_layout=True, figsize=(10, 5))
    spec = fig.add_gridspec(ncols=1, nrows=2, height_ratios=[3, 1])

    ax1 = fig.add_subplot(spec[0, 0])
    ax1.plot(prices['portfolio'].tail(years*252), label=portfolio+' ('+str(years)+' year)', linewidth=2)
    ax1.legend(loc='upper left')
    ax1.grid(True)

    ax2 = fig.add_subplot(spec[1, 0])
    ax2.plot(perf['portfolio'].prices.to_drawdown_series().tail(years*252), label='Drawdown')
    ax2.legend(loc='lower left')
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax2.grid(True)


    if(years == 20):
        plt.savefig('static/' + portfolio + '_' + str(weekday) + '.png')
        plt.savefig('static/' + portfolio + '_latest.png')
    else:
        plt.savefig('static/' + portfolio + '_' + str(years) + '_' + str(weekday) + '.png')
        plt.savefig('static/' + portfolio + '_' + str(years) + '_latest.png')

    plt.close()




def calculate_etfs():
    if datetime.now(timezone.utc).astimezone().tzinfo.utcoffset(None)==timedelta(seconds=28800):
        prices = ffn.get('SPY, UPRO, QQQ, QLD, TQQQ, TLT, TMF, GLD', start='2013-01-01', end=datetime.today())
    else:
        prices = ffn.get('SPY, UPRO, QQQ, QLD, TQQQ, TLT, TMF, GLD', start='2012-12-31', end=datetime.today())

    prices.to_csv('static/etfs_latest.csv')

    symbols = ['spy', 'upro', 'qqq', 'qld', 'tqqq', 'tlt', 'tmf', 'gld']

    perf = prices.loc[:, symbols].calc_stats()

    for symbol in symbols:
        perf[symbol].stats.to_csv('static/' + symbol + '_stats.csv')
        perf[symbol].return_table.to_csv('static/' + symbol + '_monthly_returns.csv')


        fig = plt.figure(constrained_layout=True, figsize=(10, 5))
        spec = fig.add_gridspec(ncols=1, nrows=2, height_ratios=[3, 1])

        ax1 = fig.add_subplot(spec[0, 0])
        ax1.plot(prices[symbol], label=symbol, linewidth=2)
        ax1.legend(loc='upper left')
        ax1.grid(True)

        ax2 = fig.add_subplot(spec[1, 0])
        ax2.plot(perf[symbol].prices.to_drawdown_series(), label='Drawdown')
        ax2.legend(loc='lower left')
        ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        ax2.grid(True)

        plt.savefig('static/' + symbol + '.png')


        ### download weekly data
        df = yfin.download(symbol, start='2013-01-01', end=datetime.today(), interval="1wk", actions=False)
        df.to_csv('static/' + symbol + '_dividend_weekly.csv')

        new_df = df.dropna(axis = 0, how ='any')
        new_df.to_csv('static/' + symbol + '_weekly.csv')
            
    
    
# calculate_invincible_portfolio()
# calculate_invincible_portfolio2()
# calculate_invincible_portfolio3()
# calculate_invincible_portfolio4()
# calculate_invincible_portfolio5()
# calculate_invincible_portfolio6()
# calculate_invincible_portfolio7()

calculate_etfs()
