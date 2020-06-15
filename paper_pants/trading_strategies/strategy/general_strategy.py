import paper_pants.trading_strategies.technical_indicators.ohlcv_ti as ti
import paper_pants.data_collection.API.stock_api as sa
import paper_pants.data_collection.API.oanda_api as oa
from datetime import date, datetime, timedelta, time
from dateutil.relativedelta import relativedelta
import pandas as pd
import copy


class Strategy:
    _tis = {'macd': ti.macd, 'atr': ti.atr, 'bollinger_band': ti.bollinger_band,
            'rsi': ti.rsi, 'adx': ti.adx, 'obv': ti.obv, 'slope': ti.slope, 'renko': ti.renko}

    def __init__(self, portfolio, type, start_date, end_date, tis=_tis, period='daily'):
        self.start_date = start_date
        self.end_date = end_date
        self.portfolio = portfolio
        self.type = type
        self.tis = tis
        self.period = period
        self.df_data = None

        self.__load_ohlcv_data()
        self.__calculate_indicators()
        print(self.df_data)

    def __str__(self):
        return 'Portfolio: {}, Type: {}, Period: {}, TIs: {}'.format(self.portfolio,
                                                                     self.type,
                                                                     self.period,
                                                                     self.tis.keys())

    def __load_ohlcv_data(self):
        if self.type == 'FOREX':
            oA = oa.OandaApi(self.portfolio.tickers)
            temp = oA.get_data(self.start_date, self.end_date, 'M1')
            self.df_data = temp
        elif self.type == 'STOCK':
            sA = sa.StockApi(self.portfolio.tickers)
            temp = sA.get_data_pd_yahoo(self.start_date, self.end_date)
            self.df_data = temp
        else:
            raise Exception('Not a valid type.')

    def __calculate_indicators(self):
        df_indicators = None

        if self.tis:
            for ticker in self.df_data.stack(level=1).keys():
                df_ticker = copy.deepcopy(self.df_data[ticker])
                df_ticker.ffill(axis=0, inplace=True)
                for t_ind in self.tis:
                    df_ticker = df_ticker.join(self.tis[t_ind](df_ticker))

                    df_temp = df_ticker[~df_ticker.index.duplicated(keep='first')]
                    df_temp = pd.concat([df_temp], keys=[ticker], axis=1)

                if df_indicators is not None:
                    df_indicators = df_indicators.join(df_temp)
                else:
                    df_indicators = df_temp

            self.df_data = df_indicators

    def generate_signals(self):
        pass

    def long_something(self):
        return 'LONG'

    def short_something(self):
        return 'SHORT'

    def exit_something(self):
        return 'EXIT'

    def backtest_strategy(self, start_date, end_date):
        pass
