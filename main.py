import yfinance as yf
apple = yf.download("AAPL", start="2020-01-01", end = "2026-01-01")
print(apple)