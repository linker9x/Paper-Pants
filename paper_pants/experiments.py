import os
import sys
from  datetime import date, datetime, timedelta, time
sys.path.append(os.path.abspath(os.path.join('..')))
sys.path.append(os.path.abspath(os.path.join('.')))
import paper_pants.data_collection.scraper.statement_scraper as ws
import paper_pants.data_collection.API.stock_api as sa

import paper_pants.technical_indicators.ohlcv_ti as ti
import pandas_datareader.data as pdr
from paper_pants.data_collection.performance_measurement.kpi import CAGR, volatility, sharpe, sortino, max_dd, calmar\


pages = ['Balance Sheet', 'Income Statement', 'Cash Flow', 'Key Ratios']
companies = ['MSFT']
startDate = datetime.combine(date.today(), time()) - timedelta(1095)
endDate = datetime.combine(date.today(), time())


if __name__ == "__main__":
    # yh_ws = ws.StatementScraper(pages, companies)
    # print(yh_ws)
    # yh_ws.scrape_yahoo()

    sA = sa.StockApi(companies, alpha_key_path='/app/api.key')
    
    ohlcv = sA.get_data_pd_yahoo(startDate, endDate) 

    print('CAGR: {}'.format(CAGR(ohlcv['MSFT'], 'd' )))
    print('Volatility: {}'.format(volatility(ohlcv['MSFT'], 'd' )))
    print('Shapre: {}'.format(sharpe(ohlcv['MSFT'], 'd', 0.022 )))
    print('Sortino: {}'.format(sortino(ohlcv['MSFT'], 'd', 0.022 )))
    print('MaxDD: {}'.format(max_dd(ohlcv['MSFT'] )))
    print('Calmar: {}'.format(calmar(ohlcv['MSFT'], 'd' )))


    #print(sA.get_data_yahoofinancials(startDate,endDate))
    #print(sA.get_data_alpha_vantage(startDate, endDate))

    ticker = ["MSFT", "AAPL"]
    ohlcv = pdr.get_data_yahoo(ticker, date.today() - timedelta(1825), date.today())


    # print(ti.macd(ohlcv, 12, 26, 9))
    # print(ti.atr(ohlcv, 20))
    # print(ti.bollinger_band(ohlcv, 20))
    # print(ti.rsi(ohlcv, 14))
    # print(ti.adx(ohlcv, 14))
    # print(ti.obv(ohlcv))
    # print(ti.slope(ohlcv, 5))
    # print(ti.renko(ohlcv))

