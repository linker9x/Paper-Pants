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
companies = ["AXP","AAPL"]
startDate = datetime.combine(date.today(), time()) - timedelta(1095)
endDate = datetime.combine(date.today(), time())


if __name__ == "__main__":
    tickers = ['MSFT']
    # portfolio = pt.Portfolio(tickers)
    # test_strategy = st.Strategy(portfolio, 'daily')
    # test_strategy.renko_macd()
    # test_strategy.calculate_return()
    # test_strategy.backtest()
    # print(test_strategy)
    sc = scraper.StatementScraper(tickers)
    sc.scrape_yahoo_stats()
    sc.scrape_yahoo_statements()
    print(sc.financials)
    print(sc.stats)
    yh_ws = ws.StatementScraper(pages, companies)
    combined = yh_ws.scrape_yahoo() 
    magic = mf.MagicFormula(combined)
    magic.print()
    # yh_ws.scrape_yahoo()
    #
    # sA = sa.StockApi(companies, alpha_key_path='/app/api.key')
    #
    # ohlcv = sA.get_data_pd_yahoo(startDate, endDate)
    # print('CAGR: {}'.format(CAGR(ohlcv['MSFT'], 'd' )))
    # print('Volatility: {}'.format(volatility(ohlcv['MSFT'], 'd' )))
    # print('Sharpe: {}'.format(sharpe(ohlcv['MSFT'], 'd', 0.022 )))
    # print('Sortino: {}'.format(sortino(ohlcv['MSFT'], 'd', 0.022 )))
    # print('MaxDD: {}'.format(max_dd(ohlcv['MSFT'] )))
    # print('Calmar: {}'.format(calmar(ohlcv['MSFT'], 'd' )))
    #



    # print(ti.macd(ohlcv, 12, 26, 9))
    # print(ti.atr(ohlcv, 20))
    # print(ti.bollinger_band(ohlcv, 20))
    # print(ti.rsi(ohlcv, 14))
    # print(ti.adx(ohlcv, 14))
    # print(ti.obv(ohlcv))
    # print(ti.slope(ohlcv, 5))
    # print(ti.renko(ohlcv))

    # tickers = ['MSFT', 'AAPL']
    # tickers_strategy = {}

    # for ticker in tickers:
    #     ohlcv = pdr.get_data_yahoo(ticker, startDate, endDate)
    #     st_ren_macd = st.Strategy(ohlcv)
    #     st_ren_macd.renko_macd()
    #     bt.Backtest(st_ren_macd)
    #     tickers_strategy[ticker] = st_ren_macd.df

    #     print(tickers_strategy[ticker])

    # st_rb = stgy.Strategy(ohlcv)
    # st_rb.resist_breakout()
    # print(bt.Backtest(st_rb))

    # st_ren_obv = stgy.Strategy(ohlcv)
    # st_ren_obv.renko_obv()
    # print(bt.Backtest(st_ren_obv))

    # st_ren_macd = st.Strategy(ohlcv)
    # st_ren_macd.renko_macd()
    # print(bt.Backtest(st_ren_macd))