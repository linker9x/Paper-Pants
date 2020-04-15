import os
import sys
from datetime import date, datetime, timedelta, time
sys.path.append(os.path.abspath(os.path.join('..')))
sys.path.append(os.path.abspath(os.path.join('.')))

import paper_pants.data_collection.API.stock_api as sa
import paper_pants.trading_strategies.strategies as st
import paper_pants.portfolio.portfolio as pt

pages = ['Balance Sheet', 'Income Statement', 'Cash Flow', 'Key Ratios']
companies = ['MSFT']
startDate = datetime.combine(date.today(), time()) - timedelta(1095)
endDate = datetime.combine(date.today(), time())


if __name__ == "__main__":
    tickers = ['MSFT', 'AAPL']
    portfolio = pt.Portfolio(tickers)
    test_strategy = st.Strategy(portfolio, 'daily')
    test_strategy.renko_macd()
    test_strategy.calculate_return()
    test_strategy.backtest()
    print(test_strategy)

