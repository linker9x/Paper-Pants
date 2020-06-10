import os
import sys
from datetime import date, datetime, timedelta, time
from dateutil.relativedelta import relativedelta
sys.path.append(os.path.abspath(os.path.join('..')))
sys.path.append(os.path.abspath(os.path.join('.')))

from paper_pants.trading_strategies.strategy.technical_strategies \
    import ResistanceBreakout#, RenkoOBV, RenkoMACD, SMACrossover


if __name__ == "__main__":
    # positions = {'MSFT': {'Position': 'Buy/Long',
    #                       'Size': 1},
    #              'AAPL': {'Position': 'Sell/Short',
    #                       'Size': 1},
    #              'IBM': {'Position': '',
    #                      'Size': 0}}
    # print(positions.keys())
    #
    # end_dt = datetime.now()
    # start_dt = end_dt + relativedelta(months=-1)
    # stock_strategy = ResistanceBreakout(positions.keys(), 'STOCK', start_dt, end_dt)
    # print(stock_strategy)
    # print(stock_strategy.generate_signal())

    pairs = {'EUR_USD': {'Position': 'Buy/Long',
                          'Size': 1},
             'GBP_USD': {'Position': 'Sell/Short',
                          'Size': 1},
             'USD_CHF': {'Position': '',
                          'Size': 0},
             'AUD_USD': {'Position': 'Buy/Long',
                          'Size': 1},
             'USD_CAD': {'Position': 'Sell/Short',
                          'Size': 1}}
    print(pairs.keys())

    fx_end_dt = datetime.now()
    fx_start_dt = fx_end_dt + relativedelta(minutes=-10)
    fx_strategy = ResistanceBreakout(pairs.keys(), 'FOREX', fx_start_dt, fx_end_dt)
    print(fx_strategy)
