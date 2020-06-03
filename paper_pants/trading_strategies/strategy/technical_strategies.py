from paper_pants.trading_strategies.strategy.general_strategy import Strategy
import paper_pants.trading_strategies.technical_indicators.ohlcv_ti as ti


class ResistanceBreakout(Strategy):
    def __init__(self, portfolio, type, end_date):
        tis = {'atr': ti.atr}
        Strategy.__init__(self, portfolio, type, end_date, offset=-1, tis=tis)


    def generate_signal(self):

        # df = self.df
        # self.name = 'resist_breakout'
        # rb_df = None
        #
        # for ticker in df.stack(level=1).keys():
        #     ticker_df = copy.deepcopy(df[ticker])
        #
        #     ticker_df["roll_max_high"] = ticker_df["High"].rolling(20).max()
        #     ticker_df["roll_min_low"] = ticker_df["Low"].rolling(20).min()
        #     ticker_df["roll_max_vol"] = ticker_df["Volume"].rolling(20).max()
        #
        #     cur_signal = ['']
        #     new_signal = []
        #
        #     for i in range(len(ticker_df)):
        #         if cur_signal[i] == '':
        #             if ticker_df["High"][i] >= ticker_df["roll_max_high"][i] and ticker_df["Volume"][i] > 1.5 * \
        #                     ticker_df["roll_max_vol"][i - 1]:
        #                 next_pos = "Buy/Long"
        #             elif ticker_df["Low"][i] <= ticker_df["roll_min_low"][i] and ticker_df["Volume"][i] > 1.5 * \
        #                     ticker_df["roll_max_vol"][i - 1]:
        #                 next_pos = "Sell/Short"
        #             else:
        #                 next_pos = cur_signal[i]
        #
        #         elif cur_signal[i] == "Buy/Long":
        #             if ticker_df["Close"][i] < ticker_df["Close"][i - 1] - ticker_df["atr"][i - 1]:
        #                 next_pos = ""
        #             elif ticker_df["Low"][i] <= ticker_df["roll_min_low"][i] and ticker_df["Volume"][i] > 1.5 * \
        #                     ticker_df["roll_max_vol"][i - 1]:
        #                 next_pos = "Sell/Short"
        #             else:
        #                 next_pos = cur_signal[i]
        #
        #         elif cur_signal[i] == "Sell/Short":
        #             if ticker_df["Close"][i] > ticker_df["Close"][i - 1] + ticker_df["atr"][i - 1]:
        #                 next_pos = ""
        #             elif ticker_df["High"][i] >= ticker_df["roll_max_high"][i] and ticker_df["Volume"][i] > 1.5 * \
        #                     ticker_df["roll_max_vol"][i - 1]:
        #                 next_pos = "Buy/Long"
        #             else:
        #                 next_pos = cur_signal[i]
        #
        #         new_signal.append(next_pos)
        #         cur_signal.append(next_pos)
        #
        #     ticker_df["cur_signal"] = np.array(cur_signal[:len(ticker_df)])
        #     ticker_df["new_signal"] = np.array(new_signal)
        #
        #     temp_df = ticker_df[~ticker_df.index.duplicated(keep='first')]
        #     temp_df = pd.concat([temp_df], keys=[ticker], axis=1)
        #
        #     if rb_df is not None:
        #         rb_df = rb_df.join(temp_df)
        #     else:
        #         rb_df = temp_df
        #
        # self.df = rb_df
        return 'cat'


# class RenkoOBV(Strategy):
#     def __init__(self, portfolio, type, start_date, end_date):
#         tis = {'renko': ti.renko}
#         Strategy.__init__(self, portfolio, type, start_date, end_date, 'RenkoOBV', tis=tis)
#
#     def generate_signal(self):
        # pdf = self.df
        # self.name = 'renko_obv'
        # ro_df = None
        #
        # for ticker in df.stack(level=1).keys():
        #     ticker_df = copy.deepcopy(df[ticker])
        #
        #     ticker_df["obv_slope"] = ti.slope(ticker_df, col_name='obv')
        #
        #     cur_signal = ['']
        #     new_signal = []
        #     for i in range(len(ticker_df)):
        #         if cur_signal[i] == "":
        #             if ticker_df["renko_bar_num"][i] >= 2 and ticker_df["obv_slope"][i] > 30:
        #                 next_pos = "Buy/Long"
        #             elif ticker_df["renko_bar_num"][i] <= -2 and ticker_df["obv_slope"][i] < -30:
        #                 next_pos = "Sell/Short"
        #             else:
        #                 next_pos = cur_signal[i]
        #
        #         elif cur_signal[i] == "Buy/Long":
        #             if ticker_df["renko_bar_num"][i] <= -2 and ticker_df["obv_slope"][i] < -30:
        #                 next_pos = "Sell/Short"
        #             elif ticker_df["renko_bar_num"][i] < 2:
        #                 next_pos = ""
        #             else:
        #                 next_pos = cur_signal[i]
        #
        #         elif cur_signal[i] == "Sell/Short":
        #             if ticker_df["renko_bar_num"][i] >= 2 and ticker_df["obv_slope"][i] > 30:
        #                 next_pos = "Buy/Long"
        #             elif ticker_df["renko_bar_num"][i] > -2:
        #                 next_pos = ""
        #             else:
        #                 next_pos = cur_signal[i]
        #
        #         new_signal.append(next_pos)
        #         cur_signal.append(next_pos)
        #
        #     ticker_df["cur_signal"] = np.array(cur_signal[:len(ticker_df)])
        #     ticker_df["new_signal"] = np.array(new_signal)
        #
        #     temp_df = ticker_df[~ticker_df.index.duplicated(keep='first')]
        #     temp_df = pd.concat([temp_df], keys=[ticker], axis=1)
        #
        #     if ro_df is not None:
        #         ro_df = ro_df.join(temp_df)
        #     else:
        #         ro_df = temp_df
        #
        # self.df = ro_df
