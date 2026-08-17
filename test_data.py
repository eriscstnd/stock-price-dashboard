import yfinance as yf

ticker = "AAPL"
data = yf.download(ticker, period="1y", interval="1d")
data.columns = data.columns.get_level_values(0) 
print(data.head())
import ta

data["SMA_20"] = ta.trend.sma_indicator(data["Close"], window=20)
data["SMA_50"] = ta.trend.sma_indicator(data["Close"], window=50)
data["RSI"] = ta.momentum.rsi(data["Close"], window=14)
data["MACD"] = ta.trend.macd_diff(data["Close"])
bb = ta.volatility.BollingerBands(data["Close"])
data["BB_upper"] = bb.bollinger_hband()
data["BB_lower"] = bb.bollinger_lband()

print(data.tail())
import matplotlib.pyplot as plt

data[["Close", "SMA_20", "SMA_50"]].plot(figsize=(12,6))
plt.show()