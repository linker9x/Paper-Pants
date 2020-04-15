from datetime import date, datetime, timedelta, time
import paper_pants.data_collection.API.stock_api as sa
import paper_pants.trading_strategies.strategies as st

class Portfolio(object):
    def __init__(self, tickers, strategy = None):
        self.tickers = tickers
        self.strategy = strategy
        self.historic_data = {'intraday': None,
                              'daily': None,
                              'monthly': None,
                              'yearly': None}

        startDate = datetime.combine(date.today(), time()) - timedelta(1095)
        endDate = datetime.combine(date.today(), time())
        self.get_historic_data(startDate, endDate)

    def __str__(self):
        return 'Portfolio: {}'.format(self.portfolio)

    def get_historic_data(self, startDate, endDate, period='daily'):
        sA = sa.StockApi(self.tickers)
        temp = sA.get_data_pd_yahoo(startDate, endDate)
        self.historic_data['daily'] = temp
