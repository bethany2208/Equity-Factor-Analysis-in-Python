import numpy as np
import pandas as pd


def calculate_momentum(prices, lookback=252, skip=21):
    momentum = (
        prices.shift(skip) / prices.shift(lookback) - 1
    )

    return momentum


def calculate_volatility(returns, window=252): 
    volatility = (
        returns.rolling(window).std() * np.sqrt(252)
    )

    return volatility


def calculate_value(price, earnings_per_share):  
    value = earnings_per_share / price

    return value


def calculate_forward_return(prices, horizon=21):
    forward_return = (
        prices.shift(-horizon) / prices - 1
    )

    return forward_return


def standardise_factor(factor):
    mean = factor.mean(axis=1)
    std = factor.std(axis=1)

    standardised = (
        factor.sub(mean, axis=0)
        .div(std, axis=0)
    )

    return standardised