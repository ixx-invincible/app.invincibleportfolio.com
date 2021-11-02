import ffn
import yfinance as yfin
yfin.pdr_override()

prices = ffn.get('QQQ, TQQQ', start='2005-01-01')


prices.to_csv('static/qqq_tqqq.csv')