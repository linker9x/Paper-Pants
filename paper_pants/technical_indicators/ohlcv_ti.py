import datetime
import pandas as pd
import numpy as np
import pandas_datareader.data as pdr
from stockstats import StockDataFrame as sdf
from stocktrends import Renko
import statsmodels.api as sm


def macd(dataframe, fast=12, slow=26, signal=9):
    """macd
    Returns the Moving Average Convergence Divergence (MACD) of the 'Adj Close' col. MACD is a momentum indicator that
    shows the relationship between a fast and slow moving average of the 'Adj Close' price. Default MACD is calculated
    by subtracting the 26-period Exponential Moving Average (EMA) from the 12-period EMA. A nine-day EMA of the MACD
    is then calculated to function as a buy/sell signal.

    Args:
        dataframe (pd.Dataframe): Dataframe with ohlcv data.
        fast (int): Fast period.  Default: 12
        slow (int): Slow period.  Default: 26
        signal (int): Signal period.  Default: 9
    Returns:
        pd.Dataframe: Frame with MACD and Signal cols appended. NaNs dropped.
    """
    df = dataframe.copy()

    df["MA_Fast"] = df["Adj Close"].ewm(span=fast, min_periods=fast).mean()
    df["MA_Slow"] = df["Adj Close"].ewm(span=slow, min_periods=slow).mean()

    df["MACD"] = df["MA_Fast"] - df["MA_Slow"]
    df["Signal"] = df["MACD"].ewm(span=signal, min_periods=signal).mean()
    df.dropna(inplace=True)

    # This yields the same result, but the periods aren't adjustable.
    # stock = sdf.retype(col_rename(dataframe.copy()))
    # df["MACD_2"] = stock.get('macd')

    return df


