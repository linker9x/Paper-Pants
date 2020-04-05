import numpy as np
import datetime
import ffn


def cagr(DF):
    "function to calculate the Cumulative Annual Growth Rate of a trading strategy"
    df = DF.copy()
    df["daily_ret"] = DF["Adj Close"].pct_change()
    df["cum_return"] = (1 + df["daily_ret"]).cumprod()
    n = len(df) / 252
    CAGR = (df["cum_return"][-1]) ** (1 / n) - 1

    ffn_CAGR = ffn.core.calc_cagr(DF["Adj Close"])
    return CAGR, ffn_CAGR


def volatility(DF):
    "function to calculate annualized volatility of a trading strategy"
    df = DF.copy()
    df["daily_ret"] = DF["Adj Close"].pct_change()
    vol = df["daily_ret"].std() * np.sqrt(252)
    return vol


def sharpe(DF, rf):
    "function to calculate sharpe ratio ; rf is the risk free rate"
    df = DF.copy()
    sr = (cagr(df)[0] - rf) / volatility(df)

    df["daily_ret"] = DF["Adj Close"].pct_change()
    ffn_sr = ffn.core.calc_sharpe(df["daily_ret"], rf=rf, nperiods=252)
    return sr, ffn_sr


def sortino(DF, rf):
    "function to calculate sortino ratio ; rf is the risk free rate"
    df = DF.copy()
    df["daily_ret"] = DF["Adj Close"].pct_change()
    neg_vol = df[df["daily_ret"] < 0]["daily_ret"].std() * np.sqrt(252)
    sr = (cagr(df)[0] - rf) / neg_vol

    ffn_sr = ffn.core.calc_sortino_ratio(df["daily_ret"], rf=rf, nperiods=252)
    return sr, ffn_sr


def max_dd(DF):
    "function to calculate max drawdown"
    df = DF.copy()
    df["daily_ret"] = DF["Adj Close"].pct_change()
    df["cum_return"] = (1 + df["daily_ret"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    df["drawdown_pct"] = df["drawdown"] / df["cum_roll_max"]
    max_dd = df["drawdown_pct"].max()

    ffn_max_dd = ffn.core.calc_max_drawdown(DF["Adj Close"])
    return max_dd, ffn_max_dd


def calmar(DF):
    "function to calculate calmar ratio"
    df = DF.copy()
    clmr = cagr(df)[0] / max_dd(df)[0]

    ffn_clmr = ffn.core.calc_calmar_ratio(DF["Adj Close"])
    return clmr, ffn_clmr