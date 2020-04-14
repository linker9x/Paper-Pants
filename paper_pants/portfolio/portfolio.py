from datetime import date, datetime, timedelta, time
import paper_pants.data_collection.API.stock_api as sa

class PortfolioManager(object):
    def __init__(self, portfolio):
        self.portfolio = portfolio
        self.intraday_data = {}
        self.daily_data = {}
        self.monthly_data = {}
        self.yearly_data = {}

        startDate = datetime.combine(date.today(), time()) - timedelta(1095)
        endDate = datetime.combine(date.today(), time())
        self.get_historic_data(startDate, endDate)

    def __str__(self):
        return 'Portfolio: {}'.format(self.portfolio)

    def get_historic_data(self, startDate, endDate, period='daily'):
        new_tickers = [ticker for ticker in self.portfolio if ticker not in self.daily_data.keys()]
        sA = sa.StockApi(new_tickers)
        sA.get_data_pd_yahoo(startDate, endDate).to_csv('./what.csv')

