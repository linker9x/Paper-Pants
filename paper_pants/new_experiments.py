import os
import sys
from datetime import date, datetime, timedelta, time
sys.path.append(os.path.abspath(os.path.join('..')))
sys.path.append(os.path.abspath(os.path.join('.')))

from paper_pants.trading_strategies.strategy.technical_strategies \
    import ResistanceBreakout, RenkoOBV, RenkoMACD, SMACrossover


if __name__ == "__main__":
    strategy1 = ResistanceBreakout(['MSFT', 'AAPL'], 'STOCK', '2020-01-01', '2020-05-31')
    strategy2 = RenkoOBV(['MSFT', 'AAPL'], 'STOCK', '2020-01-01', '2020-05-31')
    strategy3 = RenkoMACD(['MSFT', 'AAPL'], 'STOCK', '2020-01-01', '2020-05-31')
    strategy4 = SMACrossover(['MSFT', 'AAPL'], 'STOCK', '2020-01-01', '2020-05-31')
    print(strategy1)
    print(strategy2)
    print(strategy3)
    print(strategy4)
