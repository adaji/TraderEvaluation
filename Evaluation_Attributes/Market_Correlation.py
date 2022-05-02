import numpy as np
import pandas as pd
import datetime

class Market_Correlation:

    def __init__(self, trading_data: pd.DataFrame, start_date, end_date) -> None:
        
        self.start_date = start_date
        self.end_date = end_date
        # Renaming Time columns
        self.trading_data = pd.concat([trading_data.iloc[:, :2].rename(columns={'Time': 'Time1'}),
                                      trading_data.iloc[:, 2:].rename(columns={'Time': 'Time2'})], axis=1)

        # Removing Balance rows (price and time is 0)
        self.trading_data = self.trading_data.drop(
            index=trading_data[trading_data.Type == "Balance"].index).reset_index(drop=True)
        
        self.trading_data = self.trading_data[self.trading_data.Time1 >= self.start_date]
        self.trading_data = self.trading_data[self.trading_data.Time2 <= self.end_date]
        
        
        self.Time1 = self.trading_data.sort_values(by="Time1").Time1
        self.Time2 = self.trading_data.Time2
        
    def find_price(self, Symbol: str, time):
        # we dont have the folder of data now
        """
        try:
            price_df = pd.read_hdf('./price-data/'+ Symbol +'.h5')
        except:
            print("No data!")
            return None
        
        # Rounding time to the nearest minute, removinf seconds
        f = lambda x: x.floor('Min') if x.second < 30 else x.ceil('Min')
        time = f(time)

        # Get price for that time
        g = lambda x: price_df.loc[x].values[0]
        price = g(time)
        """
        return 1
    
    def find_returns(self, Symbol: str):
        # we dont have the folder of data now
        """
        try:
            price_df = pd.read_hdf('./price-data/'+ Symbol +'.h5')
        except:
            print("No data!")
            return None
        
        # Rounding datetime to the nearest minute, removinf seconds
        times = self.Time2.applymap(
            lambda x: x.floor('Min') if x.second < 30 else x.ceil('Min'))

        # Get price for that intrval
        prices = times.applymap(lambda x: price_df.loc[x].values[0])
        return_ =  ((prices / prices.shift()) -1 )*100
        """
        return np.random.random(len(self.Time2))/10

        
    def portfolio_return(self):
        protfolio_return = []
        for t2 in range(self.trading_data.shape[0]):
            t1 = 0
            return_ = []
            w = []
            while self.Time1.iloc[t1] < self.Time2.iloc[t2]:

                if self.Time1.index[t1] == t2:
                    return_.append((self.trading_data.Price.iloc[t2,1]/self.trading_data.Price.iloc[t2,0] -
                                    (self.trading_data.Commission[t2] + self.trading_data.Swap[t2])/
                                    self.trading_data.Price.iloc[t2,0] -1)*100)
                    w.append(self.trading_data.Volume[self.Time1.index[t1]])
                else:
                    Symbol = self.trading_data.Symbol[t1]
                    return_.append(((self.find_price(Symbol, time = self.Time2[t2])/self.trading_data.Price.iloc[t1,0] -
                                     (self.trading_data.Commission[t1] + self.trading_data.Swap[t1])/
                                    self.trading_data.Price.iloc[t1,0])-1)*100)
                    w.append(self.trading_data.Volume[self.Time1.index[t1]])
                t1 += 1
                if t1 == len(self.Time1):
                    break

            protfolio_return.append(np.dot(return_,w)/sum(w))
            self.Time1 = self.Time1.drop(index =self.Time1[self.Time1.index ==t2].index)
        # Get protfolio_return includeing swap and commission
        return protfolio_return
    
    def correlation(self, protfolio_return):
        weight_ = self.trading_data.groupby(['Symbol'])["Volume"].sum()
        weight = weight_ / sum(weight_)
        Symbols = self.trading_data.Symbol.unique() 
        corr =  pd.DataFrame(columns=["correlation", "Weight"])
        for symbol in Symbols:
            asset_return = self.find_returns(symbol)
            corr_ = np.corrcoef(asset_return,protfolio_return)[0][1]
            corr.loc[symbol,"correlation"] = abs(corr_)
            corr.loc[symbol,"Weight"] = weight[symbol]
        # Get correlation of protfolio_return with assets that traded in the fixed intervals
        return corr
    
    def score(self, corr):
        total_corr = np.dot(corr["correlation"] , corr["Weight"])
        score = ((1-total_corr)/10)*100
        # Get score of market correlation
        return score
        
        
           
              
            
            
            
            
            