from typing import List
import pandas as pd 
import pandas_datareader.data as pdr 
from alpha_vantage.timeseries import TimeSeries

from yahoofinancials import YahooFinancials
import datetime 


class StockApi(object):
    """
        Get stock data from different stock apis
        
        Attributes
        ----------
        -

        Methods
        -------
        get_data_pd_yahoo(startDate, endDate, interval='d')
            Get stock data from yahoo finance api with pandareader
        get_data_zahoofinancials(startDate, endDate, interval='daily')
            Get stock data from yahoo finance api with yahoofinancials
        get_data_alpha_vantage(startDate, endDate, interval='1min')
            Get stock data from alpha vantage
    """

    def __init__(self, companies: List[str], attempts:int = 5, alpha_key_path:str = None):
        """
            Init the needed variables

            Parameters
            ----------
            companies: List[str]
                List of companies to get the data from
            attempts: int, default 5
                how often a fetch task should be retried if it fails 
            alpha_key_path: str, default None
                Path to the api key for alpha vantage
        """
        self._companies = companies
        self.__placeholderLength = max(len(company) for company in companies) + 10
        self._attempts = 5
        if not alpha_key_path is None:
            print('Try to load alpha api key...')
            try:
                self._alpha_key = open(alpha_key_path, 'r').read()
                self.__alpha_key_loaded = True
                print('Alpha key successful loaded')
            except:
                self.__alpha_key_loaded = False
                print('Alpha key failed to load')
        else:
            self.__alpha_key_loaded = False
        
        
        
    def __str__(self)->str:
        retStr = 'Companies:\n'
        retStr += '\n'.join(['{:>{width}}'.format(company, width=self.__placeholderLength) for company in self._companies])
        return retStr

    def __repr__(self)->str:
        return 'StockApi(' + repr(self._companies) + ', ' + self._attempts + ')'

    def get_data_pd_yahoo(self, startDate:datetime, endDate:datetime, interval:str = 'd')->pd.DataFrame:
        """
            Get the data for the companies with the pandareader yahoo function 
            
            Parameters
            ----------
            startDate: datetime 
                Starting date
            endDate: datetime
                Ending date
            interval: string, default 'd'
                Valid values are '1d', '5d', '1mo', '3mo', '6mo', '1y', '2y', '5y',
                    '10y', 'ytd', 'max'
            
            Returns
            -------
            pandas.Dataframe()


        """
        stock_data = pd.DataFrame() # dataframe to store close price of each ticker
        attempt = 0 # attempts to fetch the data
        drop = [] 
        tickers = [company for company in self._companies if company not in drop]
        print('Try to get data for the companies ({} - {})'.format(startDate, endDate))
        while len(tickers) != 0 and attempt <= self._attempts:
            if attempt > 0:
                print('Retry {} companies that failed...'.format(len(drop)))
            print('-----------------')
            print('Attempt: {}'.format(attempt + 1))
            print('-----------------')
            for i in range(len(tickers)):
                try:
                    tmpStockData = pdr.get_data_yahoo(tickers[i], startDate, endDate, interval=interval)
                    tmpStockData.dropna(inplace = True)
                    stock_data[tickers[i]] = tmpStockData['Adj Close']
                    drop.append(tickers[i])
                except:
                    print('\t{}: failed to fetch data'.format(tickers[i]))
            tickers = [company for company in self._companies if company not in drop]
            attempt += 1
        print('fetching data finished!')
        return stock_data.fillna(method='bfill', axis=0)

    def get_data_yahoofinancials(self, startDate:datetime, endDate:datetime, interval:str = 'daily')->pd.DataFrame:
        """
            Get the data for the companies with the yahoofinancials function
            
            Parameters
            ----------
            startDate: datetime 
                Starting date
            endDate: datetime
                Ending date
            interval: string, default 'daily'
                Valid values are 'daily', 'weekly', 'monthly'

            Returns
            -------
            pandas.Dataframe()

        """
        stock_data = pd.DataFrame() # dataframe to store close price of each ticker
        attempt = 0 # attempts to fetch the data
        drop = [] 
        tickers = [company for company in self._companies if company not in drop]
        print('Try to get data for the companies ({} - {})'.format(startDate, endDate))
        while len(tickers) != 0 and attempt <= self._attempts:
            if attempt > 0:
                print('Retry {} companies that failed...'.format(len(drop)))
            print('-----------------') 
            print('Attempt: {}'.format(attempt + 1))
            print('-----------------')
            for i in range(len(tickers)):
                try:
                    yahoo_financials = YahooFinancials(tickers[i])
                    json_response = yahoo_financials.get_historical_price_data(startDate.strftime('%Y-%m-%d'), endDate.strftime('%Y-%m-%d'), interval)
                    ohlv = json_response[tickers[i]]['prices']
                    tmpStockData = pd.DataFrame(ohlv)[['formatted_date', 'adjclose']]
                    tmpStockData.set_index('formatted_date', inplace=True)
                    tmpStockData2 = tmpStockData[~tmpStockData.index.duplicated(keep='first')]
                    stock_data[tickers[i]] = tmpStockData2['adjclose']
                    drop.append(tickers[i])
                except:
                    print('\t{}: failed to fetch data'.format(tickers[i]))
            tickers = [company for company in self._companies if company not in drop]
            attempt += 1
        print('fetching data finished!')
        return stock_data.fillna(method='bfill', axis=0)

    def get_data_alpha_vantage(self, startDate:datetime, endDate:datetime, interval:str = '1min')->pd.DataFrame:
        """
            Get the data for the companies with the alpha vantage function
            
            Parameters
            ----------
            startDate: datetime 
                Starting date
            endDate: datetime
                Ending date
            interval: string, default '1min'
                Valid values are '1min', '5min', '15min', '30min', '60min', 'daily', 'weekly', 'monthly'

            Returns
            -------
            pandas.Dataframe()

        """
        if not self.__alpha_key_loaded:
            print('No Alpha Vantage Api Key loaded')
            return pd.DataFrame()
        stock_data = pd.DataFrame() # dataframe to store close price of each ticker
        attempt = 0 # attempts to fetch the data
        drop = [] 
        tickers = [company for company in self._companies if company not in drop]
        print('Try to get data for the companies ({} - {})'.format(startDate, endDate))
        while len(tickers) != 0 and attempt <= self._attempts:
            if attempt > 0:
                print('Retry {} companies that failed...'.format(len(drop)))
            print('-----------------') 
            print('Attempt: {}'.format(attempt + 1))
            print('-----------------')
            for i in range(len(tickers)):
                try:
                    ts = TimeSeries(key=self._alpha_key, output_format='pandas')
                    if interval in ['1min', '5min', '15min', '30min', '60min']:
                        tmpStockData = ts.get_intraday(symbol=tickers[i], interval=interval, outputsize='full')[0]
                    elif interval == 'daily':
                        tmpStockData = ts.get_daily(symbol=tickers[i], outputsize='full')[0]
                    elif interval == 'weekly':
                        tmpStockData = ts.get_weekly(symbol=tickers[i])[0]
                    elif interval == 'monthly':
                        tmpStockData = ts.get_monthly(symbol=tickers[i])[0]
                    else:
                        print('wrong interval')
                        return pd.DataFrame()
                    tmpStockData.columns = ['open', 'high', 'low', 'close', 'volume']                  
                    stock_data[tickers[i]] = tmpStockData['close']
                    drop.append(tickers[i])
                except:
                    print('\t{}: failed to fetch data'.format(tickers[i]))
            tickers = [company for company in self._companies if company not in drop]
            attempt += 1
        print('fetching data finished!')
        return stock_data.fillna(method='bfill', axis=0)

   