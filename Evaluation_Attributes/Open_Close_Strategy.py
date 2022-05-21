from Data_Operation import OpenClose_data
import pandas as pd
import matplotlib.pyplot as plt


class OS_CS:

    def __init__(self, trading_data: pd.DataFrame) -> None:
        self.trading_data = trading_data
        self._statement_preprocess()
        self._open_score, self._close_score = self._main()

    def _statement_preprocess(self):
        # Removing Balance rows (price and time is 0)
        self.trading_data = self.trading_data.drop(
            index=self.trading_data[self.trading_data.Type == "Balance"].index).reset_index(drop=True)

        # Renaming Time & Price columns
        self.trading_data = pd.concat([self.trading_data.iloc[:, :5].rename(columns={'Time': 'Time1', 'Price': 'Price1'}),
                                      self.trading_data.iloc[:, 5:].rename(columns={'Time': 'Time2', 'Price': 'Price2'})], axis=1)

        # Correction of Time2 datatype
        self.trading_data.Time2 = pd.to_datetime(self.trading_data.Time2)

        # Sort by Time2 (close date)
        self.trading_data = self.trading_data.sort_values(by='Time2')

    def _main(self):
        # Fetch prices from server
        prices = self.trading_data.apply(lambda x: OpenClose_data(  # cutting dataframe for faster testing: trading_data.loc[:10]
            Symbol=x.Symbol,
            Start_Date=x.Time1.strftime("%Y-%m-%dT%H:%M:00.000"),
            End_Data=x.Time2.strftime("%Y-%m-%dT%H:%M:00.000"),
        ).send_post_request, axis=1).to_frame()

        # Selecting only rows with complete data, droping short-term trades & trades with no price data fetched from API
        # SHOULD BE CORRECTED - NO SELECTION
        prices = prices[prices[0].apply(lambda x: len(x)) == 22]
        self.trading_data = self.trading_data.loc[prices.index]

        # Calculate return for different simulated scenarios with 2 options:
        # SHOULD BE CORRECTED - OPTION 1 SHOULD BE USED
        # Option 1: Base price used from trading_data (statement)
        # Downside: Statement prices (open/close) difference with same time data fetched from API is too much!
        # open_scenarios= prices.apply(lambda x: df.loc[x.name].Price2 / x[0].loc[0:10].close - 1, axis=1)
        # close_scenarios = prices.apply(lambda x: x[0].loc[11:].close / df.loc[x.name].Price1 - 1, axis=1)

        # # Assigning column 5 & 16 (real returns) from trading_data prices
        # open_scenarios[5] = close_scenarios[16] = df.loc[:1, :].apply(lambda x: x.Price2 / x.Price1 - 1, axis=1)

        # Option 2: Base price used from data fetched from API (close price of nearest 1Min candle to original time that trade executed)
        open_scenarios = prices.apply(lambda x: x[0].loc[16].close / x[0].loc[0:10].close - 1, axis=1)
        close_scenarios = prices.apply(lambda x: x[0].loc[11:].close / x[0].loc[5].close - 1, axis=1)

        # Calculate scores for all scenarios (Score = 11 - rank of each trade among 11 different scenarios)
        open_scores = 11 - (open_scenarios*-1).rank(axis=1)
        close_scores = 11 - (close_scenarios*-1).rank(axis=1)

        # Calculate aggregated mean for scores
        self._cumulative_open_score = open_scores.cumsum().div((open_scores.index.values + 1), axis=0)
        self._cumulative_close_score = close_scores.cumsum().div((close_scores.index.values + 1), axis=0)

        # Plot scores
        x = self.trading_data.Time2[:self._cumulative_open_score.index[-1]+1]
        # Plotting: open strategy
        plt.figure()
        plt.plot(self._cumulative_open_score)
        plt.plot(self._cumulative_open_score[5], color='black', linewidth=4)
        plt.legend(['-50%', '-40%', '-30%', '-20%', '-10%', 'Strategy', '+10%', '+20%',
                    '+30%', '+40%', '+50%'], loc='center left', bbox_to_anchor=(1, 0.5))
        plt.xticks(list(set(range(len(x)))), labels=x, rotation='vertical')
        plt.show()

        # Plotting: close strategy
        plt.figure()
        plt.plot(self._cumulative_close_score)
        plt.plot(self._cumulative_close_score[16], color='black', linewidth=4)
        plt.legend(['-50%', '-40%', '-30%', '-20%', '-10%', 'Strategy', '+10%', '+20%',
                    '+30%', '+40%', '+50%'], loc='center left', bbox_to_anchor=(1, 0.5))
        plt.xticks(list(set(range(len(x)))), labels=x, rotation='vertical')
        plt.show()

        # Returning final average score for open & close strategies
        return (self._cumulative_open_score.iat[-1, 5], self._cumulative_close_score.iat[-1, 5])
