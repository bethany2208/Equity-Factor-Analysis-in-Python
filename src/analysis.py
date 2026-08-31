import numpy as np
import pandas as pd


def create_analysis_dataset(
    momentum,
    value,
    volatility,
    forward_returns
):
   

    data = pd.concat(
        [
            momentum.stack().rename("momentum"),
            value.stack().rename("value"),
            volatility.stack().rename("volatility"),
            forward_returns.stack().rename("forward_return")
        ],
        axis=1
    )

    data = data.dropna()

    return data


def run_cross_sectional_regressions(data):
 

    coefficients = []

    required_columns = [
        "momentum",
        "value",
        "volatility",
        "forward_return"
    ]

    for date, group in data.groupby(level=0):

        group = group.dropna(
            subset=required_columns
        )

        # Need enough stocks to estimate the regression.
        if len(group) < 10:
            continue

        y = group["forward_return"].to_numpy()

        X = group[
            [
                "momentum",
                "value",
                "volatility"
            ]
        ].to_numpy()

        # Add intercept.
        X = np.column_stack(
            [
                np.ones(len(X)),
                X
            ]
        )

        try:
            beta = np.linalg.lstsq(
                X,
                y,
                rcond=None
            )[0]
        except np.linalg.LinAlgError:
            continue

        coefficients.append(
            [
                date,
                beta[0],
                beta[1],
                beta[2],
                beta[3]
            ]
        )

    coefficients = pd.DataFrame(
        coefficients,
        columns=[
            "date",
            "alpha",
            "momentum",
            "value",
            "volatility"
        ]
    )

    if coefficients.empty:
        raise ValueError(
            "No cross-sectional regressions could be estimated."
        )

    coefficients = coefficients.set_index("date")

    return coefficients


def calculate_factor_statistics(coefficients):


    results = []

    for factor in [
        "momentum",
        "value",
        "volatility"
    ]:

        series = coefficients[factor].dropna()

        mean_coefficient = series.mean()

        standard_error = (
            series.std(ddof=1)
            / np.sqrt(len(series))
        )

        t_stat = (
            mean_coefficient / standard_error
            if standard_error != 0
            else np.nan
        )

        results.append(
            [
                factor,
                mean_coefficient,
                standard_error,
                t_stat,
                len(series)
            ]
        )

    results = pd.DataFrame(
        results,
        columns=[
            "factor",
            "mean_coefficient",
            "standard_error",
            "t_statistic",
            "number_of_periods"
        ]
    )

    return results


def factor_correlations(data):
   

    columns = [
        "momentum",
        "value",
        "volatility",
        "forward_return"
    ]

    return data[columns].corr()