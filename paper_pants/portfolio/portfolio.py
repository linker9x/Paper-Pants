from datetime import date, datetime, timedelta, time
import paper_pants.data_collection.API.stock_api as sa
import paper_pants.trading_strategies.strategy.strategies as st

class Portfolio(object):
    def __init__(self, tickers, positions):
        self.tickers = tickers
        self.positions = positions

    def __str__(self):
        return 'Tickers: {}, Positions: {}'.format(self.tickers, self.positions)
