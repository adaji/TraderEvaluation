import numpy as np
import pandas as pd
import datetime


class OS_CS:

    def __init__(self, trading_data: pd.DataFrame, symbol: str) -> None:
        self.symbol = symbol
        # Renaming Time columns
        self.trading_data = pd.concat([trading_data.iloc[:, :2].rename(columns={'Time': 'Time1'}),
                                      trading_data.iloc[:, 2:].rename(columns={'Time': 'Time2'})], axis=1)

        # Removing Balance rows (price and time is 0)
        self.trading_data = self.trading_data.drop(
            index=trading_data[trading_data.Type == "Balance"].index).reset_index(drop=True)

        # Correction of Time2 datatype
        self.trading_data.Time2 = pd.to_datetime(self.trading_data.Time2)

    def find_dates(self, open_strategy: bool) -> pd.DataFrame:
        r = [-0.5, -0.4, -0.3, -0.2, -0.1, 0.1, 0.2, 0.3, 0.4, 0.5]
        duration = self.trading_data.apply(lambda x: x.Time2 - x.Time1, axis=1)
        simulated_time = np.empty((len(duration), 10), dtype=object)
        if open_strategy:
            for i in range(10):
                simulated_time[:, i] = self.trading_data.Time1 + duration * r[i]
        else:
            for i in range(10):
                simulated_time[:, i] = self.trading_data.Time2 + duration * r[i]

        return pd.DataFrame(simulated_time)

    def find_prices(self, simulated_times: pd.DataFrame) -> pd.DataFrame:
        try:
            price_df = pd.read_hdf('./price-data/'+self.symbol+'.h5')
        except:
            print("No data!")
            return None

        # Rounding datetime in simulated_times to the nearest minute, removinf seconds
        simulated_times = simulated_times.applymap(
            lambda x: x.floor('Min') if x.second < 30 else x.ceil('Min'))

        # Get price for simulated data
        return simulated_times.applymap(lambda x: price_df.loc[x].values[0])

    def main(self, open_strategy: bool) -> list:
        # This is the wrapper function. It should be called at __init__ to run all steps

        # Step1: Find simulated dates
        simulated_time = self.find_dates(open_strategy)

        # Step 2: Find prices for simulated dates
        simulated_prices = self.find_prices(simulated_time)

        # Step3: Calculate ranking of every trade between all simulated scenarios

        # Step4: Calculate final score (ranking) for the trader
