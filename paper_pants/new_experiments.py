import os
import sys
from datetime import date, datetime, timedelta, time
from dateutil.relativedelta import relativedelta
sys.path.append(os.path.abspath(os.path.join('..')))
sys.path.append(os.path.abspath(os.path.join('.')))

from paper_pants.portfolio.portfolio import Portfolio
from paper_pants.trading_strategies.strategy.technical_strategies \
    import ResistanceBreakout, RenkoOBV, RenkoMACD, SMACrossover


if __name__ == "__main__":
    # tickers = ['MSFT', 'AAPL', 'IBM']
    # positions = {'MSFT': {'Position': 'Buy/Long',
    #                       'Size': 1},
    #              'AAPL': {'Position': 'Sell/Short',
    #                       'Size': 1},
    #              'IBM': {'Position': '',
    #                      'Size': 0}}
    # pf1 = Portfolio(tickers, positions)
    # print(pf1)
    #
    # end_dt = datetime.now()
    # start_dt = end_dt + relativedelta(months=-1)
    # stock_strategy = ResistanceBreakout(pf1, 'STOCK', start_dt, end_dt)
    # stock_strategy.generate_signals()
    # print(stock_strategy)

    pairs = ['EUR_USD', 'GBP_USD', 'USD_CHF', 'AUD_USD', 'USD_CAD']
    positions = {'EUR_USD': {'Position': 'Buy/Long',
                             'Size': 1},
                 'GBP_USD': {'Position': 'Buy/Long',
                             'Size': 1},
                 'USD_CHF': {'Position': '',
                             'Size': 0},
                 'AUD_USD': {'Position': 'Buy/Long',
                             'Size': 1},
                 'USD_CAD': {'Position': 'Buy/Long',
                             'Size': 1}}
    pf = Portfolio(pairs, positions)
    print(pf)

    # fx_end_dt = datetime.now()
    fx_end_dt = datetime(2020, 6, 12)
    fx_start_dt = fx_end_dt + relativedelta(minutes=-55)

    # fx_strategy = ResistanceBreakout(pf, 'FOREX', fx_start_dt, fx_end_dt)
    # fx_strategy = RenkoOBV(pf, 'FOREX', fx_start_dt, fx_end_dt)
    # fx_strategy = RenkoMACD(pf, 'FOREX', fx_start_dt, fx_end_dt)
    fx_strategy = SMACrossover(pf, 'FOREX', fx_start_dt, fx_end_dt)

    fx_strategy.generate_signals()
    print(fx_strategy)
