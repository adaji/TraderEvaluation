import numpy as np
import pandas as pd
import datetime

class Market_Correlation:

    def __init__(self, trading_data: pd.DataFrame, start_date=None, end_date= None, frequency = None) -> None:

        # Renaming Time columns
        self.trading_data = pd.concat([trading_data.iloc[:, :2].rename(columns={'Time': 'Time1'}),
                                      trading_data.iloc[:, 2:].rename(columns={'Time': 'Time2'})], axis=1)

        # Removing Balance rows (price and time is 0)
        self.trading_data = self.trading_data.drop(
            index=trading_data[trading_data.Type == "Balance"].index).reset_index(drop=True)
        
        self.trading_data = self.trading_data[self.trading_data.Time1 >= start_date]
        self.trading_data = self.trading_data[self.trading_data.Time2 <= end_date]
        
        
        self.Time1 = self.trading_data.sort_values(by="Time1").Time1
        self.Time2 = self.trading_data.Time2
        
    def find_prices(self, Symbol: str, time):
        return 1
    
    def portfolio_return(self):
        protfolio_return = []
        for t2 in range(self.trading_data.shape[0]):
            t1 = 0
            return_ = []
            w = []
            while self.Time1.iloc[t1] < self.Time2.iloc[t2]:

                if self.Time1.index[t1] == t2:
                    return_.append((self.trading_data.Price.iloc[t2,1]/self.trading_data.Price.iloc[t2,0]-1)*100)
                    w.append(self.trading_data.Volume[self.Time1.index[t1]])
                else:
                    Symbol = self.trading_data.Symbol[t1]
                    return_.append((self.find_prices(Symbol, time = self.Time2[t2])/self.trading_data.Price.iloc[t1,0]-1)*100)
                    w.append(self.trading_data.Volume[self.Time1.index[t1]])
                t1 += 1
                if t1 == len(self.Time1):
                    break

            protfolio_return.append(np.dot(return_,w)/sum(w))
            self.Time1 = self.Time1.drop(index =self.Time1[self.Time1.index ==t2].index)
            
        return protfolio_return
            