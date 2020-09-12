import yfinance as yf
import matplotlib as plt
import pandas as pd

msft = yf.Ticker("MSFT")
#print(msft)

#print(msft.info)
#print(msft.history(period="max"))

h = msft.history(period="max")

#ATR
h['move'] =  h['Close'] - h['Open']
h['ATR'] = h['move'].rolling(window=14).mean()

#Bollinger bands
h['upper_band'] = h['Close'].rolling(window=20).mean() + (h['Close'].rolling(window=20).std() * 2)
h['lower_band'] = h['Close'].rolling(window=20).mean() - (h['Close'].rolling(window=20).std() * 2)

#Relative strength indicator
h['prev_close'] =  h['Close'].shift(1)
h['move_perc'] = h.apply(lambda x: 100 - round((x['Open'] * 100) / x['Close'], 2), axis=1)


h['down_strength'] = h['move_perc'].rolling(window=14).apply(lambda x: abs(x[x < 0].mean()))
h['up_strength'] = h['move_perc'].rolling(window=14).apply(lambda x: x[x >= 0].mean())
h['rsi'] = 100 - (100 / (1 + (h['up_strength'] / h['down_strength'])))
print(h.tail())

h['rsi'][h.index.year == 2020].plot()
h[['Open', 'Close', 'prev_close', 'move_perc', 'move', 'up_strength', 'down_strength', 'rsi']].tail(21)

