import paper_pants.trading_strategies.technical_indicators.ohlcv_ti as ti
import paper_pants.data_collection.API.stock_api as sa
from datetime import date, datetime, timedelta, time
import pandas as pd


class Strategy:
    _tis = {'macd': ti.macd, 'atr': ti.atr, 'bollinger_band': ti.bollinger_band,
            'rsi': ti.rsi, 'adx': ti.adx, 'obv': ti.obv, 'slope': ti.slope, 'renko': ti.renko}

    def __init__(self, portfolio, type, start_date, end_date, name, tis=_tis, period='daily'):
        self.portfolio = portfolio
        self.type = type
        self.start_date = datetime.strptime(start_date, '%Y-%m-%d')
        self.end_date = datetime.strptime(end_date, '%Y-%m-%d')

        self.name = name
        self.tis = tis
        self.period = period

        self.df_hist_data = None

        self.load_ohlcv_data()
        print(self.df_hist_data)
        # self.calculate_indicators()

    def __str__(self):
        return 'Portfolio: {}, Name: {}, Type: {}, Period: {}, TIs: {}'.format(self.portfolio,
                                                                               self.name,
                                                                               self.type,
                                                                               self.period,
                                                                               self.tis.keys())

    def load_ohlcv_data(self):
        if self.type == 'FOREX':
            self.df_hist_data = pd.DataFrame()
        else:
            self.type = 'STOCK'

            sA = sa.StockApi(self.portfolio)
            temp = sA.get_data_pd_yahoo(self.start_date, self.end_date)
            self.df_hist_data = temp

    def calculate_indicators(self):
        hd_df = self.portfolio.historic_data
        ti_df = None

        for ticker in hd_df.stack(level=1).keys():
            ticker_df = copy.deepcopy(hd_df[ticker])
            for t_ind in _tis:
                # print(ticker_df)
                ticker_df = ticker_df.join(_tis[t_ind](ticker_df))

                temp_df = ticker_df[~ticker_df.index.duplicated(keep='first')]
                temp_df = pd.concat([temp_df], keys=[ticker], axis=1)

            if ti_df is not None:
                ti_df = ti_df.join(temp_df)
            else:
                ti_df = temp_df

        self.df = ti_df

    def generate_signal(self):
        pass

    def backtest_strategy(self, start_date, end_date):
        pass
