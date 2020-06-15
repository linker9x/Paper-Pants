from paper_pants.trading_strategies.strategy.general_strategy import Strategy
import paper_pants.trading_strategies.technical_indicators.ohlcv_ti as ti
import copy


class ResistanceBreakout(Strategy):
    def __init__(self, portfolio, type, start_date, end_date):
        tis = {'atr': ti.atr}
        Strategy.__init__(self, portfolio, type, start_date, end_date, tis=tis)

    def generate_signals(self):
        for ticker in self.df_data.stack(level=1).keys():
            ticker_df = copy.deepcopy(self.df_data[ticker])
            ticker_df['roll_max_high'] = ticker_df['High'].rolling(20).max()
            ticker_df['roll_min_low'] = ticker_df['Low'].rolling(20).min()
            ticker_df['roll_max_vol'] = ticker_df['Volume'].rolling(20).max()
            print(ticker_df)

            cur_pos = self.portfolio.positions[ticker]['Position']
            cur_size = self.portfolio.positions[ticker]['Size']

            print(cur_pos)
            print(cur_size)

            sec_bottom_row = ticker_df.iloc[-2]
            bottom_row = ticker_df.iloc[-1]

            if cur_pos == '':
                if bottom_row['High'] >= bottom_row['roll_max_high'] and bottom_row['Volume'] > 1.5 * \
                        sec_bottom_row['roll_max_vol']:
                    next_pos = 'Buy/Long'
                    print('CUR: {}, ACTION: {}'.format(cur_pos, self.long_something()))
                elif bottom_row['Low'] <= bottom_row['roll_min_low'] and bottom_row['Volume'] > 1.5 * \
                        sec_bottom_row['roll_max_vol']:
                    next_pos = 'Sell/Short'
                    print('CUR: {}, ACTION: {}'.format(cur_pos, self.short_something()))
                else:
                    next_pos = cur_pos
                    print('CUR: {}, ACTION: {}'.format(cur_pos, None))

            elif cur_pos == 'Buy/Long':
                if bottom_row['Close'] < sec_bottom_row['Close'] - sec_bottom_row['atr']:
                    next_pos = ''
                    print('CUR: {}, ACTION: {}'.format(cur_pos, self.exit_something()))
                elif bottom_row['Low'] <= bottom_row['roll_min_low'] and bottom_row['Volume'] > 1.5 * \
                        sec_bottom_row['roll_max_vol']:
                    next_pos = 'Sell/Short'
                    print('CUR: {}, ACTION: {}'.format(cur_pos, self.short_something()))
                else:
                    next_pos = cur_pos
                    print('CUR: {}, ACTION: {}'.format(cur_pos, self.long_something()))

            elif cur_pos == 'Sell/Short':
                if bottom_row['Close'] > sec_bottom_row['Close'] + sec_bottom_row['atr']:
                    next_pos = ''
                    print('CUR: {}, ACTION: {}'.format(cur_pos, self.exit_something()))
                elif bottom_row['High'] >= bottom_row['roll_max_high'] and bottom_row['Volume'] > 1.5 * \
                        sec_bottom_row['roll_max_vol']:
                    next_pos = 'Buy/Long'
                    print('CUR: {}, ACTION: {}'.format(cur_pos, self.long_something()))
                else:
                    next_pos = cur_pos
                    print('CUR: {}, ACTION: {}'.format(cur_pos, self.short_something()))

            next_size = cur_size  # figure this out and actually buy something?
            self.portfolio.positions[ticker]['Position'] = next_pos
            self.portfolio.positions[ticker]['Size'] = next_size


