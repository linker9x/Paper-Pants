import requests
import pandas as pd
from bs4 import BeautifulSoup

yahoo = {
    'Balance Sheet': '/balance-sheet?p=',
    'Income Statement': '/financials?p=',
    'Cash Flow': '/cash-flow?p=',
    'Key Ratios': '/key-statistics?p='
}

class StatementScraper(object):
    def __init__(self, name, pages, companies):
        self.name = name
        self.pages = pages
        self.companies = companies
        self.financials = {}

    def __str__(self):
        return ('Name: %s, Type: %s, Companies: %s' % (self.name, self.pages, self.companies))


    def scrape_yahoo_statements(self):
        statements = [yp for yp in self.pages if yp in yahoo and yp != 'Key Ratios']

        for ys in statements:
            for company in self.companies:
                temp_dir = {}
                bs_url = 'https://in.finance.yahoo.com/quote/' + company + yahoo[ys] + company
                page_content = requests.get(bs_url).content
                soup = BeautifulSoup(page_content, 'html.parser')

                table = soup.find_all('div', {'class': 'W(100%) Whs(nw) Ovx(a) BdT Bdtc($seperatorColor)'})
                for t in table:
                    header = t.find_all('div', {'class': 'D(tbhg)'})
                    for h in header:
                        temp_dir[ys + ' Financial Year'] = h.get_text(separator='|').split("|")[1]

                    rows = t.find_all('div', {'data-test': 'fin-row'})
                    for r in rows:
                        cells = r.find_all('div', {'data-test': 'fin-col'})
                        if len(cells) in [4, 5, 6]:
                            row_text = r.get_text(separator='|').split("|")
                            temp_dir[row_text[0]] = row_text[1]

                if company in self.financials:
                    self.financials[company].update(temp_dir)
                else:
                    self.financials[company] = temp_dir

        return None

    def scrape_yahoo_stats(self):
        for company in self.companies:
            temp_dir = {}
            bs_url = 'https://in.finance.yahoo.com/quote/' + company + yahoo['Key Ratios'] + company
            page_content = requests.get(bs_url).content
            soup = BeautifulSoup(page_content, 'html.parser')

            table = soup.find_all('div', {'class': 'Pos(r) Mt(10px)'})
            for t in table:
                rows = t.find_all('tr')

                for r in rows:
                    row_text = r.get_text(separator='|').split("|")
                    temp_dir[row_text[0]] = row_text[-1]

            if company in self.financials:
                self.financials[company].update(temp_dir)
            else:
                self.financials[company] = temp_dir

        return None

    def scrape_yahoo(self):
        if 'Key Ratios' in self.pages:
            self.scrape_yahoo_stats()

        self.scrape_yahoo_statements()

        print(self.financials)

        combined_financials = pd.DataFrame(self.financials)
        combined_financials.to_csv('./export_webscrape.csv', index=True, header=True)