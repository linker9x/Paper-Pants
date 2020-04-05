import os
import sys
import datetime
sys.path.append(os.path.abspath(os.path.join('..')))
sys.path.append(os.path.abspath(os.path.join('.')))
import paper_pants.data_collection.scraper.statement_scraper as ws
import paper_pants.data_collection.API.stock_api as sa

import paper_pants.metrics.technical_indicators as ti
import paper_pants.metrics.kpi_ffn as kpi

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

    ticker = "IBM"
    ohlcv = pdr.get_data_yahoo(ticker, datetime.date.today() - datetime.timedelta(1825), datetime.date.today())

    # TECHNICAL INDICATORS
    # print(ti.macd(ohlcv, 12, 26, 9))
    # print(ti.atr(ohlcv, 20))
    # print(ti.bollinger_band(ohlcv, 20))
    # print(ti.rsi(ohlcv, 14))
    # print(ti.adx(ohlcv, 14))
    # print(ti.obv(ohlcv))
    # print(ti.slope(ohlcv, 5))
    # print(ti.renko(ohlcv))

    # KPIS
    print("Org CAGR: {0:.2f}, ffn CAGR: {1:.2f}".format(*kpi.cagr(ohlcv)))
    print("Org Vol: {:.2f}".format(kpi.volatility(ohlcv)))
    print("Org Sharpe: {0:.2f},  ffn Sharpe: {1:.2f}".format(*kpi.sharpe(ohlcv, 0.022)))
    print("Org Sortino: {0:.2f},  ffn Sortino: {1:.2f}".format(*kpi.sortino(ohlcv, 0.022)))
    print("Org MaxDD: {0:.2f},  ffn MaxDD: {1:.2f}".format(*kpi.max_dd(ohlcv)))
    print("Org Calmar: {0:.2f},  ffn Calmar: {1:.2f}".format(*kpi.calmar(ohlcv)))
