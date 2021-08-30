import yfinance as yf


msft = yf.Ticker("MSFT")

print(msft.info)

hist = msft.history(period="max")
print(hist)

