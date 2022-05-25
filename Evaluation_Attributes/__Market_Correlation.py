from Data_Operation import Market_Data
from datetime import datetime
import numpy as np
import pandas as pd
import datetime


#TODO  : Market_corr 

class Market_Correlation:

    def __init__(self,*,trading_data: pd.DataFrame, Experience: int, start_date=None, end_date=None) -> None:
        
        """
        A class used to represent a Market_Correlation attribute

        ...

        Attributes
        ----------
        trading_data : pd.DataFrame
            trader's data
        start_date : pd.Timestamp
            the start date of calculations
        end_date : pd.Timestamp
            the end date of calculations
        Experience : int
            the trader's D-Periods of Experience

        Methods
        -------
        portfolio_return()
            calculate the return of protfolio per close position
        correlation(protfolio_return_)
            calculate the correlation of protfolio_return with each assets that trader open a position on it at the fixed interval.
        score(corr)
            calculate the score of trader's Market _correlaton.
        """


        self.__start_date = start_date
        self.__end_date = end_date
        self.__Experience = Experience
        
        # Renaming Time columns
        self.__trading_data = pd.concat([trading_data.iloc[:, :2].rename(columns={'Time': 'Time1'}),
                                      trading_data.iloc[:, 2:].rename(columns={'Time': 'Time2'})], axis=1)

        # Removing Balance rows (price and time is 0)
        self.__trading_data = self.__trading_data.drop(
            index=self.__trading_data[trading_data.Type == "Balance"].index).reset_index(drop=True)
        

        # filter data from start_date to end_date
        if self.__start_date == None: self.__start_date = self.__trading_data.Time1.iloc[0,0]
        if self.__end_date == None: self.__end_date = self.__trading_data.Time2.iloc[-1,1]
        self.__trading_data = self.__trading_data[self.__trading_data.Time1 >= self.__start_date]
        self.__trading_data = (self.__trading_data[self.__trading_data.Time2 <= self.__end_date]).reset_index(drop=True)
        
        # renaming enter and exit Time
        self.__Time1 = self.__trading_data.sort_values(by="Time1").Time1
        self.__Time2 = self.__trading_data.Time2
        
        if self.__Experience < 12:
            raise ValueError("Trader's Experience should be more than 12 D-Periods to calculate market correlation!")
    
    
    def __find_price(self, Symbol: str, time: pd.Timestamp)-> float:
        
        """
        This function is used to determine a symbol's price at a specific time.
        at first, convert the type of time from TimeStamp to str, because the type of argument of time in the Market_Date function is str.
        Then try to find the price of the symbol at that time and return the price if there is no information about that symbol return None.
        
        Parameters
        ----------
        Symbol :str
            The symbol to find its price
        time : pd.Timestamp
            The time of symbol's price
        
        Returns
        -------
        float
            the price of symbol at the specefic time
        
        """
       
        time = time.strftime('%Y-%m-%dT%H:%M:%S')
        
        asset = Market_Data(
        Symbol= Symbol,
        Start_Date= time,
        End_Data=time,
        Interval="1Min"
        ).send_post_request
        
        try:
            return asset.close[0]
        except:
            asset["close"] = [np.nan]
            return asset.close[0]
        

    def __find_returns(self, Symbol: str)-> pd.DataFrame:
        
        """
        This function is used to calculate the symbol's returns in the interval of close_time of the positions(self.Time2).
        at first, define a list to save the symbol's prices in the specefic interval. then determine the symbol's price in each day of 
        the interval like previous function by using a for-loop. finally calculate the symbol's returns and return them as pd.DataFrame.
            
        Parameters
        ----------
        Symbol :str
            The symbol to find its returns in self.Time2
            
        Returns
        -------
        pd.DataFrame
            the symbol's returns at the specefic intervlal
        
        """
        price_list = []
        for t in self.__Time2:
            t = t.strftime('%Y-%m-%dT%H:%M:%S')
            asset = Market_Data(
            Symbol= Symbol,
            Start_Date= t,
            End_Data=t,
            Interval="1Min"
            ).send_post_request
            
            try:
                price_list.append(asset.close[0])
            except:
                asset["close"] = [np.nan]
                price_list.append(asset.close[0])
   
        prices = pd.DataFrame(price_list)
        return_ =  ((prices / prices.shift()) -1 )*100
        
        return return_.iloc[:,0]

    @property
    def portfolio_return(self)-> list:
        
        """
        This function is used to calculate the return of protfolio per close position.
        at first, define an empty list for protfolio_return. for each time in close_time position calculate return and weight of assets 
        that opened before it's time. If it was a selling position, consider the negative sign for calculated return. finaly calculate 
        the weighted average for return in each close_time position and return the portfolio return as a list.
            
        Returns
        -------
        list
            the return of protfolio per close position
        
        """
        protfolio_return_ = [] # portfolio return is updated per close position
        for t2 in range(self.__trading_data.shape[0]):
            t1 = 0
            return_ = []  # list of assets' return from t1 to t2 
            w = [] # weight 
            while self.__Time1.iloc[t1] < self.__Time2.iloc[t2]:

                if self.__Time1.index[t1] == t2:
                    asset_return = (self.__trading_data.Price.iloc[t2,1]/self.__trading_data.Price.iloc[t2,0] -  # asset return from t1 to t2
                                    (self.__trading_data.Commission[t2] + self.__trading_data.Swap[t2])/
                                    self.__trading_data.Price.iloc[t2,0] -1)*100
                    
                    if self.__trading_data.Type[self.__Time1.index[t1]] == "Sell":
                        asset_return = -1 * asset_return
                    
                    return_.append(asset_return)
                    w.append(self.__trading_data.Volume[self.__Time1.index[t1]])
                else:
                    Symbol = self.__trading_data.Symbol[self.__Time1.index[t1]]
                    asset_return = ((self.__find_price(Symbol, time = self.__Time2[t2])/self.__trading_data.Price.iloc[self.__Time1.index[t1],0] -  
                                     (self.__trading_data.Commission[self.__Time1.index[t1]] + self.__trading_data.Swap[self.__Time1.index[t1]])/
                                    self.__trading_data.Price.iloc[self.__Time1.index[t1],0])-1)*100
                    if self.__trading_data.Type[self.__Time1.index[t1]] == "Sell":
                        asset_return = -1 * asset_return
                        
                    return_.append(asset_return)
                    w.append(self.__trading_data.Volume[self.__Time1.index[t1]])
                t1 += 1
                if t1 == len(self.__Time1):
                    break

            protfolio_return_.append(np.dot(return_,w)/sum(w))
            self.__Time1 = self.__Time1.drop(index =self.__Time1[self.__Time1.index ==t2].index)
        self.__protfolio_return_ = protfolio_return_
        return self.__protfolio_return_
    @property
    def correlation(self)-> pd.DataFrame:
        
        """
        This function is used to calculate the correlation of protfolio_return with each assets that trader open a position on it at 
        the fixed interval. At first, determine the weights and symbols of assets that trader open a position on them at the fixed interval
        finally calculate the correlation of each symbol's returns with protfolio_return and return the correlation and weights of each 
        symbol as a pd.DataFrame.(the weights are calculated by the Volume.) 
            
        Returns
        -------
        pd.DataFrame
            Dataframe of correlation between portfolio return and symbol's returns, weight of each symbols
        
        """
        weight_ = self.__trading_data.groupby(['Symbol'])["Volume"].sum()
        weight = weight_ / sum(weight_)
        Symbols = self.__trading_data.Symbol.unique() 
        corr =  pd.DataFrame(columns=["correlation", "Weight"])
        for symbol in Symbols:
            asset_return = self.__find_returns(symbol)
            corr_ = np.corrcoef(asset_return[1:],self.__protfolio_return_[1:])[0][1]
            corr.loc[symbol,"correlation"] = abs(corr_)
            corr.loc[symbol,"Weight"] = weight[symbol]
        self.__corr = corr
        return self.__corr
    @property
    def score(self)-> float:
        
        """
        This function is used to calculate the score of trader's Market _correlaton.

        Returns
        -------
        float
            the score of trader's Market _correlaton.
        
        """
        total_corr = np.dot(self.__corr["correlation"] , self.__corr["Weight"])
        return ((1-total_corr)/10)*100
        
        
           
              
            
            
            
            
            