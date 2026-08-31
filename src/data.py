import yfinance as yf
import pandas as pd


def download_price_data(tickers, start, end):
   

    data = yf.download(
        tickers,
        start=start,
        end=end,
        auto_adjust=True,
        progress=False
    )

    prices = data["Close"]
    if isinstance(prices, pd.Series):
        prices = prices.to_frame(name=tickers[0])

    return prices


def get_historical_eps(ticker):


    stock = yf.Ticker(ticker)

    try:
        income_statement = stock.get_income_stmt(
            freq="yearly"
        )
    except Exception as error:
        print(
            f"Could not download financial data for {ticker}: "
            f"{error}"
        )
        return pd.Series(dtype=float)

    if income_statement.empty:
        return pd.Series(dtype=float)

    # Possible Yahoo Finance row names.
    net_income_rows = [
        "NetIncome",
        "NetIncomeCommonStockholders",
        "NetIncomeIncludingNoncontrollingInterest"
    ]

    shares_rows = [
        "DilutedAverageShares",
        "BasicAverageShares"
    ]

    net_income = None
    shares = None

    for row in net_income_rows:
        if row in income_statement.index:
            net_income = income_statement.loc[row]
            break

    for row in shares_rows:
        if row in income_statement.index:
            shares = income_statement.loc[row]
            break

    if net_income is None or shares is None:
        return pd.Series(dtype=float)

    combined = pd.concat(
        [
            net_income.rename("net_income"),
            shares.rename("shares")
        ],
        axis=1
    ).dropna()

    if combined.empty:
        return pd.Series(dtype=float)

    eps = combined["net_income"] / combined["shares"]

    eps.index = pd.to_datetime(eps.index)

    eps.index = eps.index + pd.Timedelta(days=90)

    eps.name = ticker

    return eps.sort_index()


def get_historical_eps_for_universe(
    tickers,
    dates
):
   
    eps_data = {}

    for ticker in tickers:

        print(f"Downloading earnings data for {ticker}...")

        eps = get_historical_eps(ticker)

        if eps.empty:
            eps_data[ticker] = pd.Series(
                index=dates,
                dtype=float
            )
            continue

        eps_daily = (
            eps.reindex(dates)
            .ffill()
        )

        eps_data[ticker] = eps_daily

    historical_eps = pd.DataFrame(
        eps_data,
        index=dates
    )

    return historical_eps