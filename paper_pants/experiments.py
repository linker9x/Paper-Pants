import os
import sys
from datetime import date, datetime, timedelta, time
sys.path.append(os.path.abspath(os.path.join('..')))
sys.path.append(os.path.abspath(os.path.join('.')))

import paper_pants.data_collection.API.stock_api as sa
import paper_pants.data_collection.scraper.statement_scraper as scraper
import paper_pants.trading_strategies.strategies as st
import paper_pants.portfolio.portfolio as pt

import pandas_datareader.data as pdr
import paper_pants.data_collection.value_investing.magic_formula as mf

pages = ['Balance Sheet', 'Income Statement', 'Cash Flow', 'Key Ratios']
companies = ["APX.AX", "AAPL"]
startDate = datetime.combine(date.today(), time()) - timedelta(1095)
endDate = datetime.combine(date.today(), time())


if __name__ == "__main__":
    # portfolio = pt.Portfolio(companies)
    # test_strategy = st.Strategy(portfolio, 'daily')
    # test_strategy.renko_macd()
    # test_strategy.calculate_return()
    # test_strategy.backtest()
    # print(test_strategy)

    sc = scraper.StatementScraper(companies)
    sc.scrape_yahoo_stats()
    sc.scrape_yahoo_statements()
    print(sc.financials)
    print(sc.stats)
    magic = mf.MagicFormula(sc.financials, sc.stats)
    # magic.print()