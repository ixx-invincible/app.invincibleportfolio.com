import yfinance as yf

msft = yf.Ticker("MSFT")

# get stock info
print(msft.info)

hist = msft.history(period="max")
print(hist)