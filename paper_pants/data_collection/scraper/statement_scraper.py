import requests
import pandas as pd
from bs4 import BeautifulSoup


class StatementScraper(object):
    def __init__(self, name, type, url, companies):
        self.name = name
        self.type = type
        self.url = url
        self.companies = companies
        self.statements = {}

    def __str__(self):
        return ('Name: %s, Type: %s, URL: %s, Companies: %s' % (self.name, self.type, self.url, self.companies))

    def save_dataframe(self):
        return None

    def get_statements(self):
        return None

    def scrape_yahoo_balance(self):
        temp_dir = {}

        for company in self.companies:
            bs_url = 'https://in.finance.yahoo.com/quote/' + company + '/balance-sheet?p=' + company
            page_content = requests.get(bs_url).content
            soup = BeautifulSoup(page_content, 'html.parser')
            table = soup.find_all('div', {'class': 'W(100%) Whs(nw) Ovx(a) BdT Bdtc($seperatorColor)'})

            for idx, t in enumerate(table):
                rows = t.find_all('div', {'data-test': 'fin-row'})
                for idxr, r in enumerate(rows):
                    cells = r.find_all('div', {'data-test': 'fin-col'})
                    if len(cells) == 4:
                        temp_dir[r.get_text(separator='|').split("|")[0]] = r.get_text(separator='|').split("|")[1]

        return temp_dir

