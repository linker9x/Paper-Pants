import paper_pants.trading_strategies.strategies.technical_indicators.ohlcv_ti as ti
import paper_pants.trading_strategies.backtesting.kpis.kpi as kpi
import copy
import numpy as np
import pandas as pd

_kpis = {'CAGR' : kpi.CAGR, 'volatility': kpi.volatility, 'sharpe': kpi.sharpe, 'sortino': kpi.sortino,
         'max_dd': kpi.max_dd, 'calmar': kpi.calmar}

_tis = {'macd' : ti.macd, 'atr' : ti.atr, 'bollinger_band' : ti.bollinger_band,
        'rsi' : ti.rsi, 'adx' : ti.adx, 'obv' : ti.obv, 'slope' : ti.slope, 'renko' : ti.renko}

_strategies = ['rebalancing', 'resist_breakout', 'renko_obv', 'renko_macd']

class Strategy(object):
    def __init__(self, portfolio, period='daily'):
        self.portfolio = portfolio
        self.df = None
        self.name = None
        self.period = period
        self.kpis = {}

        self._calculate_all_tis()

    def __str__(self):
        return 'Strategy: {}, Period: {}, KPIs: {} \n df: {}'.format(self.name, self.period, self.kpis, self.df)

    def _calculate_all_tis(self):
        hd_df = self.portfolio.historic_data[self.period]
        ti_df = None

        for ticker in hd_df.stack(level=1).keys():
            ticker_df = copy.deepcopy(hd_df[ticker])
            for t_ind in _tis:
                # print(ticker_df)
                ticker_df = ticker_df.join(_tis[t_ind](ticker_df))

                temp_df = ticker_df[~ticker_df.index.duplicated(keep='first')]
                temp_df = pd.concat([temp_df], keys=[ticker], axis=1)

            if ti_df is not None:
                ti_df = ti_df.join(temp_df)
            else:
                ti_df = temp_df

        self.df = ti_df
        # ti_df.to_csv('./look.csv')

    def rebalancing(self):
        return None

    def resist_breakout(self):
        df = self.df
        self.name = 'resist_breakout'
        rb_df = None

        for ticker in df.stack(level=1).keys():
            ticker_df = copy.deepcopy(df[ticker])

            ticker_df["roll_max_high"] = ticker_df["High"].rolling(20).max()
            ticker_df["roll_min_low"] = ticker_df["Low"].rolling(20).min()
            ticker_df["roll_max_vol"] = ticker_df["Volume"].rolling(20).max()

            cur_signal = ['']
            new_signal = []
            print(ticker_df)
            for i in range(len(ticker_df)):

                if cur_signal[i] == '':
                    print(ticker_df["Volume"][i] > 1.5 * ticker_df["roll_max_vol"][i-1])
                    if ticker_df["High"][i] >= ticker_df["roll_max_high"][i] and ticker_df["Volume"][i] > 1.5 * ticker_df["roll_max_vol"][i-1]:
                        next_pos = "Buy/Long"
                    elif ticker_df["Low"][i] <= ticker_df["roll_min_low"][i] and ticker_df["Volume"][i] > 1.5 * ticker_df["roll_max_vol"][i-1]:
                        next_pos = "Sell/Short"
                    else:
                        next_pos = cur_signal[i]

                elif cur_signal[i] == "Buy/Long":
                    if ticker_df["Close"][i] < ticker_df["Close"][i-1] - ticker_df["atr"][i-1]:
                        next_pos = ""
                    elif ticker_df["Low"][i] <= ticker_df["roll_min_low"][i] and ticker_df["Volume"][i] > 1.5 * ticker_df["roll_max_vol"][i-1]:
                        next_pos = "Sell/Short"
                    else:
                        next_pos = cur_signal[i]

                elif cur_signal[i] == "Sell/Short":
                    if ticker_df["Close"][i] > ticker_df["Close"][i-1] + ticker_df["atr"][i-1]:
                        next_pos = ""
                    elif ticker_df["High"][i] >= ticker_df["roll_max_high"][i] and ticker_df["Volume"][i] > 1.5 * ticker_df["roll_max_vol"][i-1]:
                        next_pos = "Buy/Long"
                    else:
                        next_pos = cur_signal[i]

                new_signal.append(next_pos)
                cur_signal.append(next_pos)


            ticker_df["cur_signal"] = np.array(cur_signal[:len(ticker_df)])
            ticker_df["new_signal"] = np.array(new_signal)

            temp_df = ticker_df[~ticker_df.index.duplicated(keep='first')]
            temp_df = pd.concat([temp_df], keys=[ticker], axis=1)

            if rb_df is not None:
                rb_df = rb_df.join(temp_df)
            else:
                rb_df = temp_df

        self.df = rb_df
        rb_df.to_csv('./rb_df.csv')

    #
    # def renko_obv(self):
    #     df = self.df
    #     self.name = 'renko_obv'
    #
    #     df["obv_slope"] = ti.slope(df, col_name='obv')
    #
    #     cur_signal = ['']
    #     new_signal = []
    #     for i in range(len(df)):
    #         if cur_signal[i] == "":
    #             if df["renko_bar_num"][i] >= 2 and df["obv_slope"][i] > 30:
    #                 next_pos = "Buy/Long"
    #             elif df["renko_bar_num"][i] <= -2 and df["obv_slope"][i] < -30:
    #                 next_pos = "Sell/Short"
    #             else:
    #                 next_pos = cur_signal[i]
    #
    #         elif cur_signal[i] == "Buy/Long":
    #             if df["renko_bar_num"][i] <= -2 and df["obv_slope"][i] < -30:
    #                 next_pos = "Sell/Short"
    #             elif df["renko_bar_num"][i] < 2:
    #                 next_pos = ""
    #             else:
    #                 next_pos = cur_signal[i]
    #
    #         elif cur_signal[i] == "Sell/Short":
    #             if df["renko_bar_num"][i] >= 2 and df["obv_slope"][i] > 30:
    #                 next_pos = "Buy/Long"
    #             elif df["renko_bar_num"][i] > -2:
    #                 next_pos = ""
    #             else:
    #                 next_pos = cur_signal[i]
    #
    #         new_signal.append(next_pos)
    #         cur_signal.append(next_pos)
    #
    #     df["cur_signal"] = np.array(cur_signal[:len(df)])
    #     df["new_signal"] = np.array(new_signal)
    #
    #     self.df = df
    #     #df.to_csv('./look.csv')
    #
    # def renko_macd(self):
    #     df = self.df
    #     self.name = 'renko_macd'
    #
    #     df["macd_slope"] = ti.slope(df, col_name='macd')
    #     df["macd_sig_slope"] = ti.slope(df, col_name='macd_signal')
    #
    #     cur_signal = ['']
    #     new_signal = []
    #     for i in range(len(df)):
    #         if cur_signal[i] == "":
    #             if df["renko_bar_num"][i] >= 2 and df["macd"][i] > df["macd_signal"][i] \
    #                     and df["macd_slope"][i] > df["macd_sig_slope"][i]:
    #                 next_pos = "Buy/Long"
    #             elif df["renko_bar_num"][i] <= -2 and df["macd"][i] < df["macd_signal"][i] \
    #                     and df["macd_slope"][i] < df["macd_sig_slope"][i]:
    #                 next_pos = "Sell/Short"
    #             else:
    #                 next_pos = cur_signal[i]
    #
    #         elif cur_signal[i] == "Buy/Long":
    #             if df["renko_bar_num"][i] <= -2 and df["macd"][i] < df["macd_signal"][i] \
    #                     and df["macd_slope"][i] < df["macd_sig_slope"][i]:
    #                 next_pos = "Sell/Short"
    #             elif df["macd"][i] < df["macd_signal"][i] and df["macd_slope"][i] < df["macd_sig_slope"][i]:
    #                 next_pos = ""
    #             else:
    #                 next_pos = cur_signal[i]
    #
    #         elif cur_signal[i] == "Sell/Short":
    #             if df["renko_bar_num"][i] >= 2 and df["macd"][i] > df["macd_signal"][i] and \
    #                     df["macd_slope"][i] > df["macd_sig_slope"][i]:
    #                 next_pos = "Buy/Long"
    #             elif df["macd"][i] > df["macd_signal"][i] and df["macd_slope"][i] > df["macd_sig_slope"][i]:
    #                 next_pos = ""
    #             else:
    #                 next_pos = cur_signal[i]
    #
    #         new_signal.append(next_pos)
    #         cur_signal.append(next_pos)
    #
    #     df["cur_signal"] = np.array(cur_signal[:len(df)])
    #     df["new_signal"] = np.array(new_signal)
    #
    #     self.df = df
    #     #df.to_csv('./look.csv')

    # def _calculate_return(self, type='normal'):
    #     df = df
    #     ret_col = []
    #
    #     for i in range(len(df)):
    #         if df['cur_signal'][i] == "":
    #             ret_col.append(0)
    #         elif df['cur_signal'][i] == "Buy/Long":
    #             ret_col.append((df["Adj Close"][i]/df["Adj Close"][i-1]) - 1)
    #         elif df['cur_signal'][i] == "Sell/Short":
    #             ret_col.append((df["Adj Close"][i-1] / df["Adj Close"][i]) - 1)
    #
    #     df["ret"] = np.array(ret_col)
    #     df['cum_return'] = (1 + df['ret']).cumprod() # I think the one is the investment
    #
    # def _calculate_all_kpis(self):
    #     df = df
    #     kpis = self.kpis
    #
    #     for ki in _kpis:
    #         if ki != 'max_dd':
    #             kpis[ki] = _kpis[ki](df, self.period)
    #         else:
    #             kpis[ki] = _kpis[ki](df)
    #
    #     self.kpis = kpis