def atr(dataframe, period=20):
    """atr
    Returns the average true range (ATR) for given period. ATR measures market volatility by assessing entire range of
    a stock price for the given period. True Range (TR ) is the max abs value of the following: HIGH - LOW,
    HIGH - PREV CLOSE, LOW - PREV CLOSE. ATR is calculated from TR by taking the moving average of the true ranges
    for the given period.

    Args:
        dataframe (pd.Dataframe): Dataframe with ohlcv data.
        period (int): Window period.  Default: 20
    Returns:
        pd.Dataframe: Frame with TR and ATR cols appended. NaNs NOT dropped.
    """

    df = dataframe.copy()

    df['H-L'] = abs(df['High']-df['Low'])
    df['H-PC'] = abs(df['High']-df['Adj Close'].shift(1))
    df['L-PC'] = abs(df['Low']-df['Adj Close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)

    df['ATR'] = df['TR'].rolling(period).mean()
    df.drop(['H-L', 'H-PC', 'L-PC'], axis=1, inplace=True)
    #df.dropna(inplace=True)

    # This delivers something else.
    # stock = sdf.retype(col_rename(dataframe.copy()))
    # df["ATR_2"] = stock.get('atr')
    return df


def bollinger_band(dataframe, period=20):
    """Bollinger Band
    A Bollinger Band depicts market volatility by plotting one band two standard deviations above the moving average(MA)
    for a given period and one two standard deviations below. When the prices are more volatile, the bands widen. When
    the prices are less volatile, the bands contract.

    Args:
        dataframe (pd.Dataframe): Dataframe with ohlcv data.
        period (int): Window period.  Default: 20
    Returns:
        pd.Dataframe: Frame with band values and width of the band. NaNs dropped.
    """
    df = dataframe.copy()

    df['MA'] = df['Adj Close'].rolling(period).mean()
    std = df['Adj Close'].rolling(period).std(ddof=0)  # ddof=0 for std of the population

    df["BB_up"] = df["MA"] + 2*std
    df["BB_dn"] = df["MA"] - 2*std
    df["BB_width"] = df["BB_up"] - df["BB_dn"]

    df.dropna(inplace=True)

    # This delivers different values as well. No idea what n is here.
    # stock = sdf.retype(col_rename(dataframe.copy()))
    # df["BB_up_2"] = stock.get('boll_ub')
    # df["BB_dn_2"] = stock.get('boll_lb')
    # df["BB_width_2"] = stock.get('boll')
    return df


def rsi(dataframe, period=14):
    """rsi
    The relative strength index (RSI) is a momentum indicator. RSI that measures the magnitude of price changes to
    determine if the stock was overbought or oversold. It takes on values from 0 to 100. Values of 70 or above suggest
    that the stock might be overbought or overvalued. Values of 30 or below suggest that the stock might be oversold or
    undervalued.

    Args:
        dataframe (pd.Dataframe): Dataframe with ohlcv data.
        period (int): Window period.  Default: 14
    Returns:
        pd.Dataframe: Frame with RS and RSI cols appended. NaNs NOT dropped.
    """
    df = dataframe.copy()

    # difference between cur 'Adj Close' and prev 'Adj Close'
    df['delta'] = df['Adj Close'].diff().dropna()

    # gains and losses
    df['gain'] = np.where(df['delta'] >= 0, df['delta'], 0)
    df['loss'] = np.where(df['delta'] < 0, abs(df['delta']), 0)

    df['gain'][df['gain'].index[period - 1]] = np.mean(df['gain'][:period])  # first value is sum of avg gains
    df['gain'] = df['gain'].drop(df['gain'].index[:(period - 1)])
    df['loss'][df['loss'].index[period - 1]] = np.mean(df['loss'][:period])  # first value is sum of avg losses
    df['loss'] = df['loss'].drop(df['loss'].index[:(period - 1)])

    # rolling mean of the period for the gains divided by the rolling mean of the period for the losses
    df['RS'] = df['gain'].ewm(com=period-1, adjust=False).mean() / df['loss'].ewm(com=period-1, adjust=False).mean()

    df['RSI'] = 100 - (100 / (1 + df['RS']))

    # RSI is only available from stockstats for a period of 6 and 12
    # stock = sdf.retype(col_rename(dataframe.copy()))
    # df["RSI_2_6"] = stock.get('rsi_6')
    # df["RSI_2_12"] = stock.get('rsi_12')

    return df


def adx(dataframe, period=14):
    """adx
    The average directional index (ADX) is used to determine the strength of a price trend. Directional movement
    is determined by comparing the difference between the consecutive lows and highs. The Plus Directional Indicator
    DI_plus) and Minus Directional Indicator (DI_minus) are calculated from smoothed averages of these differences.
    They measure trend direction over time. The Average Directional Index (ADX) is calculated from the smoothed averages
    of the differences and sums between DI_plus and DI_minus.

    Args:
        dataframe (pd.Dataframe): Dataframe with ohlcv data.
        period (int): Window period.  Default: 14
    Returns:
        pd.Dataframe: Frame with DX and ADX cols appended. NaNs dropped.
    """
    df = dataframe.copy()

    df['TR'] = atr(df, period)['TR'] #the period doesn't influence the TR col

    # if cur high - prev high > prev low - cur low --> plus directional movement = cur high - prev high
    df['DMplus'] = np.where((df['High'] - df['High'].shift(1)) > (df['Low'].shift(1) - df['Low']),
                           df['High'] - df['High'].shift(1), 0)
    # if cur high - prev high < 0 --> 0
    df['DMplus'] = np.where(df['DMplus'] < 0,
                             0, df['DMplus'])

    # if prev low - cur low > cur high - prev high --> neg directional movement = prev low - cur low
    df['DMminus'] = np.where((df['Low'].shift(1)-df['Low']) > (df['High']-df['High'].shift(1)),
                              df['Low'].shift(1)-df['Low'], 0)
    # if prev low - cur low < 0 --> 0
    df['DMminus'] = np.where(df['DMminus'] < 0,
                              0, df['DMminus'])

    # smooth the sums of these three cols for a period of n
    df['TR_wws'] = wws(df['TR'], period)
    df['DMplus_wws'] = wws(df['DMplus'], period)
    df['DMminus_wws'] = wws(df['DMminus'], period)

    # calculate the +/- directional indicators
    df['DIplus'] = 100 * (df['DMplus_wws'] / df['TR_wws'])
    df['DIminus'] = 100 * (df['DMminus_wws'] / df['TR_wws'])

    # calculate the difference and sum of +/- directional indicators
    df['DIdiff'] = abs(df['DIplus'] - df['DIminus'])
    df['DIsum'] = df['DIplus'] + df['DIminus']

    # calculate directional movement index
    df['DX'] = 100 * (df['DIdiff'] / df['DIsum'])

    # find the smoothed average for a period of n
    df.dropna(inplace=True)
    df['ADX'] = wwma(df['DX'], period)

    df.dropna(inplace=True)
    return df['ADX']


def wws(column, period):
    """wws
    Wilders smoothed sum calculates the smoothed sum for a given period. The prev cumulative sum is divided by the
    period and subtracted from prev cumulative sum, before the current value is added to arrive at the cur cumulative
    sum.

    Args:
        dataframe (pd.Dataframe): Dataframe with ohlcv data.
        period (int): Window period.
    Returns:
        np.Array: Array with the smoothed sums. NaNs NOT dropped.
    """
    wws_list = []

    for i in range(len(column)):
        if i < period:
            wws_list.append(np.NaN)
        elif i == period:
            wws_list.append(column.rolling(period).sum().tolist()[period])
        elif i > period:
            wws_list.append(wws_list[i-1] - (wws_list[i-1] / period) + column[i])

    return np.array(wws_list)


def wwma(column, period):
    """wwma
    Wilders moving average calculates the smoothed average for a given period. The prev rolling average is multiplied
    by n-1 periods, before the current value is added. This is then divided by n to arrive at the cur rolling average.

    Args:
        dataframe (pd.Dataframe): Dataframe with ohlcv data.
        period (int): Window period.
    Returns:
        np.Array: Array with the smoothed MAs. NaNs NOT dropped.
    """
    return pd.Series(
        data=[column.iloc[:period].mean()],
        index=[column.index[period - 1]],
    ).append(
        column.iloc[period:]
    ).ewm(
        alpha=1.0/period,
        adjust=False,
    ).mean()


def obv(dataframe):
    """obv
    On-balance volume (OBV) is a momentum indicator that uses volume to predict changes in stock price. OBV is
    calculated by adding the day's volume to a cumulative total when the price closes up and subtracting the
    day's volume when the security's price closes down.


    Args:
        dataframe (pd.Dataframe): Dataframe with ohlcv data.
    Returns:
        pd.Dataframe: Frame with OBV col appended. NaNs NOT dropped.
    """
    df = dataframe.copy()

    df['OBV'] = np.where(df['Adj Close'] > df['Adj Close'].shift(1), df['Volume'],
                           np.where(df['Adj Close'] < df['Adj Close'].shift(1), -df['Volume'],
                                    0)).cumsum()

    return df


def slope(dataframe, period=5):
    """slope
    Calculates the slope of 'Adj Close' over a period of n.

    Args:
        dataframe (pd.Dataframe): Dataframe with ohlcv data.
        period (int): Window period.  Default: 5
    Returns:
        pd.Dataframe: Frame with TR and ATR cols appended. NaNs NOT dropped.
    """
    df = dataframe.copy()

    column = df['Adj Close']

    # list for slope values in window
    slopes = [np.NaN for i in range(period-1)]

    for i in range(period, len(column)+1):
        # window -> i.e. row values 0 to 4 of Adj Close
        y = column[i-period:i]

        # [0, 1, 2, 3, 4]
        x = np.array(range(period))

        y_scaled = (y - y.min())/(y.max() - y.min())
        x_scaled = (x - x.min())/(x.max() - x.min())
        x_scaled = sm.add_constant(x_scaled)

        model = sm.OLS(y_scaled, x_scaled)
        results = model.fit()
        slopes.append(results.params[-1])

    slope_angle = (np.rad2deg(np.arctan(np.array(slopes))))

    df['slope_angle'] = np.array(slope_angle)

    # not the same thing?
    # df['close'] = df['Adj Close']
    # print(df[['close']].ta.slope(as_angle=True, offset=5))
    return df


def renko(dataframe):
    """atr
    A Renko chart is built using price movement without standardized time intervals. A new brick is created when the
    price moves a specified price amount. Each block is positioned at a 45-degree angle (up or down) to the prior brick.
    An up brick is typically colored white or green, while a down brick is typically colored black or red. Brick size
    is determined by ATR.

    Args:
        dataframe (pd.Dataframe): Dataframe with ohlcv data.
    Returns:
        pd.Dataframe: Frame with renko col appended.
    """
    df = dataframe.copy()
    brick_size = round(atr(df, 120)['ATR'][-1], 0)
    df.reset_index(inplace=True)

    df_renko = Renko(col_rename(df))
    df_renko.brick_size = brick_size

    return df_renko.get_ohlc_data()


def col_rename(df):
    """
    Helper function that changes the col names to lowercase.

    Args:
        df (pd.Dataframe): Dataframe with ohlcv data.
    Returns:
        pd.Dataframe: Dataframe with lowercase headers.
    """
    df.drop('Close', axis=1, inplace=True)
    df.rename(columns={"Date": "date", "High": "high", "Low": "low", "Open": "open", "Adj Close": "close",
                       "Volume": "volume"}, inplace=True)
    return df