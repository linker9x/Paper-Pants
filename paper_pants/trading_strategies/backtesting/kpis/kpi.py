import pandas as pd 
import numpy as np


def CAGR(dataframe:pd.DataFrame, period:str)->float:
    """CAGR
        Compound annual growth rate. Calculate the CARG and return it.
        Compound annual growth rate (CAGR) is a business and investing 
        specific term for the geometric progression ratio that provides 
        a constant rate of return over the time period. CAGR is not an 
        accounting term, but it is often used to describe some element 
        of the business, for example revenue, units delivered, registered 
        users, etc. CAGR dampens the effect of volatility of periodic 
        returns that can render arithmetic means irrelevant. It is 
        particularly useful to compare growth rates from various data 
        sets of common domain such as revenue growth of companies in 
        the same industry or sector.

        CAGR is equivalent to the more generic exponential growth rate 
        when the exponential growth interval is one year.
        
        Parameters
        ----------
        dataframe: pandas.DataFrame
            Dataframe with ohlcv data.
        period: str
            Period of the DataFrame: daily, weekly, monthly, yearly
            weekly,monthly and yearly is additional and not quantified 100%
        
        Returns
        -------
        float
    """
    df = dataframe.copy()
    df['ret'] = dataframe['Close'].pct_change()
    df['cum_return'] = (1 + df['ret']).cumprod()
    if period == 'daily' or period == 'd':
        n = len(df)/252
    elif period == 'weekly' or period == 'w':
        n = len(df)/52
    elif period == 'monthly' or period == 'm':
        n = len(df)/12
    elif period == 'yearly' or period == 'y':
        n = len(df)
    else:
        raise ValueError("Period has a wrong value")
    CAGR = (df['cum_return'][-1])**(1/n) - 1
    return CAGR

def volatility(dataframe:pd.DataFrame, period:str)->float:
    """voldatility
        function to calculate annualized volatility of a trading strategy
        
        In finance, volatility (symbol σ) is the degree of variation of a trading price series over time, usually measured by the standard deviation of logarithmic returns.
        Historic volatility measures a time series of past market prices. Implied volatility looks forward in time, being derived from the market price of a market-traded derivative (in particular, an option).
    
        Parameters
        ----------
        dataframe: pandas.DataFrame
            Dataframe with ohlcv data.
        period: str
            Period of the DataFrame: daily, weekly, monthly
            weekly, monthly is additional and not quantified 100%
            
        Returns
        -------
        float
    """
    df = dataframe.copy()
    df["ret"] = dataframe["Close"].pct_change()
    if period == 'daily' or period == 'd':
        vol = df["ret"].std() * np.sqrt(252)
    elif period == 'weekly' or period == 'w':
        vol = df["ret"].std() * np.sqrt(52)
    elif period == 'monthly' or period == 'm':
        vol = df["et"].std() * np.sqrt(12) 
    else:
        raise ValueError("Period has a wrong value")    
    return vol

def sharpe(dataframe:pd.DataFrame, period:str, rf:float)->float:
    """
        function to calculate sharpe ratio ; rf is the risk free rate
        In finance, the Sharpe ratio (also known as the Sharpe index, the Sharpe measure, and the reward-to-variability ratio) measures the performance of an investment (e.g., a security or portfolio) compared to a risk-free asset, after adjusting for its risk. 
        It is defined as the difference between the returns of the investment and the risk-free return, divided by the standard deviation of the investment (i.e., its volatility). 
        It represents the additional amount of return that an investor receives per unit of increase in risk.
        
        Parameters
        ----------
        dataframe: pandas.DataFrame
            Dataframe with ohlcv data.
        period: str
            Period of the DataFrame: daily, weekly, monthly
            weekly, monthly is additional and not quantified 100%
        rf: float
            Risk free rate

        Returns
        -------
        float
    
    """
    df = dataframe.copy()
    sr = (CAGR(df, period) - rf)/volatility(df, period)
    return sr
    
def sortino(dataframe:pd.DataFrame, period:str, rf:float)->float:
    """
        function to calculate sortino ratio ; rf is the risk free rate
        
        The Sortino ratio measures the risk-adjusted return of an investment asset, portfolio, or strategy.
        It is a modification of the Sharpe ratio but penalizes only those returns falling below a user-specified 
        target or required rate of return, while the Sharpe ratio penalizes both upside and downside volatility equally. 
        Though both ratios measure an investment's risk-adjusted return, they do so in significantly different ways that 
        will frequently lead to differing conclusions as to the true nature of the investment's return-generating efficiency.

        The Sortino ratio is used as a way to compare the risk-adjusted performance of programs with differing risk and return profiles. 
        In general, risk-adjusted returns seek to normalize the risk across programs and then see which has the higher return unit per risk.

        Parameters
        ----------
        dataframe: pandas.DataFrame
            Dataframe with ohlcv data.
        period: str
            Period of the DataFrame: daily, weekly, monthly
            weekly, monthly is additional and not quantified 100%
        rf: float
            Risk free rate

        Returns
        -------
        float
    
    """
    df = dataframe.copy()
    df["ret"] = dataframe["Close"].pct_change()
    if period == 'daily' or period == 'd':        
        neg_vol = df[df["ret"]<0]["ret"].std() * np.sqrt(252)
    elif period == 'weekly' or period == 'w':        
        neg_vol = df[df["ret"]<0]["ret"].std() * np.sqrt(52)
    elif period == 'monthly' or period == 'm':        
        neg_vol = df[df["ret"]<0]["ret"].std() * np.sqrt(12)
    else:
        raise ValueError("Period has a wrong value")     
    sr = (CAGR(df, period) - rf)/neg_vol
    return sr

def max_dd(dataframe:pd.DataFrame)->float:
    """
        function to calculate max drawdown
        The drawdown is the measure of the decline from a historical peak in some 
        variable (typically the cumulative profit or total open equity of a financial trading strategy)

        Parameters
        ----------
        dataframe: pandas.DataFrame
            Dataframe with ohlcv data.

        Returns
        -------
        float
    """
    df = dataframe.copy()
    df["ret"] = dataframe["Close"].pct_change()
    df["cum_return"] = (1 + df["ret"]).cumprod()
    df["cum_roll_max"] = df["cum_return"].cummax()
    df["drawdown"] = df["cum_roll_max"] - df["cum_return"]
    df["drawdown_pct"] = df["drawdown"]/df["cum_roll_max"]
    max_dd = df["drawdown_pct"].max()
    return max_dd
    
def calmar(dataframe:pd.DataFrame, period:str)->float:
    """
        function to calculate calmar ratio

        Calmar ratio (or Drawdown ratio) is a performance measurement used to evaluate 
        Commodity Trading Advisors and hedge funds. 

        Parameters
        ----------
        dataframe: pandas.DataFrame
            Dataframe with ohlcv data.
        period: str
            Period of the DataFrame: daily, weekly, monthly, yearly
            weekly,monthly and yearly is additional and not quantified 100%
        
        Returns
        -------
        float

    """
    df = dataframe.copy()
    clmr = CAGR(df, period)/max_dd(df)
    return clmr

