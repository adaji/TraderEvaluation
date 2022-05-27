import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import norm
from Data_Operation import Market_Data
from datetime import datetime, timedelta

class Risk_Stability:

    def __init__(self, *, trading_data:pd.DataFrame, start_date=None , end_date=None, window = 45) -> None:
        
        """
        A class used to calculate Risk_Stability

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
        
        self.__window = window
        self.__start_date = start_date
        self.__end_date = end_date
        self.__trading_data = trading_data
       
        self.__trading_data['Profit'] = self.__trading_data['Profit'].astype(str).str.replace(' ', '').astype(float)
        self.__trading_data["Balance"] = self.__trading_data['Profit'].cumsum()
        self.__trading_data = self.__trading_data[["Time","Balance"]]
        for i in range(0,self.__trading_data.shape[0]):
            if self.__trading_data.iloc[i,1] == 0:
                self.__trading_data.iloc[i,1] = self.__trading_data.iloc[i,0]
                
        self.__trading_data = self.__trading_data.iloc[:, [1,2]]
        self.__trading_data ['Time'] = pd.to_datetime(self.__trading_data ['Time'])
        self.__trading_data["day"] = self.__trading_data["Time"].dt.day
        self.__trading_data["month"] = self.__trading_data["Time"].dt.month
        self.__trading_data["year"] = self.__trading_data["Time"].dt.year
        self.__trading_data = self.__trading_data.groupby(by = ["year", "month", "day"]).first()
        self.__trading_data["Log Return"] = np.log(self.__trading_data.Balance) - np.log(self.__trading_data.Balance.shift(1))
        if self.__start_date == None: self.__start_date = self.__trading_data.Time.iloc[0]
        if self.__end_date == None: self.__end_date = self.__trading_data.Time.iloc[-1]
            
        self.__trading_data = self.__trading_data[self.__trading_data.Time >= self.__start_date]
        self.__trading_data = (self.__trading_data[self.__trading_data.Time <= self.__end_date]).reset_index(drop=True)
        self.__Time_interval = pd.date_range(start=self.__start_date,end=self.__end_date).to_pydatetime().tolist()
        

    def __Value_at_Risk(self):
        """
        This function is used to calculate the 1-month VaR for each day from start-date to end-date.

        Returns
        -------
        list
            the list of 1-month VaR. (the unit of VaR is percentage)
        
        """
                
        VaR = []
        upper_bond = []
        lower_bond = []
        for i in range(self.__window, self.__trading_data.shape[0]):
            VaR.append(np.mean(self.__trading_data["Log Return"][i-self.__window: i] ) - 1.96 * np.std(self.__trading_data["Log Return"][i-self.__window: i] ))
        for i in range(self.__window, len(VaR)):
            upper_bond.append(max(VaR[i-self.__window:i]))
            lower_bond.append(min(VaR[i-self.__window:i]))
    
        return VaR, upper_bond, lower_bond
    @property
    def plot_VaR(self):
        
        """
        This function is used to plot the 1-month VaR Vs time-interval

        Returns
        -------
        plot
            the plot of the 1-month VaR Vs time-interval
        
        """
        VaR, upper_bond, lower_bond = self.__Value_at_Risk()
        plt.figure(figsize=(12, 6))
        
        plt.xlabel('Time')
        plt.ylabel('VaR(%)')
        plt.tight_layout()
        plt.plot(self.__trading_data.Time[2*self.__window:], VaR[self.__window:], label="VaR")
        plt.plot(self.__trading_data.Time[2*self.__window:], upper_bond, label="Max VaR")
        plt.plot(self.__trading_data.Time[2*self.__window:], lower_bond, label="Min VaR")
        plt.legend()
        return plt.show() 
        
        

