import paper_pants.trading_strategies.strategies.strategies as st
import paper_pants.trading_strategies.backtesting.kpis.kpi as kpi
import numpy as np
import copy

_kpis = {'CAGR' : kpi.CAGR, 'volatility': kpi.volatility, 'sharpe': kpi.sharpe, 'sortino': kpi.sortino,
         'max_dd': kpi.max_dd, 'calmar': kpi.calmar}

class Backtest(st.Strategy):
    def __init__(self, strategy, period='daily'):
        self.strategy = strategy
        self.period = period
        self.kpis = {}

        self._calculate_return()
        self._calculate_all_ratios()

    def __str__(self):
        return 'Name: {}, Period: {}, KPIs: {}'.format(self.strategy.name, self.period, self.kpis)

    def _calculate_return(self, type='normal'):
        df = self.strategy.df
        ret_col = []

        for i in range(len(df)):
            if df['cur_signal'][i] == "":
                ret_col.append(0)
            elif df['cur_signal'][i] == "Buy/Long":
                ret_col.append((df["Adj Close"][i]/df["Adj Close"][i-1]) - 1)
            elif df['cur_signal'][i] == "Sell/Short":
                ret_col.append((df["Adj Close"][i-1] / df["Adj Close"][i]) - 1)

        df["ret"] = np.array(ret_col)
        df['cum_return'] = (1 + df['ret']).cumprod() # I think the one is the investment

    def _calculate_all_ratios(self):
        df = self.strategy.df
        kpis = self.kpis

        for ki in _kpis:
            if ki != 'max_dd':
                kpis[ki] = _kpis[ki](df, self.period)
            else:
                kpis[ki] = _kpis[ki](df)

        self.kpis = kpis