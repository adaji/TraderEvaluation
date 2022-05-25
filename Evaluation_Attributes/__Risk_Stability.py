import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from Data_Operation import Market_Data
from datetime import datetime, timedelta

class Risk_Stability:

    def __init__(self, *, trading_data:pd.DataFrame, conf_level=0.95, start_date=None , end_date=None) -> None:
        
        """
        A class used to calculate VaR
        ...
        Attributes
        ----------
        trading_data : pd.DataFrame
            trader's data
        start_date : str
            the start date of calculations
        end_date : str
            the end date of calculations
        Experience : float
            the trader's D-Periods of Experience
        Methods
        -------
        Value_at_Risk()
            Calculate the 1-month VaR for each day from start-date to end-date
        plot_VaR(VaR_list)
            Plot VaR_list Vs time-interval
        """
        
        self.__conf_level = conf_level
        self.__start_date = start_date
        self.__end_date = end_date
        
        # Removing Balance rows (price and time is 0)
        self.__trading_data = trading_data.drop(
            index=trading_data[trading_data.Type == "Balance"].index).reset_index(drop=True)
        
        if self.__start_date == None: self.__start_date = self.__trading_data.Time.iloc[0,0].strftime('%Y-%m-%d')
        if self.__end_date == None: self.__end_date = self.__trading_data.Time.iloc[-1,1].strftime('%Y-%m-%d')
        self.__Time_interval = pd.date_range(start=self.__start_date,end=self.__end_date).to_pydatetime().tolist()
        

    
    def __find_price(self, symbol: str, time: datetime)-> float:
        """
        This function is used to determine a symbol's price at a specific time.
        at first, convert the type of time from TimeStamp to str, because the type of argument of time in the Market_Date function is str.
        Then try to find the price of the symbol at that time and return the price if there is no information about that symbol return 
        None.
        
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
        try:
            df = Market_Data(
            Symbol=symbol,
            Start_Date= (time -timedelta(days = 30)).strftime('%Y-%m-%dT%H:%M:%S'),
            End_Data=time.strftime('%Y-%m-%dT%H:%M:%S'),
            Interval="1d"
            ).send_post_request
            return df.close
        except:
            return np.nan
            
    
        
    @property
    def Value_at_Risk(self):
        """
        This function is used to calculate the 1-month VaR for each day from start-date to end-date.
        Returns
        -------
        list
            the list of 1-month VaR. (the unit of VaR is percentage)
        
        """
        VaR_list = []
        for t in self.__Time_interval:
            prices = pd.DataFrame()

            tickers  = self.__trading_data[(self.__trading_data.Time.iloc[:,0]<=t) & (self.__trading_data.Time.iloc[:,1]>=t)].Symbol.tolist()
            weights  = self.__trading_data[(self.__trading_data.Time.iloc[:,0]<=t) & (self.__trading_data.Time.iloc[:,1]>=t)].Volume.tolist()
            DATA = pd.DataFrame({"W":weights, "tickers":tickers}).groupby(["tickers"])["W"].sum()
            tickers = DATA.index.tolist()
            weights = DATA.values.tolist()
            
            if tickers == []:
                VaR_list.append(np.nan)
                continue
                
            for ticker in tickers:
                
                prices[ticker] = self.__find_price(ticker, t)
            prices = prices.loc[~(prices==0).any(axis=1)]
            returns = prices.pct_change()
            cov_matrix= returns.cov()


            weights=np.array(weights)
            weights = weights/sum(weights)
            port_stdev = np.sqrt(weights.T.dot(cov_matrix).dot(weights))

            cutoff = norm.ppf(self.__conf_level, 0, 1)
            VaR = np.sqrt(prices.shape[0])*port_stdev*cutoff*100
            VaR_list.append(VaR)
        self.__VaR_list = VaR_list
        return self.__VaR_list


    @property
    def plot_VaR(self):
        
        """
        This function is used to plot the 1-month VaR Vs time-interval
        Returns
        -------
        plot
            the plot of the 1-month VaR Vs time-interval
        
        """
        plt.figure(figsize=(12, 6))
        plt.style.use('fivethirtyeight')
        plt.xlabel('Time')
        plt.ylabel('VaR(%)')
        plt.tight_layout()
        plt.plot(self.__Time_interval, self.__VaR_list)
        return plt.show()