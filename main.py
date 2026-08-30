import yfinance as yf
##using five large companies to begin, won't come to a valid conclusion but everythibg can workd
tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "JPM", "META"]

data = yf.download(
    tickers,
    start = "2020-01-01",
    end = "2026-01-01"
)

prices = data["Close"]
returns = prices.pct_change()

print("Closing Prices:")
print(prices.head())

print("\nDaily Returns (%):")
print((returns * 100).head())

print("\nDataset Shape:")
print(prices.shape)

print("\nSummary Statistics:")
print(returns.describe())

#Momentum

