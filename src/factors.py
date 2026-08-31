import numpy as np

def calculate_momentum(prices):
    momentum = prices.shift(21) / prices.shift(252) -1
    return momentum

def calculate_volatility(returns, window=252):
    volatility = returns.rolling(window).std() * np.sqrt(252)
    return volatility

def calculate_value(price, book_value):
    #going to calculate value using market value/ book value
    return price/ book_value