class RenkoOBV(Strategy):
    def __init__(self, portfolio, type, start_date, end_date):
        tis = {'renko': ti.renko, 'obv': ti.obv}
        Strategy.__init__(self, portfolio, type, start_date, end_date, tis=tis)

    def generate_signals(self):
        for ticker in self.df_data.stack(level=1).keys():
            ticker_df = copy.deepcopy(self.df_data[ticker])
            ticker_df['obv_slope'] = ti.slope(ticker_df, col_name='obv')
            print(ticker_df)

            cur_pos = self.portfolio.positions[ticker]['Position']
            cur_size = self.portfolio.positions[ticker]['Size']

            print(cur_pos)
            print(cur_size)

            bottom_row = ticker_df.iloc[-1]

            if cur_pos == '':
                if bottom_row['renko_bar_num'] >= 2 and bottom_row['obv_slope'] > 30:
                    next_pos = 'Buy/Long'
                    print('CUR: {}, ACTION: {}'.format(cur_pos, self.long_something()))
                elif bottom_row['renko_bar_num'] <= -2 and bottom_row['obv_slope'] < -30:
                    next_pos = 'Sell/Short'
                    print('CUR: {}, ACTION: {}'.format(cur_pos, self.short_something()))
                else:
                    next_pos = cur_pos
                    print('CUR: {}, ACTION: {}'.format(cur_pos, None))

            elif cur_pos == 'Buy/Long':
                if bottom_row['renko_bar_num'] <= -2 and bottom_row['obv_slope'] < -30:
                    next_pos = 'Sell/Short'
                    print('CUR: {}, ACTION: {}'.format(cur_pos, self.short_something()))
                elif bottom_row['renko_bar_num'] < 2:
                    next_pos = ''
                    print('CUR: {}, ACTION: {}'.format(cur_pos, self.exit_something()))
                else:
                    next_pos = cur_pos
                    print('CUR: {}, ACTION: {}'.format(cur_pos, self.long_something()))

            elif cur_pos == 'Sell/Short':
                if bottom_row['renko_bar_num'] >= 2 and bottom_row['obv_slope'] > 30:
                    next_pos = 'Buy/Long'
                    print('CUR: {}, ACTION: {}'.format(cur_pos, self.long_something()))
                elif bottom_row['renko_bar_num'] > -2:
                    next_pos = ''
                    print('CUR: {}, ACTION: {}'.format(cur_pos, self.exit_something()))
                else:
                    next_pos = cur_pos
                    print('CUR: {}, ACTION: {}'.format(cur_pos, self.short_something()))

            next_size = cur_size  # figure this out and actually buy something?
            self.portfolio.positions[ticker]['Position'] = next_pos
            self.portfolio.positions[ticker]['Size'] = next_size


class RenkoMACD(Strategy):
    def __init__(self, portfolio, type, start_date, end_date):
        tis = {'renko': ti.renko, 'macd': ti.macd}
        Strategy.__init__(self, portfolio, type, start_date, end_date, tis=tis)

    def generate_signals(self):
        for ticker in self.df_data.stack(level=1).keys():
            ticker_df = copy.deepcopy(self.df_data[ticker])
            ticker_df['macd_slope'] = ti.slope(ticker_df, col_name='macd')
            ticker_df['macd_sig_slope'] = ti.slope(ticker_df, col_name='macd_signal')
            print(ticker_df)

            cur_pos = self.portfolio.positions[ticker]['Position']
            cur_size = self.portfolio.positions[ticker]['Size']

            print(cur_pos)
            print(cur_size)

            bottom_row = ticker_df.iloc[-1]

            if cur_pos == '':
                if bottom_row['renko_bar_num'] >= 2 and bottom_row['macd'] > bottom_row['macd_signal'] \
                        and bottom_row['macd_slope'] > bottom_row['macd_sig_slope']:
                    next_pos = 'Buy/Long'
                elif bottom_row['renko_bar_num'] <= -2 and bottom_row['macd'] < bottom_row['macd_signal'] \
                        and bottom_row['macd_slope'] < bottom_row['macd_sig_slope']:
                    next_pos = 'Sell/Short'
                else:
                    next_pos = cur_pos

            elif cur_pos == 'Buy/Long':
                if bottom_row['renko_bar_num'] <= -2 and bottom_row['macd'] < bottom_row['macd_signal'] \
                        and bottom_row['macd_slope'] < bottom_row['macd_sig_slope']:
                    next_pos = 'Sell/Short'
                elif bottom_row['macd'] < bottom_row['macd_signal'] and bottom_row['macd_slope'] < \
                        bottom_row['macd_sig_slope']:
                    next_pos = ''
                else:
                    next_pos = cur_pos

            elif cur_pos == 'Sell/Short':
                if bottom_row['renko_bar_num'] >= 2 and bottom_row['macd'] > bottom_row['macd_signal'] and \
                        bottom_row['macd_slope'] > bottom_row['macd_sig_slope']:
                    next_pos = 'Buy/Long'
                elif bottom_row['macd'] > bottom_row['macd_signal'] and bottom_row['macd_slope'] > \
                        bottom_row['macd_sig_slope']:
                    next_pos = ''
                else:
                    next_pos = cur_pos

            next_size = cur_size  # figure this out and actually buy something?
            self.portfolio.positions[ticker]['Position'] = next_pos
            self.portfolio.positions[ticker]['Size'] = next_size


# class SMACrossover(Strategy):
#     def __init__(self, portfolio, type, start_date, end_date):
#         tis = {}
#         Strategy.__init__(self, portfolio, type, start_date, end_date, 'SMACrossover', tis=tis)
#
#     def generate_signal(self):
#         pass
