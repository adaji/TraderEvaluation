from Data_Operation import OpenClose_data
import pandas as pd
import matplotlib.pyplot as plt


class OS_CS:

    def __init__(self, trading_data: pd.DataFrame, window_periods=100, plot_unit='S') -> None:
        self.window_periods = window_periods
        self.plot_unit = plot_unit

        trading_data = self.__statement_preprocess(trading_data)
        self.__main(trading_data)

    @staticmethod
    def __statement_preprocess(trading_data):
        # Removing Balance rows (price and time is 0)
        trading_data = trading_data.drop(
            index=trading_data[trading_data.Type == "Balance"].index).reset_index(drop=True)

        # Renaming Time & Price columns
        trading_data = pd.concat([trading_data.iloc[:, :5].rename(columns={'Time': 'Time1', 'Price': 'Price1'}),
                                  trading_data.iloc[:, 5:].rename(columns={'Time': 'Time2', 'Price': 'Price2'})], axis=1)

        # Correction of Time2 datatype
        trading_data.Time2 = pd.to_datetime(trading_data.Time2)

        # Sort by Time2 (close date)
        trading_data = trading_data.sort_values(by='Time2')

        return trading_data

    def __main(self, trading_data: pd.DataFrame) -> None:
        # Fetch prices from server
        prices = trading_data.apply(lambda x: OpenClose_data(
            Symbol=x.Symbol,
            Start_Date=x.Time1.strftime("%Y-%m-%dT%H:%M:%S.000"),
            End_Data=x.Time2.strftime("%Y-%m-%dT%H:%M:%S.000"),
        ).send_post_request, axis=1).to_frame()

        # Calculate scores for all scenarios (Score = 11 - rank of each trade among 11 different scenarios)
        # NOTE1: For strategy base price, price fetched from API for Time1/Time2 is used
        # NOTE2: Open_scores/Close_scores range between 0 to 10
        # buy_mask shows if trade is buy or sell
        buy_mask = trading_data.Type.str.contains('buy', case=False)
        self.open_scores = 11 - prices.apply(lambda x: x[0]
                                             [:11].close.rank(ascending=buy_mask[x.name]), axis=1)
        self.close_scores = 11 - \
            prices.apply(lambda x: x[0][11:].close.rank(ascending=not buy_mask[x.name]), axis=1)

        # Calculate aggregated mean for scores
        self.cumulative_open_scores = self.open_scores.cumsum().div((self.open_scores.index.values + 1), axis=0)
        self.cumulative_close_scores = self.close_scores.cumsum().div((self.close_scores.index.values + 1), axis=0)

        # Calculate aggregated mean for scores with MOVING AVERAGE
        divisor = pd.Series(self.open_scores.index).apply(
            lambda x: x+1 if x < self.window_periods else self.window_periods)
        self.ma_cumulative_open_scores = self.open_scores.rolling(
            min_periods=1, window=self.window_periods).sum().div(divisor, axis=0)
        self.ma_cumulative_close_scores = self.close_scores.rolling(
            min_periods=1, window=self.window_periods).sum().div(divisor, axis=0)

        # Rounding x-axis for plot based on unit
        if self.plot_unit == 'per_trade':
            x = pd.Series(self.open_scores.index, name='Time2')
        else:
            x = trading_data.Time2.dt.round(self.plot_unit)

        # Aggregate scores on base unit
        self.open_scores = self.open_scores.set_index(x).groupby('Time2').mean()
        self.close_scores = self.close_scores.set_index(x).groupby('Time2').mean()

        self.cumulative_open_scores = self.cumulative_open_scores.set_index(
            x).groupby('Time2').mean()
        self.cumulative_close_scores = self.cumulative_close_scores.set_index(
            x).groupby('Time2').mean()

        self.ma_cumulative_open_scores = self.ma_cumulative_open_scores.set_index(
            x).groupby('Time2').mean()
        self.ma_cumulative_close_scores = self.ma_cumulative_close_scores.set_index(
            x).groupby('Time2').mean()

        # Finding final scores
        self.final_open_score = self.cumulative_open_scores.iat[-1, 5]
        self.final_close_score = self.cumulative_close_scores.iat[-1, 5]

    @property
    def plot_open_strategy(self) -> plt.scatter:
        for i in range(11):
            if i == 5:
                plt.plot(self.cumulative_open_scores[i], color='black', linewidth=4)
            else:
                plt.plot(self.cumulative_open_scores[i])

        if self.plot_unit != 'per_trade':
            plt.xticks(rotation=90)
        plt.legend(['-50%', '-40%', '-30%', '-20%', '-10%', 'Strategy', '+10%', '+20%',
                    '+30%', '+40%', '+50%'], loc='center left', bbox_to_anchor=(1, 0.5))
        plt.title('Open Strategy Chart - Accumulative Average')
        plt.xlabel('Position Close Dates')
        plt.ylabel('Score')

        return plt.show()

    @property
    def plot_close_strategy(self) -> plt.scatter:
        for i in range(11, 22):
            if i == 16:
                plt.plot(self.cumulative_close_scores[i], color='black', linewidth=4)
            else:
                plt.plot(self.cumulative_close_scores[i])

        if self.plot_unit != 'per_trade':
            plt.xticks(rotation=90)
        plt.legend(['-50%', '-40%', '-30%', '-20%', '-10%', 'Strategy', '+10%', '+20%',
                    '+30%', '+40%', '+50%'], loc='center left', bbox_to_anchor=(1, 0.5))
        plt.title('Close Strategy Chart - Accumulative Average')
        plt.xlabel('Position Close Dates')
        plt.ylabel('Score')

        return plt.show()

    @property
    def plot_open_strategy_moving_average(self) -> plt.scatter:
        for i in range(11):
            if i == 5:
                plt.plot(self.ma_cumulative_open_scores[i], color='black', linewidth=4)
            else:
                plt.plot(self.ma_cumulative_open_scores[i])

        if self.plot_unit != 'per_trade':
            plt.xticks(rotation=90)
        plt.legend(['-50%', '-40%', '-30%', '-20%', '-10%', 'Strategy', '+10%', '+20%',
                    '+30%', '+40%', '+50%'], loc='center left', bbox_to_anchor=(1, 0.5))
        plt.title('Open Strategy Chart - Moving Average')
        plt.xlabel('Position Close Dates')
        plt.ylabel('Score')

        return plt.show()

    @property
    def plot_close_strategy_moving_average(self) -> plt.scatter:
        for i in range(11, 22):
            if i == 16:
                plt.plot(self.ma_cumulative_close_scores[i], color='black', linewidth=4)
            else:
                plt.plot(self.ma_cumulative_close_scores[i])

        if self.plot_unit != 'per_trade':
            plt.xticks(rotation=90)
        plt.legend(['-50%', '-40%', '-30%', '-20%', '-10%', 'Strategy', '+10%', '+20%',
                    '+30%', '+40%', '+50%'], loc='center left', bbox_to_anchor=(1, 0.5))
        plt.title('Close Strategy Chart - Moving Average')
        plt.xlabel('Position Close Dates')
        plt.ylabel('Score')

        return plt.show()
