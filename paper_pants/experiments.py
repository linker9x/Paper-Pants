import os
import sys
sys.path.append(os.path.abspath(os.path.join('..')))
sys.path.append(os.path.abspath(os.path.join('.')))
import paper_pants.data_collection.scraper.statement_scraper as ws

name = 'yahoo'
pages = ['Balance Sheet', 'Income Statement', 'Cash Flow', 'Key Ratios']
companies = ['AAPL', 'MSFT', 'IBM', 'HLT']

yh_ws = ws.StatementScraper(name, pages, companies)
print(yh_ws)
yh_ws.scrape_yahoo()

