from Data_Operation import OpenClose_data
import pandas as pd
import matplotlib.pyplot as plt


class OS_CS:

    def __init__(self, trading_data: pd.DataFrame) -> None:
        trading_data = self.__statement_preprocess(trading_data)
        self.open_scores, self.close_scores = self.__main(trading_data)

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

        # Calculate scores for all scenarios (Score = 11 - rank of each trade among 11 different scenarios)
        # NOTE1: For strategy base price, price fetched from API for Time1/Time2 is used
        # NOTE2: Open_scores/Close_scores range between 0 to 10
        # buy_mask shows if trade is buy or sell
        buy_mask = trading_data.Type.str.contains('buy', case=False)
        open_scores = 11 - prices.apply(lambda x: x[0]
                                        [:11].close.rank(ascending=buy_mask[x.name]), axis=1)
        close_scores = 11 - \
            prices.apply(lambda x: x[0][11:].close.rank(ascending=not buy_mask[x.name]), axis=1)

        # Calculate aggregated mean for scores
        # cumulative_open_scores = open_scores.cumsum().div((open_scores.index.values + 1), axis=0)
        # cumulative_close_scores = close_scores.cumsum().div((close_scores.index.values + 1), axis=0)

        return (open_scores, close_scores)

    @property
    def plot_open_strategy(self) -> plt.scatter:
        plt.plot(self.open_scores)
        plt.plot(self.open_scores[5], color='black', linewidth=4)
        plt.legend(['-50%', '-40%', '-30%', '-20%', '-10%', 'Strategy', '+10%', '+20%',
                    '+30%', '+40%', '+50%'], loc='center left', bbox_to_anchor=(1, 0.5))
        plt.title('Open Strategy Chart')
        plt.xlabel('Position Close Dates')
        plt.ylabel('Score')

        return plt.show()

    @property
    def plot_close_strategy(self) -> plt.scatter:
        plt.plot(self.close_scores)
        plt.plot(self.close_scores[16], color='black', linewidth=4)
        plt.legend(['-50%', '-40%', '-30%', '-20%', '-10%', 'Strategy', '+10%', '+20%',
                    '+30%', '+40%', '+50%'], loc='center left', bbox_to_anchor=(1, 0.5))
        plt.title('Close Strategy Chart')
        plt.xlabel('Position Close Dates')
        plt.ylabel('Score')

        return plt.show()
