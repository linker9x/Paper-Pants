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
    "function to calculate ADX"
    df2 = dataframe.copy()
    df2['TR'] = atr(df2,n)['TR'] #the period parameter of ATR function does not matter because period does not influence TR calculation
    df2['DMplus']=np.where((df2['High']-df2['High'].shift(1))>(df2['Low'].shift(1)-df2['Low']),df2['High']-df2['High'].shift(1),0)
    df2['DMplus']=np.where(df2['DMplus']<0,0,df2['DMplus'])
    df2['DMminus']=np.where((df2['Low'].shift(1)-df2['Low'])>(df2['High']-df2['High'].shift(1)),df2['Low'].shift(1)-df2['Low'],0)
    df2['DMminus']=np.where(df2['DMminus']<0,0,df2['DMminus'])
    TRn = []
    DMplusN = []
    DMminusN = []
    TR = df2['TR'].tolist()
    DMplus = df2['DMplus'].tolist()
    DMminus = df2['DMminus'].tolist()
    for i in range(len(df2)):
        if i < n:
            TRn.append(np.NaN)
            DMplusN.append(np.NaN)
            DMminusN.append(np.NaN)
        elif i == n:
            TRn.append(df2['TR'].rolling(n).sum().tolist()[n])
            DMplusN.append(df2['DMplus'].rolling(n).sum().tolist()[n])
            DMminusN.append(df2['DMminus'].rolling(n).sum().tolist()[n])
        elif i > n:
            TRn.append(TRn[i-1] - (TRn[i-1]/n) + TR[i])
            DMplusN.append(DMplusN[i-1] - (DMplusN[i-1]/n) + DMplus[i])
            DMminusN.append(DMminusN[i-1] - (DMminusN[i-1]/n) + DMminus[i])
    df2['TRn'] = np.array(TRn)
    df2['DMplusN'] = np.array(DMplusN)
    df2['DMminusN'] = np.array(DMminusN)
    df2['DIplusN']=100*(df2['DMplusN']/df2['TRn'])
    df2['DIminusN']=100*(df2['DMminusN']/df2['TRn'])
    df2['DIdiff']=abs(df2['DIplusN']-df2['DIminusN'])
    df2['DIsum']=df2['DIplusN']+df2['DIminusN']
    df2['DX']=100*(df2['DIdiff']/df2['DIsum'])
    ADX = []
    DX = df2['DX'].tolist()
    for j in range(len(df2)):
        if j < 2*n-1:
            ADX.append(np.NaN)
        elif j == 2*n-1:
            ADX.append(df2['DX'][j-n+1:j+1].mean())
        elif j > 2*n-1:
            ADX.append(((n-1)*ADX[j-1] + DX[j])/n)
    df2['ADX']=np.array(ADX)

    stock = sdf.retype(col_rename(dataframe.copy()))
    df2["ADX_2"] = stock.get('adx')

    df2.dropna(inplace=True)
    return df2[['ADX', 'ADX_2']]


def obv(dataframe):
    df = dataframe.copy()

    df['obv'] = np.where(df['Adj Close'] > df['Adj Close'].shift(1), df['Volume'],
                           np.where(df['Adj Close'] < df['Adj Close'].shift(1), -df['Volume'],
                                    0)).cumsum()

    return df


def slope(ser,n):
    "function to calculate the slope of n consecutive points on a plot"
    slopes = [i*0 for i in range(n-1)]
    for i in range(n,len(ser)+1):
        y = ser[i-n:i]
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