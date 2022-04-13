# -*- coding: utf-8 -*-
"""
Created on Fri Feb 21 10:22:27 2020

@author: TerryLaw
"""

from datetime import datetime, timezone, timedelta

import ffn
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import yfinance as yfin
yfin.pdr_override()


def calculate_etfs():
    # if datetime.now(timezone.utc).astimezone().tzinfo.utcoffset(None)==timedelta(seconds=28800):
    #     prices = ffn.get('SPY, UPRO, QQQ, QLD, TQQQ, TLT, TMF, GLD', start='2005-01-01', end=datetime.today())
    # else:
    #     prices = ffn.get('SPY, UPRO, QQQ, QLD, TQQQ, TLT, TMF, GLD', start='2004-12-31', end=datetime.today())

    # prices.to_csv('static/etfs/etfs_latest.csv')

    symbols = ['spy', 'tlt', 'gld']
    # symbols = ['spy', 'upro', 'qqq', 'qld', 'tqqq', 'tlt', 'tmf', 'gld']

    for symbol in symbols:
        # if datetime.now(timezone.utc).astimezone().tzinfo.utcoffset(None)==timedelta(seconds=28800):
        #     df = yfin.download(symbol, start='2005-01-01', end=datetime.today())
        #     df_weekly = yfin.download(symbol, start='2005-01-01', end=datetime.today(), interval="1wk")
        # else:
        #     df = yfin.download(symbol, start='2004-12-31', end=datetime.today())
        #     df_weekly = yfin.download(symbol, start='2004-12-31', end=datetime.today(), interval="1wk")
        
        if datetime.now(timezone.utc).astimezone().tzinfo.utcoffset(None)==timedelta(seconds=28800):
            df = yfin.download(symbol, start='2013-01-01', end='2022-04-01')
            df_weekly = yfin.download(symbol, start='2013-01-01', end='2022-04-01', interval="1wk")
        else:
            df = yfin.download(symbol, start='2012-12-31', end='2022-03-31')
            df_weekly = yfin.download(symbol, start='2012-12-31', end='2022-03-31', interval="1wk")

        df.dropna(axis = 0, how ='any').to_csv('static/etfs/' + symbol + '_daily.csv')
        df_weekly.dropna(axis = 0, how ='any').to_csv('static/etfs/' + symbol + '_weekly.csv')

        perf = df['Adj Close'].calc_stats()

        perf.stats.to_csv('static/etfs/' + symbol + '_stats.csv')
        perf.return_table.to_csv('static/etfs/' + symbol + '_monthly_returns.csv')


        fig = plt.figure(constrained_layout=True, figsize=(10, 5))
        spec = fig.add_gridspec(ncols=1, nrows=2, height_ratios=[3, 1])

        ax1 = fig.add_subplot(spec[0, 0])
        ax1.plot(df['Adj Close'], label=symbol, linewidth=2)
        ax1.legend(loc='upper left')
        ax1.grid(True)

        ax2 = fig.add_subplot(spec[1, 0])
        ax2.plot(perf.prices.to_drawdown_series(), label='Drawdown')
        ax2.legend(loc='lower left')
        ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        ax2.grid(True)

        plt.savefig('static/etfs/' + symbol + '.png')


        fig = plt.figure(constrained_layout=True, figsize=(10, 5))
        spec = fig.add_gridspec(ncols=1, nrows=2, height_ratios=[3, 1])

        ax1 = fig.add_subplot(spec[0, 0])
        ax1.plot(df['Adj Close'].rebase(), label=symbol, linewidth=2)
        ax1.legend(loc='upper left')
        ax1.grid(True)

        ax2 = fig.add_subplot(spec[1, 0])
        ax2.plot(perf.prices.to_drawdown_series(), label='Drawdown')
        ax2.legend(loc='lower left')
        ax2.yaxis.set_major_formatter(mtick.PercentFormatter(1.0))
        ax2.grid(True)

        plt.savefig('static/etfs/' + symbol + '_rebase.png')

        plt.close()


            

calculate_etfs()