#         pass
#
#
# class RenkoMACD(Strategy):
#     def __init__(self, portfolio, type, start_date, end_date):
#         tis = {'renko': ti.renko}
#         Strategy.__init__(self, portfolio, type, start_date, end_date, 'RenkoMACD', tis=tis)
#
#     def generate_signal(self):
        # df = self.df
        # self.name = 'renko_macd'
        # rm_df = None
        #
        # for ticker in df.stack(level=1).keys():
        #     ticker_df = copy.deepcopy(df[ticker])
        #
        #     ticker_df["macd_slope"] = ti.slope(ticker_df, col_name='macd')
        #     ticker_df["macd_sig_slope"] = ti.slope(ticker_df, col_name='macd_signal')
        #
        #     cur_signal = ['']
        #     new_signal = []
        #     for i in range(len(ticker_df)):
        #         if cur_signal[i] == "":
        #             if ticker_df["renko_bar_num"][i] >= 2 and ticker_df["macd"][i] > ticker_df["macd_signal"][i] \
        #                     and ticker_df["macd_slope"][i] > ticker_df["macd_sig_slope"][i]:
        #                 next_pos = "Buy/Long"
        #             elif ticker_df["renko_bar_num"][i] <= -2 and ticker_df["macd"][i] < ticker_df["macd_signal"][i] \
        #                     and ticker_df["macd_slope"][i] < ticker_df["macd_sig_slope"][i]:
        #                 next_pos = "Sell/Short"
        #             else:
        #                 next_pos = cur_signal[i]
        #
        #         elif cur_signal[i] == "Buy/Long":
        #             if ticker_df["renko_bar_num"][i] <= -2 and ticker_df["macd"][i] < ticker_df["macd_signal"][i] \
        #                     and ticker_df["macd_slope"][i] < ticker_df["macd_sig_slope"][i]:
        #                 next_pos = "Sell/Short"
        #             elif ticker_df["macd"][i] < ticker_df["macd_signal"][i] and ticker_df["macd_slope"][i] < \
        #                     ticker_df["macd_sig_slope"][i]:
        #                 next_pos = ""
        #             else:
        #                 next_pos = cur_signal[i]
        #
        #         elif cur_signal[i] == "Sell/Short":
        #             if ticker_df["renko_bar_num"][i] >= 2 and ticker_df["macd"][i] > ticker_df["macd_signal"][i] and \
        #                     ticker_df["macd_slope"][i] > ticker_df["macd_sig_slope"][i]:
        #                 next_pos = "Buy/Long"
        #             elif ticker_df["macd"][i] > ticker_df["macd_signal"][i] and ticker_df["macd_slope"][i] > \
        #                     ticker_df["macd_sig_slope"][i]:
        #                 next_pos = ""
        #             else:
        #                 next_pos = cur_signal[i]
        #
        #         new_signal.append(next_pos)
        #         cur_signal.append(next_pos)
        #
        #     ticker_df["cur_signal"] = np.array(cur_signal[:len(ticker_df)])
        #     ticker_df["new_signal"] = np.array(new_signal)
        #
        #     temp_df = ticker_df[~ticker_df.index.duplicated(keep='first')]
        #     temp_df = pd.concat([temp_df], keys=[ticker], axis=1)
        #
        #     if rm_df is not None:
        #         rm_df = rm_df.join(temp_df)
        #     else:
        #         rm_df = temp_df
        #
        # self.df = rm_df
#         pass
#
#
# class SMACrossover(Strategy):
#     def __init__(self, portfolio, type, start_date, end_date):
#         tis = {}
#         Strategy.__init__(self, portfolio, type, start_date, end_date, 'SMACrossover', tis=tis)
#
#     def generate_signal(self):
#         pass
