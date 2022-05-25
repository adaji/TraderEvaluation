from Data_Operation import OpenClose_data
import pandas as pd
import matplotlib.pyplot as plt


class OS_CS:

    def __init__(self, trading_data: pd.DataFrame) -> None:
        trading_data = self.__statement_preprocess(trading_data)

        # Cumulative scores and final scores are accessible from object instance
        self.open_scores, self.close_scores = self.__main(trading_data)
        # self.final_open_score = self.open_scores.iat[-1, 5]
        # self.final_close_score = self.close_scores.iat[-1, 5]

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

    @staticmethod
    def __main(trading_data: pd.DataFrame) -> list:
        # Fetch prices from server
        prices = trading_data.apply(lambda x: OpenClose_data(
            Symbol=x.Symbol,
            Start_Date=x.Time1.strftime("%Y-%m-%dT%H:%M:%S.000"),
            End_Data=x.Time2.strftime("%Y-%m-%dT%H:%M:%S.000"),
        ).send_post_request, axis=1).to_frame()

        # # Selecting only rows with complete data, droping short-term trades & trades with no price data fetched from API
        # # SHOULD BE CORRECTED - NO SELECTION
        # prices = prices[prices[0].apply(lambda x: len(x)) == 22]
        # trading_data = trading_data.loc[prices.index]

        # Calculate scores for all scenarios (Score = 11 - rank of each trade among 11 different scenarios)
        # NOTE1: For strategy base price, price fetched from API for Time1/Time2 is used
        # NOTE2: Open_scores/Close_scores range between 0 to 10
        open_scores = 11 - prices.apply(lambda x: x[0][:11].close.rank(), axis=1)
        close_scores = 11 - prices.apply(lambda x: x[0][11:].close.rank(ascending=False), axis=1)

        # Change index to Time2
        open_scores.set_index(trading_data.Time2, inplace=True)
        close_scores.set_index(trading_data.Time2, inplace=True)

        # Calculate aggregated mean for scores
        # cumulative_open_scores = open_scores.cumsum().div((open_scores.index.values + 1), axis=0)
        # cumulative_close_scores = close_scores.cumsum().div((close_scores.index.values + 1), axis=0)

        # Returning cumulative score for open & close strategies
        return (open_scores, close_scores)

    @property
    def plot_open_strategy(self) -> plt.scatter:
        # Calculate average score for trades that close at the same second
        y = self.open_scores.groupby('Time2').mean()
        plt.plot(list(set(range(len(y)))), y)
        plt.plot(list(set(range(len(y)))), y[5], color='black', linewidth=4)
        plt.legend(['-50%', '-40%', '-30%', '-20%', '-10%', 'Strategy', '+10%', '+20%',
                    '+30%', '+40%', '+50%'], loc='center left', bbox_to_anchor=(1, 0.5))
        plt.xticks(list(set(range(len(y)))), labels=y.index, rotation='vertical')
        plt.title('Open Strategy Chart')
        plt.xlabel('Position Close Dates')
        plt.ylabel('Score')

        return plt.show()

    @property
    def plot_close_strategy(self) -> plt.scatter:
        # Calculate average score for trades that close at the same second
        y = self.close_scores.groupby('Time2').mean()
        plt.plot(list(set(range(len(y)))), y)
        plt.plot(list(set(range(len(y)))), y[16], color='black', linewidth=4)
        plt.legend(['-50%', '-40%', '-30%', '-20%', '-10%', 'Strategy', '+10%', '+20%',
                    '+30%', '+40%', '+50%'], loc='center left', bbox_to_anchor=(1, 0.5))
        plt.xticks(list(set(range(len(y)))), labels=y.index, rotation='vertical')
        plt.title('Close Strategy Chart')
        plt.xlabel('Position Close Dates')
        plt.ylabel('Score')

        return plt.show()