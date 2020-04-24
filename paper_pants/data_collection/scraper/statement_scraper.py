import requests
import os
import datetime
import re
import pandas as pd
from bs4 import BeautifulSoup

_yahoo = {
    'balance_sheet': '/balance-sheet?p=',
    'income_statement': '/financials?p=',
    'cash_flow': '/cash-flow?p=',
    'key_ratios': '/key-statistics?p='
}

class StatementScraper(object):
    """
    Class for scraper for financial statements (Balance Sheet, Income and Cash Flow Statements) and key ratios.

    ...

    Attributes
    ----------
    name : str
        the source to scrape (currently only yahoo)
    pages : list
        pages to be scraped from the source (Key Ratios, Balance Sheet, Income and Cash Flow Statements)
    tickers : list
        ticker name of tickers whose data should be scraped
    financials : dict
        dict containing the result of the scrape

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes | NOTE: Wait..., what? I will add this method if this comment stays here `=D
    """

    def __init__(self, tickers):
        """
        :param pages:
            pages to be scraped from the source (Key Ratios, Balance Sheet, Income and Cash Flow Statements)
        :param tickers:
            ticker name of tickers whose data should be scraped
        """

        self.name = 'yahoo'
        self.pages = ['key_ratios', 'balance_sheet', 'income_statement', 'cash_flow']
        self.tickers = tickers
        self.financials = None
        self.stats = None

    def __str__(self):
        return 'Name: {}, \nType: {}, \nTickers: {}'.format(self.name, self.pages, self.tickers)

    def __save_financials(self, ID):
        """
        Save the results of the scrape as a .csv file.

        :param ID:
            Append to file name (day, month, year _ hour, minute, second)
        :return:
        """
        if not self.financials.empty:
            filepath = '../data/statements_stats'
            if not os.path.exists(filepath):
                os.mkdir(filepath)

            financials_df = self.financials
            financials_df.to_csv(filepath + 'yahoo_webscrape_' + ID + '.csv', index=True, header=True)

    def scrape_yahoo_statements(self):
        """
        Scrapes selected Yahoo finance statement pages of selected tickers for the most recent annual figures.
        Page selection is stored in pages attr. Company selection is stored in tickers attr.
        """
        financial_df = None

        # Key Ratio HTML code is different from the HTML code for the statements, so it has to be scraped separately
        statements = [yp for yp in self.pages if yp in _yahoo and yp != 'key_ratios']

        # Currently IS, BS and CF
        for ticker in self.tickers:
            temp_dir = {}
            for ys in statements:
                url = 'https://in.finance.yahoo.com/quote/' + ticker + _yahoo[ys] + ticker # statement URL

                try:
                    page_content = requests.get(url, timeout=5).content
                    soup = BeautifulSoup(page_content, 'html.parser')

                    table = soup.find_all('div', {'class': 'W(100%) Whs(nw) Ovx(a) BdT Bdtc($seperatorColor)'})
                    for t in table:
                        header = t.find_all('div', {'class': 'D(tbhg)'})
                        for h in header:
                            date_row = h.get_text(separator='|').split("|")
                            temp_dir['FYE'] = [entry for entry in date_row if '/' in entry]
                        rows = t.find_all('div', {'data-test': 'fin-row'})
                        for r in rows:
                            cells = r.find_all('div', {'data-test': 'fin-col'})
                            # all of the rows with relevant information have 4-6 cells in them
                            if len(cells) in [4, 5, 6]:
                                row_text = r.get_text(separator='|').split("|")
                                position = row_text[0]
                                values = row_text[1:] if len(row_text) == 5 else row_text[-4:]
                                values = ['0' if entry == '-' else entry for entry in values]
                                temp_dir[position] = [float(entry.replace(',', '')) for entry in values]

                except requests.exceptions.ReadTimeout:
                    print('Request timed out')

            df = pd.DataFrame(temp_dir)
            df.set_index("FYE", inplace=True)
            df = df.transpose()
            df = pd.concat([df], keys=[ticker], axis=1)

            if financial_df is not None:
                financial_df = financial_df.join(df)
            else:
                financial_df = df

        self.financials = financial_df

        return financial_df

    def scrape_yahoo_stats(self):
        """
        Scrapes Yahoo finance key stats page of selected tickers for the most recent quarterly stats. Company
        selection is stored in tickers attr.
        """
        stats_df = None

        for ticker in self.tickers:
            temp_dir = {}
            url = 'https://in.finance.yahoo.com/quote/' + ticker + _yahoo['key_ratios'] + ticker # stats page url

            try:
                page_content = requests.get(url, timeout=5).content
                soup = BeautifulSoup(page_content, 'html.parser')

                table = soup.find_all('div', {'class': 'Pos(r) Mt(10px)'})
                for t in table:
                    rows = t.find_all('tr')
                    for r in rows:
                        row_text = r.get_text(separator='|').split("|")
                        # cell 0 has the key, cell -1 has the value (most recent fy end), empty text between
                        temp_dir[row_text[0]] = row_text[-1]

                df = pd.DataFrame(temp_dir, index=['Value'])
                df = df.transpose()
                df = pd.concat([df], keys=[ticker], axis=1)

                if stats_df is not None:
                    stats_df = stats_df.join(df)
                else:
                    stats_df = df

                self.stats = stats_df

            except requests.exceptions.ReadTimeout:
                print('Request timed out')

        return stats_df