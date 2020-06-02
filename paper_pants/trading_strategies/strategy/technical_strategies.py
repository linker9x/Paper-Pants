from paper_pants.trading_strategies.strategy.general_strategy import Strategy
import paper_pants.trading_strategies.technical_indicators.ohlcv_ti as ti


class ResistanceBreakout(Strategy):
    def __init__(self, portfolio, type, start_date, end_date):
        tis = {'atr': ti.atr}
        Strategy.__init__(self, portfolio, type, start_date, end_date, 'ResistanceBreakout', tis=tis)

    def generate_signal(self):
        pass


class RenkoOBV(Strategy):
    def __init__(self, portfolio, type, start_date, end_date):
        tis = {'renko': ti.renko}
        Strategy.__init__(self, portfolio, type, start_date, end_date, 'RenkoOBV', tis=tis)

    def generate_signal(self):
        pass


class RenkoMACD(Strategy):
    def __init__(self, portfolio, type, start_date, end_date):
        tis = {'renko': ti.renko}
        Strategy.__init__(self, portfolio, type, start_date, end_date, 'RenkoMACD', tis=tis)

    def generate_signal(self):
        pass


class SMACrossover(Strategy):
    def __init__(self, portfolio, type, start_date, end_date):
        tis = {}
        Strategy.__init__(self, portfolio, type, start_date, end_date, 'SMACrossover', tis=tis)

    def generate_signal(self):
        pass
