import paper_pants.trading_strategies.strategies.technical_indicators.ohlcv_ti as ti
import copy
import numpy as np

_tis = [ti.macd, ti.atr, ti.bollinger_band, ti.rsi, ti.adx, ti.obv, ti.slope, ti.renko]
_strategies = ['rebalancing', 'resist_breakout', 'renko_obv', 'renko_macd']

class Strategy(object):
    def __init__(self, dataframe):
        self.df = copy.deepcopy(dataframe)
        self._calculate_all()


    def __str__(self):
        return ('df: {}'.format(self.df))

    def _calculate_all(self):
        df = self.df
        for t_ind in _tis:
            print(str(t_ind))
            df = df.join(t_ind(df))
        self.df = df
        #df.to_csv('./look.csv')

    def rebalancing(self):
        return None

    def resist_breakout(self):
        df = self.df
        df["roll_max_high"] = df["High"].rolling(20).max()
        df["roll_min_low"] = df["Low"].rolling(20).min()
        df["roll_max_vol"] = df["Volume"].rolling(20).max()

        cur_signal = ['']
        new_signal = []
        for i in range(len(df)):
            if cur_signal[i] == "":
                if df["High"][i] >= df["roll_max_high"][i] and df["Volume"][i] > 1.5 * df["roll_max_vol"][i-1]:
                    next_pos = "Buy/Long"
                elif df["Low"][i] <= df["roll_min_low"][i] and df["Volume"][i] > 1.5 * df["roll_max_vol"][i-1]:
                    next_pos = "Sell/Short"
                else:
                    next_pos = cur_signal[i]

            elif cur_signal[i] == "Buy/Long":
                if df["Adj Close"][i] < df["Adj Close"][i-1] - df["atr"][i-1]:
                    next_pos = ""
                elif df["Low"][i] <= df["roll_min_low"][i] and df["Volume"][i] > 1.5 * df["roll_max_vol"][i-1]:
                    next_pos = "Sell/Short"
                else:
                    next_pos = cur_signal[i]

            elif cur_signal[i] == "Sell/Short":
                if df["Adj Close"][i] > df["Adj Close"][i-1] + df["atr"][i-1]:
                    next_pos = ""
                elif df["High"][i] >= df["roll_max_high"][i] and df["Volume"][i] > 1.5 * df["roll_max_vol"][i-1]:
                    next_pos = "Buy/Long"
                else:
                    next_pos = cur_signal[i]

            new_signal.append(next_pos)
            cur_signal.append(next_pos)

        df["cur_signal"] = np.array(cur_signal[:len(df)])
        df["new_signal"] = np.array(new_signal)

        self.df = df
        df.to_csv('./look.csv')


    def renko_obv(self):
        df = self.df

        df["obv_slope"] = ti.slope(df, col_name='obv')

        cur_signal = ['']
        new_signal = []
        for i in range(len(df)):
            if cur_signal[i] == "":
                if df["renko_bar_num"][i] >= 2 and df["obv_slope"][i] > 30:
                    next_pos = "Buy/Long"
                elif df["renko_bar_num"][i] <= -2 and df["obv_slope"][i] < -30:
                    next_pos = "Sell/Short"
                else:
                    next_pos = cur_signal[i]

            elif cur_signal[i] == "Buy/Long":
                if df["renko_bar_num"][i] <= -2 and df["obv_slope"][i] < -30:
                    next_pos = "Sell/Short"
                elif df["renko_bar_num"][i] < 2:
                    next_pos = ""
                else:
                    next_pos = cur_signal[i]

            elif cur_signal[i] == "Sell/Short":
                if df["renko_bar_num"][i] >= 2 and df["obv_slope"][i] > 30:
                    next_pos = "Buy/Long"
                elif df["renko_bar_num"][i] > -2:
                    next_pos = ""
                else:
                    next_pos = cur_signal[i]

            new_signal.append(next_pos)
            cur_signal.append(next_pos)

        df["cur_signal"] = np.array(cur_signal[:len(df)])
        df["new_signal"] = np.array(new_signal)

        self.df = df
        df.to_csv('./look.csv')

    def renko_macd(self):
        df = self.df

        df["macd_slope"] = ti.slope(df, col_name='macd')
        df["macd_sig_slope"] = ti.slope(df, col_name='macd_signal')

        cur_signal = ['']
        new_signal = []
        for i in range(len(df)):
            if cur_signal[i] == "":
                if df["renko_bar_num"][i] >= 2 and df["macd"][i] > df["macd_signal"][i] \
                        and df["macd_slope"][i] > df["macd_sig_slope"][i]:
                    next_pos = "Buy/Long"
                elif df["renko_bar_num"][i] <= -2 and df["macd"][i] < df["macd_signal"][i] \
                        and df["macd_slope"][i] < df["macd_sig_slope"][i]:
                    next_pos = "Sell/Short"
                else:
                    next_pos = cur_signal[i]

            elif cur_signal[i] == "Buy/Long":
                if df["renko_bar_num"][i] <= -2 and df["macd"][i] < df["macd_signal"][i] \
                        and df["macd_slope"][i] < df["macd_sig_slope"][i]:
                    next_pos = "Sell/Short"
                elif df["macd"][i] < df["macd_signal"][i] and df["macd_slope"][i] < df["macd_sig_slope"][i]:
                    next_pos = ""
                else:
                    next_pos = cur_signal[i]

            elif cur_signal[i] == "Sell/Short":
                if df["renko_bar_num"][i] >= 2 and df["macd"][i] > df["macd_signal"][i] and \
                        df["macd_slope"][i] > df["macd_sig_slope"][i]:
                    next_pos = "Buy/Long"
                elif df["macd"][i] > df["macd_signal"][i] and df["macd_slope"][i] > df["macd_sig_slope"][i]:
                    next_pos = ""
                else:
                    next_pos = cur_signal[i]

            new_signal.append(next_pos)
            cur_signal.append(next_pos)

        df["cur_signal"] = np.array(cur_signal[:len(df)])
        df["new_signal"] = np.array(new_signal)

        self.df = df
        df.to_csv('./look.csv')
