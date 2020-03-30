import datetime
import pandas as pd
import numpy as np
import pandas_datareader.data as pdr
from stockstats import StockDataFrame as sdf
from stocktrends import Renko
import statsmodels.api as sm


def macd(dataframe, fast, slow, signal):
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


def atr(dataframe, n):
    df = dataframe.copy()

    df['H-L'] = abs(df['High']-df['Low'])
    df['H-PC'] = abs(df['High']-df['Adj Close'].shift(1))
    df['L-PC'] = abs(df['Low']-df['Adj Close'].shift(1))
    df['TR'] = df[['H-L', 'H-PC', 'L-PC']].max(axis=1, skipna=False)

    df['ATR'] = df['TR'].rolling(n).mean()
    df.drop(['H-L', 'H-PC', 'L-PC'], axis=1, inplace=True)
    #df.dropna(inplace=True)

    # This delivers something else.
    # stock = sdf.retype(col_rename(dataframe.copy()))
    # df["ATR_2"] = stock.get('atr')
    return df

def bollinger_band(dataframe,n):
    df = dataframe.copy()

    df['MA'] = df['Adj Close'].rolling(n).mean()
    std = df['Adj Close'].rolling(n).std(ddof=0)  # ddof=0 for std of the population

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


def rsi(dataframe, n):
    df = dataframe.copy()

    df['delta'] = df['Adj Close'].diff().dropna()

    df['gain'] = np.where(df['delta'] >= 0, df['delta'], 0)
    df['loss'] = np.where(df['delta'] < 0, abs(df['delta']), 0)

    df['gain'][df['gain'].index[n - 1]] = np.mean(df['gain'][:n])  # first value is sum of avg gains
    df['gain'] = df['gain'].drop(df['gain'].index[:(n - 1)])
    df['loss'][df['loss'].index[n - 1]] = np.mean(df['loss'][:n])  # first value is sum of avg losses
    df['loss'] = df['loss'].drop(df['loss'].index[:(n - 1)])
    df['RS'] = df['gain'].ewm(com=n - 1, adjust=False).mean() / df['loss'].ewm(com=n - 1, adjust=False).mean()

    df['RSI'] = 100 - (100 / (1 + df['RS']))

    # RSI is only available from stockstats for a period of 6 and 12
    # stock = sdf.retype(col_rename(dataframe.copy()))
    # df["RSI_2_6"] = stock.get('rsi_6')
    # df["RSI_2_12"] = stock.get('rsi_12')

    return df


def adx(dataframe, n):
    df = dataframe.copy()

    df['TR'] = atr(df, n)['TR'] #the period doesn't influence the TR col

    # if cur high - prev high > prev low - cur low --> plus directional movement = cur high - prev high
    df['DMplus'] = np.where((df['High'] - df['High'].shift(1)) > (df['Low'].shift(1) - df['Low']),
                           df['High'] - df['High'].shift(1), 0)
    # if cur high - prev high < 0 --> 0
    df['DMplus'] = np.where(df['DMplus'] < 0,
                             0, df['DMplus'])

    # if prev low - cur low > cur high - prev high --> neg directional movement = prev low - cur low
    df['DMminus'] = np.where((df['Low'].shift(1)-df['Low'])>(df['High']-df['High'].shift(1)),
                              df['Low'].shift(1)-df['Low'], 0)
    # if prev low - cur low < 0 --> 0
    df['DMminus'] = np.where(df['DMminus'] < 0,
                              0, df['DMminus'])

    # smooth the sums of these three cols for a period of n
    df['TR_wws'] = wws(df['TR'], n)
    df['DMplus_wws'] = wws(df['DMplus'], n)
    df['DMminus_wws'] = wws(df['DMminus'], n)

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
    df['ADX'] = wwma(df['DX'], n)

    df.dropna(inplace=True)
    return df['ADX']

def wws(column, period):
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
    df = dataframe.copy()

    df['obv'] = np.where(df['Adj Close'] > df['Adj Close'].shift(1), df['Volume'],
                           np.where(df['Adj Close'] < df['Adj Close'].shift(1), -df['Volume'],
                                    0)).cumsum()

    return df


def slope(column, n):
    "function to calculate the slope of n consecutive points on a plot"
    slopes = [i*0 for i in range(n-1)]
    for i in range(n, len(column)+1):
        y = column[i-n:i]
        x = np.array(range(n))
        y_scaled = (y - y.min())/(y.max() - y.min())
        x_scaled = (x - x.min())/(x.max() - x.min())
        x_scaled = sm.add_constant(x_scaled)
        model = sm.OLS(y_scaled,x_scaled)
        results = model.fit()
        slopes.append(results.params[-1])
    slope_angle = (np.rad2deg(np.arctan(np.array(slopes))))
    return np.array(slope_angle)


def renko(dataframe):
    df = dataframe.copy()
    brick_size = round(atr(df, 120)['ATR'][-1], 0)
    df.reset_index(inplace=True)

    df_renko = Renko(col_rename(df))
    df_renko.brick_size = brick_size

    return df_renko.get_ohlc_data()


def col_rename(df):
    df.drop('Close', axis=1, inplace=True)
    df.rename(columns={"Date": "date", "High": "high", "Low": "low", "Open": "open", "Adj Close": "close",
                       "Volume": "volume"}, inplace=True)
    return df