from typing import List
import oandapyV20
import oandapyV20.endpoints.instruments as instruments
import os
import pandas as pd
import datetime 

class OandaApi(object):
    """
        Get forex data with help of the Oanda API

        Attributes
        ----------

        Methods
        -------

    """

    def __init__(self, currency_pairs: List[str], token_path: str = './data_collection/API/oanda_key.txt', account_id:str = "101-001-14961137-001"):
        self._currency_pairs = currency_pairs
        self.__placeholderLength = max(len(currency_pair) for currency_pair in currency_pairs) + 10 # same as in StockApi, only for nice printing 
        self._token_path = token_path
        self._client = oandapyV20.API(access_token=open(token_path, 'r').read(), environment="practice")
        self._account_id = account_id
        

    def __str__(self)->str:
        retStr = 'Currency pairs:\n'
        retStr += '\n'.join(['{:>{width}}'.format(currency_pair, width=self.__placeholderLength) for currency_pair in self._currency_pairs])
        return retStr

    def __repr__(self)->str:
        return 'OandaApi(' + repr(self._currency_pairs) + ')'

    def get_data(self, fromDate:datetime, toDate:datetime, interval:str = 'S5')->pd.DataFrame:
        """
            Get the data for the companies from the api

            Parameters
            ----------
            fromDate: datetime 
                Starting date
            toDate: datetime
                Ending date
            interval: string, default 'd'
                Valid values are 'S5' - 'S30', 'M1' - 'M30',
                    'H1' - 'H12', 'D', 'W', 'M'
            
            Returns
            -------
            pandas.Dataframe()
        """
        forex_data = None
        params = {"from": fromDate.timestamp(),
                  "to": toDate.timestamp(),
                  "granularity":interval} 
        for currency_pair in self._currency_pairs:
            candles = instruments.InstrumentsCandles(instrument=currency_pair, params=params)
            self._client.request(candles)
            ohlc_dict = candles.response["candles"]
            ohlc = pd.DataFrame(ohlc_dict)
            ohlc_df = ohlc.mid.dropna().apply(pd.Series)
            ohlc_df["volume"] = ohlc["volume"]
            ohlc_df.index = ohlc["time"]
            ohlc_df.index.name = 'Date'
            ohlc_df = ohlc_df[[ 'o', 'l' , 'h', 'c', 'volume']]
            ohlc_df.columns = ['Open', 'Low', 'High', 'Close', 'Volume']
            ohlc_df = pd.concat([ohlc_df], keys=[currency_pair], axis=1)
            print(ohlc_df)

            ohlc_df = ohlc_df.apply(pd.to_numeric)
            if forex_data is not None:
                forex_data = forex_data.join(ohlc_df, how='outer')
            else:
                forex_data = ohlc_df
        return forex_data
