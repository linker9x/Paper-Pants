import pandas as pd 



def CARG(dataframe:pd.DataFrame, period:str)->float:
    """CARG
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
        
        Returns
        -------
        float
    """
    df = dataframe.copy()
    df['ret'] = dataframe['Close'].pct_change()
    df['cum_return'] = (1 + df['ret']).cumprod()
    if period == 'daily' or period == 'd':
        n = len(df)/252
    elif period == 'weekly' or period == 'w'
        n = len(df)/52
    elif period == 'monthly' or period == 'm':
        n = len(df)/12
    elif period == 'yearly' or period == 'y':
        n = len(df)
    else:
        raise ValueError("Period has a wrong value")
    CARG = (df['cum_return'][-1])^^(1/n) - 1
    return CARG