# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 10:22:27 2020

@author: TerryLaw
"""

from datetime import datetime, timezone, timedelta

import ffn
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
from matplotlib.font_manager import FontProperties
from matplotlib import font_manager
import yfinance as yfin
yfin.pdr_override()





def calculate_etfs():
    if datetime.now(timezone.utc).astimezone().tzinfo.utcoffset(None)==timedelta(seconds=28800):
        prices = ffn.get('SPY, UPRO, QQQ, QLD, TQQQ, TLT, TMF, GLD', start='2013-01-01', end='2021-12-31')
    else:
        prices = ffn.get('SPY, UPRO, QQQ, QLD, TQQQ, TLT, TMF, GLD', start='2012-12-31', end='2021-12-31')

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
        df = yfin.download(symbol, start='2013-01-01', end=datetime.today(), interval="1wk")
        df.to_csv('static/' + symbol + '_dividend_weekly.csv')

        new_df = df.dropna(axis = 0, how ='any')
        new_df.to_csv('static/' + symbol + '_weekly.csv')
            
        ### download daily data
        df = yfin.download(symbol, start='2013-01-01', end=datetime.today())
        df.to_csv('static/' + symbol + '_dividend_daily.csv')

        new_df = df.dropna(axis = 0, how ='any')
        new_df.to_csv('static/' + symbol + '_daily.csv')
    


def calculate_ifree_growth_and_income_fund():
    if datetime.now(timezone.utc).astimezone().tzinfo.utcoffset(None)==timedelta(seconds=28800):
        prices = ffn.get('TLT, GLD, BIL', start='2013-01-01', end=datetime.today())
    else:
        prices = ffn.get('TLT, GLD, BIL', start='2012-12-31', end=datetime.today())
    
    prices = prices.reset_index()
    prices['portfolio'] = 100
    prices['tlt_rb'] = 0
    prices['gld_rb'] = 0
    prices['bil_rb'] = 0
    prices['portfolio_rb'] = 100

    symbols = ['tlt', 'gld', 'bil']

    for i in prices.index:
        if i == 0:
            for symbol in symbols:
                prices.loc[i, symbol + '_rb'] = prices[symbol][0]

            prices.loc[i, 'portfolio_rb'] = 100
            
        else:
            prices.loc[i, 'portfolio'] = prices['portfolio_rb'][i-1] * (
                    (prices['tlt'][i] / prices['tlt_rb'][i-1]) * 0.5 +
                    (prices['gld'][i] / prices['gld_rb'][i-1]) * 0.25 +
                    (prices['bil'][i] / prices['bil_rb'][i-1]) * 0.25
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
    export(prices, 'ifree_growth_and_income_fund_tqqq50_tmf40_gld10', symbols)
    
    
def calculate_ifree_da():
    if datetime.now(timezone.utc).astimezone().tzinfo.utcoffset(None)==timedelta(seconds=28800):
        prices = ffn.get('TQQQ, TMF, GLD, QLD', start='2011-01-01', end='2022-01-01')
    else:
        prices = ffn.get('TQQQ, TMF, GLD, QLD', start='2010-12-31', end='2021-12-31')
    
    prices = prices.reset_index()
    prices['portfolio'] = 100
    prices['tqqq_rb'] = 0
    prices['tmf_rb'] = 0
    prices['gld_rb'] = 0
    prices['portfolio_rb'] = 100

    symbols = ['tqqq', 'tmf', 'gld', 'qld']

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
    export(prices, 'ifree_da_tqqq50_tmf40_gld10', symbols)

    
    ### Plot for Fact Sheet
    perf = prices.loc[:, symbols].calc_stats()

    fig = plt.figure(constrained_layout=True, figsize=(10, 5))
    spec = fig.add_gridspec(ncols=1, nrows=2, height_ratios=[3, 1])

    ax1 = fig.add_subplot(spec[0, 0])
    ax1.plot(prices['portfolio'], label="iFREE Adventurer Strategy", linewidth=2)
    ax1.legend(loc='upper left')
    ax1.grid(True)

    ax1.plot(prices['qld'].rebase(), label="Nasdaq 100 Index 2x", linewidth=2)
    ax1.legend(loc='upper left')
    ax1.grid(True)

    ax2 = fig.add_subplot(spec[1, 0])
    ax2.plot(perf['portfolio'].prices.to_drawdown_series(), label='Drawdown')
    ax2.legend(loc='lower left')
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax2.grid(True)

    plt.savefig('static/iFREE_Adventurer_Strategy_latest_en.png')
    plt.close()


    fig = plt.figure(constrained_layout=True, figsize=(10, 5))
    spec = fig.add_gridspec(ncols=1, nrows=2, height_ratios=[3, 1])

    plt.rcParams['font.sans-serif'] = ['MingLiU']
    plt.rcParams['axes.unicode_minus'] = False

    ax1 = fig.add_subplot(spec[0, 0])
    ax1.plot(prices['portfolio'], label="愛訊冒險家投資策略", linewidth=2)
    ax1.legend(loc='upper left')
    ax1.grid(True)

    ax1.plot(prices['qld'].rebase(), label="納斯達克100指數 (2x)", linewidth=2)
    ax1.legend(loc='upper left')
    ax1.grid(True)

    ax2 = fig.add_subplot(spec[1, 0])
    ax2.plot(perf['portfolio'].prices.to_drawdown_series(), label='最大回徹', linewidth=2)
    ax2.legend(loc='lower left')
    ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
    ax2.grid(True)

    plt.savefig('static/iFREE_Adventurer_Strategy_latest_tc.png')
    plt.close()




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

    perf.stats.to_csv('static/' + portfolio + '_stats_da.csv')



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


# calculate_etfs()
# calculate_ifree_growth_and_income_fund()
calculate_ifree_da()
