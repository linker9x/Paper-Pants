import os
import sys
sys.path.append(os.path.abspath(os.path.join('..')))
sys.path.append(os.path.abspath(os.path.join('.')))
import paper_pants.data_collection.scraper.statement_scraper as ws

name = 'yahoo'
type = 'BS'
url = 'https://finance.yahoo.com/quote/'
companies = ['AAPL', 'MSFT']

for company in companies:
    bs_url = url + company
    yh_ws = ws.StatementScraper(name, type, 'https://finance.yahoo.com/quote/MSFT/balance-sheet?p=MSFT', companies)
    print(yh_ws)
    print(yh_ws.scrape_yahoo_balance())
