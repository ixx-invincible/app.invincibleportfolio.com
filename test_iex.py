import os
import pandas_datareader.data as web
from datetime import datetime

os.environ["IEX_API_KEY"] = "pk_1dafd28f39414e6fa735c9350a508a47"


start = datetime(2021, 6, 1)
end = datetime(2021, 6, 30)

f = web.DataReader('SPY', 'iex', start, end)

print(f.tail())