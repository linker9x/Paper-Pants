import os
import sys
from datetime import date, datetime, timedelta, time
sys.path.append(os.path.abspath(os.path.join('..')))
sys.path.append(os.path.abspath(os.path.join('.')))
import paper_pants.data_collection.scraper.statement_scraper as ws
import paper_pants.data_collection.API.stock_api as sa
startDate = datetime.combine(date.today(), time()) - timedelta(1095)
endDate = datetime.combine(date.today(), time()) 
# name = 'yahoo'
# type = 'BS'
# url = 'https://finance.yahoo.com/quote/'
companies = ['AAPL', 'MSFT']

# for company in companies:
#     bs_url = url + company
#     yh_ws = ws.StatementScraper(name, type, 'https://finance.yahoo.com/quote/MSFT/balance-sheet?p=MSFT', companies)
#     print(yh_ws)
#     print(yh_ws.scrape_yahoo_balance())


if __name__ == "__main__":
    sA = sa.StockApi(companies, alpha_key_path='/app/api.key')
    print(sA)
    print(sA.get_data_pd_yahoo(startDate, endDate ))
    print(sA.get_data_yahoofinancials(startDate,endDate))
    print(sA.get_data_alpha_vantage(startDate, endDate))