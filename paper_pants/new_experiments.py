import os
import sys
from datetime import date, datetime, timedelta, time
sys.path.append(os.path.abspath(os.path.join('..')))
sys.path.append(os.path.abspath(os.path.join('.')))

from paper_pants.trading_strategies.strategy.technical_strategies \
    import ResistanceBreakout#, RenkoOBV, RenkoMACD, SMACrossover


if __name__ == "__main__":
    positions = {'MSFT': {'Position': 'Buy/Long',
                          'Size': 1},
                 'AAPL': {'Position': 'Buy/Long',
                          'Size': 1},
                 'IBM': {'Position': '',
                         'Size': 0}}
    print(positions.keys())
    strategy = ResistanceBreakout(positions.keys(), 'STOCK', '2020-03-31')
    print(strategy)
    print(strategy.generate_signal())

