import yfinance as yf
from src.factors import calculate_momentum
from src.factors import calculate_volatility
from src.factors import calculate_value

tickers = ["AAPL", "MSFT", "NVDA", "AMZN", "JPM", "META"]

data = yf.download(
    tickers,
    start = "2020-01-01",
    end = "2026-01-01"
)

prices = data["Close"]
returns = prices.pct_change()
momentum = calculate_momentum(prices)
volatility = calculate_volatility(returns)

print("Closing Prices:")
print(prices.head())

print("\nDaily Returns (%):")
print((returns * 100).head())

print("\nMomentum:")
print(momentum.tail())

print("\nVolatility:")
print(volatility.tail())

