import os
import sys
import datetime
sys.path.append(os.path.abspath(os.path.join('..')))
sys.path.append(os.path.abspath(os.path.join('.')))
import paper_pants.data_collection.scraper.statement_scraper as ws
import paper_pants.data_collection.API.stock_api as sa

import paper_pants.technical_indicators.ohlcv_ti as ti
import pandas_datareader.data as pdr



pages = ['Balance Sheet', 'Income Statement', 'Cash Flow', 'Key Ratios']
companies = ['MSFT']
# startDate = datetime.combine(date.today(), time()) - timedelta(1095)
# endDate = datetime.combine(date.today(), time())


if __name__ == "__main__":
    # yh_ws = ws.StatementScraper(pages, companies)
    # print(yh_ws)
    # yh_ws.scrape_yahoo()

    # sA = sa.StockApi(companies, alpha_key_path='/app/api.key')
    # print(sA)
    # print(sA.get_data_pd_yahoo(startDate, endDate))
    # print(sA.get_data_yahoofinancials(startDate,endDate))
    # print(sA.get_data_alpha_vantage(startDate, endDate))

    ticker = "MSFT"
    ohlcv = pdr.get_data_yahoo(ticker, datetime.date.today() - datetime.timedelta(1825), datetime.date.today())

    # print(ti.macd(ohlcv, 12, 26, 9))
    # print(ti.atr(ohlcv, 20))
    # print(ti.bollinger_band(ohlcv, 20))
    # print(ti.rsi(ohlcv, 14))
    print(ti.adx(ohlcv, 14))
    # print(ti.obv(ohlcv))
    # print(ti.slope(ohlcv['Adj Close'], 5))
    # print(ti.renko(ohlcv))

