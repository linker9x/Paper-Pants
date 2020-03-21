import os
import sys
from datetime import date, datetime, timedelta, time
sys.path.append(os.path.abspath(os.path.join('..')))
sys.path.append(os.path.abspath(os.path.join('.')))
import paper_pants.data_collection.scraper.statement_scraper as ws

name = 'yahoo'
pages = ['Balance Sheet', 'Income Statement', 'Cash Flow', 'Key Ratios']
companies = ['AAPL', 'MSFT', 'IBM', 'HLT']

yh_ws = ws.StatementScraper(name, pages, companies)
print(yh_ws)
yh_ws.scrape_yahoo()

import paper_pants.data_collection.API.stock_api as sa
startDate = datetime.combine(date.today(), time()) - timedelta(1095)
endDate = datetime.combine(date.today(), time()) 
 

if __name__ == "__main__":
    sA = sa.StockApi(companies, alpha_key_path='/app/api.key')
    print(sA)
    print(sA.get_data_pd_yahoo(startDate, endDate ))
    print(sA.get_data_yahoofinancials(startDate,endDate))
    print(sA.get_data_alpha_vantage(startDate, endDate))
