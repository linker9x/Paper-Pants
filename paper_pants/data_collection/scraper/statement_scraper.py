import requests
import os
import datetime
import pandas as pd
from bs4 import BeautifulSoup

yahoo = {
    'Balance Sheet': '/balance-sheet?p=',
    'Income Statement': '/financials?p=',
    'Cash Flow': '/cash-flow?p=',
    'Key Ratios': '/key-statistics?p='
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
    companies : list
        ticker name of companies whose data should be scraped
    financials : dict
        dict containing the result of the scrape

    Methods
    -------
    says(sound=None)
        Prints the animals name and what sound it makes
    """

    def __init__(self, pages, companies):
        """
        :param pages:
            pages to be scraped from the source (Key Ratios, Balance Sheet, Income and Cash Flow Statements)
        :param companies:
            ticker name of companies whose data should be scraped
        """

        self.name = 'yahoo'
        self.pages = pages
        self.companies = companies
        self.financials = {}

    def __str__(self):
        return ('Name: %s, Type: %s, Companies: %s' % (self.name, self.pages, self.companies))

    def __save_financials(self, ID):
        """
        Save the results of the scrape as a .csv file.

        :param ID:
            Append to file name (day, month, year _ hour, minute, second)
        :return:
        """
        if self.financials:
            filepath = '../statements_stats_data/'
            if not os.path.exists(filepath):
                os.mkdir(filepath)

            combined_financials = pd.DataFrame(self.financials)
            combined_financials.to_csv(filepath + 'yahoo_webscrape_' + ID + '.csv', index=True, header=True)

    def __scrape_yahoo_statements(self):
        """
        Scrapes selected Yahoo finance statement pages of selected companies for the most recent annual figures.
        Page selection is stored in pages attr. Company selection is stored in companies attr.
        """

        # Key Ratio HTML code is different from the HTML code for the statements, so it has to be scraped separately
        statements = [yp for yp in self.pages if yp in yahoo and yp != 'Key Ratios']

        # Currently IS, BS and CF
        for ys in statements:
            for company in self.companies:
                temp_dir = {}   #holds the scraped data for the current iteration
                url = 'https://in.finance.yahoo.com/quote/' + company + yahoo[ys] + company # statement URL

                try:
                    page_content = requests.get(url, timeout=5).content
                    soup = BeautifulSoup(page_content, 'html.parser')

                    table = soup.find_all('div', {'class': 'W(100%) Whs(nw) Ovx(a) BdT Bdtc($seperatorColor)'})
                    for t in table:
                        header = t.find_all('div', {'class': 'D(tbhg)'})
                        for h in header:
                            temp_dir[ys + ' Financial Year'] = h.get_text(separator='|').split("|")[1] # save fy

                        rows = t.find_all('div', {'data-test': 'fin-row'})
                        for r in rows:
                            cells = r.find_all('div', {'data-test': 'fin-col'})
                            # all of the rows with relevant information have 4-6 cells in them
                            if len(cells) in [4, 5, 6]:
                                row_text = r.get_text(separator='|').split("|")
                                # cell 0 has the key, cell 1 has the value (most recent fy end)
                                temp_dir[row_text[0]] = row_text[1]

                    if company in self.financials:
                        self.financials[company].update(temp_dir)
                    else:
                        self.financials[company] = temp_dir

                except requests.exceptions.ReadTimeout:
                    print('Request timed out')

        return None

    def __scrape_yahoo_stats(self):
        """
        Scrapes Yahoo finance key stats page of selected companies for the most recent quarterly stats. Company
        selection is stored in companies attr.
        """

        for company in self.companies:
            temp_dir = {}
            url = 'https://in.finance.yahoo.com/quote/' + company + yahoo['Key Ratios'] + company # stats page url

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

                if company in self.financials:
                    self.financials[company].update(temp_dir)
                else:
                    self.financials[company] = temp_dir

            except requests.exceptions.ReadTimeout:
                print('Request timed out')

        return None

    def scrape_yahoo(self):
        """
        Scrapes selected Yahoo finance statement and/or stats pages of selected companies for the most recent annual
        figures and quarterly stats. Page selection is stored in pages attr. Company selection is stored in
        companies attr.
        """

        if not self.pages:
            raise Exception('There are no pages to scrape.')

        if not self.companies:
            raise Exception('There are no companies to scrape for.')

        if 'Key Ratios' in self.pages:
            self.__scrape_yahoo_stats()

        self.__scrape_yahoo_statements()

        self.__save_financials(datetime.datetime.now().strftime("%d%m%Y_%H%M%S"))

