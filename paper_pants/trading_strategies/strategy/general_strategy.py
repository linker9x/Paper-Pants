import paper_pants.trading_strategies.technical_indicators.ohlcv_ti as ti
import paper_pants.data_collection.API.stock_api as sa
from datetime import date, datetime, timedelta, time
from dateutil.relativedelta import relativedelta
import pandas as pd
import copy


class Strategy:
    _tis = {'macd': ti.macd, 'atr': ti.atr, 'bollinger_band': ti.bollinger_band,
            'rsi': ti.rsi, 'adx': ti.adx, 'obv': ti.obv, 'slope': ti.slope, 'renko': ti.renko}

    def __init__(self, portfolio, type, end_date, offset=0, tis=_tis, period='daily'):
        self.portfolio = portfolio
        self.type = type
        self.offset = offset

        if isinstance(end_date, datetime):
            self.start_date = end_date + relativedelta(months=offset)
            self.end_date = end_date
        else:
            self.start_date = datetime.strptime(end_date, '%Y-%m-%d') + relativedelta(months=offset)
            self.end_date = datetime.strptime(end_date, '%Y-%m-%d')

        self.tis = tis
        self.period = period

        self.df_data = None

        self.load_ohlcv_data()
        self.calculate_indicators()
        print(self.df_data)

    def __str__(self):
        return 'Portfolio: {}, Type: {}, Period: {}, TIs: {}'.format(self.portfolio,
                                                                     self.type,
                                                                     self.period,
                                                                     self.tis.keys())

    def load_ohlcv_data(self):
        if self.type == 'FOREX':
            self.df_data = pd.DataFrame()
        else:
            self.type = 'STOCK'

            sA = sa.StockApi(self.portfolio)
            temp = sA.get_data_pd_yahoo(self.start_date, self.end_date)
            self.df_data = temp

    def calculate_indicators(self):
        df_indicators = None

        if self.tis:
            for ticker in self.df_data.stack(level=1).keys():
                df_ticker = copy.deepcopy(self.df_data[ticker])
                for t_ind in self.tis:
                    df_ticker = df_ticker.join(self.tis[t_ind](df_ticker))

                    df_temp = df_ticker[~df_ticker.index.duplicated(keep='first')]
                    df_temp = pd.concat([df_temp], keys=[ticker], axis=1)

                if df_indicators is not None:
                    df_indicators = df_indicators.join(df_temp)
                else:
                    df_indicators = df_temp

            self.df_data = df_indicators

    def generate_signal(self):
        pass

    def backtest_strategy(self, start_date, end_date):
        pass
