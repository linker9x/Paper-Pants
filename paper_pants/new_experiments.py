import os
import sys
from datetime import date, datetime, timedelta, time
sys.path.append(os.path.abspath(os.path.join('..')))
sys.path.append(os.path.abspath(os.path.join('.')))

from paper_pants.trading_strategies.strategy.general_strategy import *


if __name__ == "__main__":
    strategy = Strategy(['MSFT', 'AAPL'], 'STOCK', '2020-01-01', '2020-05-31', 'StrategyName')
    print(strategy)
