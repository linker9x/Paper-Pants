import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import os
import pandas as pd

# initiating API connection and defining trade parameters
token_path = './data_collection/API/oanda_key.txt'
client = oandapyV20.API(access_token=open(token_path, 'r').read(), environment="practice")
account_id = "101-001-14961137-001"

# pairs = ['EUR_USD', 'GBP_USD', 'USD_CHF', 'AUD_USD', 'USD_CAD']
def candles(currency_pair):
    params = {"count": 800,
              "granularity": "S30"}  # granularity can be in seconds S5 - S30, minutes M1 - M30, hours H1 - H12, days D, weeks W or months M
    candles = instruments.InstrumentsCandles(instrument=currency_pair, params=params)
    client.request(candles)
    ohlc_dict = candles.response["candles"]
    ohlc = pd.DataFrame(ohlc_dict)
    ohlc_df = ohlc.mid.dropna().apply(pd.Series)
    ohlc_df["volume"] = ohlc["volume"]
    ohlc_df.index = ohlc["time"]
    ohlc_df = ohlc_df.apply(pd.to_numeric)
    return ohlc_df
