from src.data import (
    download_price_data,
    get_historical_eps_for_universe
)

from src.factors import (
    calculate_momentum,
    calculate_volatility,
    calculate_value,
    calculate_forward_return,
    standardise_factor
)

from src.analysis import (
    create_analysis_dataset,
    run_cross_sectional_regressions,
    calculate_factor_statistics,
    factor_correlations
)


TICKERS = [
    "AAPL",
    "MSFT",
    "NVDA",
    "AMZN",
    "JPM",
    "META"
]

START_DATE = "2020-01-01"
END_DATE = "2026-01-01"

FORWARD_RETURN_HORIZON = 21



print("\nDownloading price data...")

prices = download_price_data(
    TICKERS,
    start=START_DATE,
    end=END_DATE
)

print(
    f"Downloaded {len(prices)} trading days "
    f"for {len(prices.columns)} stocks."
)



returns = prices.pct_change()



print("\nCalculating momentum...")

momentum = calculate_momentum(
    prices
)


print("Calculating volatility...")

volatility = calculate_volatility(
    returns
)


print("\nDownloading historical earnings data...")

historical_eps = get_historical_eps_for_universe(
    TICKERS,
    prices.index
)


print("\nCalculating earnings yield...")

value = calculate_value(
    prices,
    historical_eps
)


print("Calculating subsequent returns...")

forward_returns = calculate_forward_return(
    prices,
    horizon=FORWARD_RETURN_HORIZON
)



print("Standardising factors...")

momentum_z = standardise_factor(
    momentum
)

value_z = standardise_factor(
    value
)

volatility_z = standardise_factor(
    volatility
)


print("\nCreating analysis dataset...")

analysis_data = create_analysis_dataset(
    momentum_z,
    value_z,
    volatility_z,
    forward_returns
)

print(
    f"Analysis dataset contains "
    f"{len(analysis_data)} observations."
)


print("\nRunning cross-sectional regressions...")

coefficients = run_cross_sectional_regressions(
    analysis_data
)


results = calculate_factor_statistics(
    coefficients
)



print("\n")
print("=" * 60)
print("FACTOR RESEARCH RESULTS")
print("=" * 60)

print("\nAverage regression coefficients:")

print(
    results[
        [
            "factor",
            "mean_coefficient",
            "standard_error",
            "t_statistic",
            "number_of_periods"
        ]
    ].to_string(index=False)
)


correlations = factor_correlations(
    analysis_data
)

print("\n")
print("=" * 60)
print("CORRELATIONS")
print("=" * 60)

print(
    correlations.to_string()
)




print("\n")
print("=" * 60)
print("DATA CHECKS")
print("=" * 60)

print("\nPrice data:")
print(prices.tail())

print("\nMomentum:")
print(momentum.tail())

print("\nValue / Earnings Yield:")
print(value.tail())

print("\nVolatility:")
print(volatility.tail())

print("\nForward returns:")
print(forward_returns.tail())