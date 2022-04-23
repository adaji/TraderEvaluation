import numpy as np
import pandas as pd
import datetime

class OS_CS:

    def __init__(self, trading_data:pd.DataFrame)-> None:
        """
        Parameters
        ----------
        trading_data : pd.DataFrame
            DESCRIPTION.

        Returns
        -------
        None
            DESCRIPTION.
        """        
        df1 = trading_data.iloc[:, 0:2].rename({"Time":"Time1"}, axis="columns")
        df2 = trading_data.iloc[:, 2:].rename({"Time":"Time2"}, axis="columns")
        Time = pd.concat([df1.Time1, df2.Time2],axis = 1)
        self.Time = Time
        self.trading_data = trading_data

       
    def find_open_dates(self)-> np.ndarray:
        """
        Returns
        -------
        np.ndarray
            DESCRIPTION.
        """
        duration = self.Time.apply(lambda x: x["Time2"] - x["Time1"] if x["Time2"] !=0 else datetime.timedelta() , axis=1)
        open_time_simulated = np.empty((len(duration),10),dtype=object) 
        r = [-0.5,-0.4,-0.3,-0.2,-0.1, 0.1, 0.2, 0.3, 0.4, 0.5]
        for i in range(10):
            open_time_simulated[:,i] = self.Time.Time1 + duration * r[i]
        return open_time_simulated

    def find_close_dates(self)-> np.ndarray:
        """
        Returns
        -------
        np.ndarray
            DESCRIPTION.
        """
        duration = self.Time.apply(lambda x: x["Time2"] - x["Time1"] if x["Time2"] !=0 else 0 , axis=1)
        close_time_simulated = np.empty((len(duration),10),dtype=object) 
        r = [-0.5,-0.4,-0.3,-0.2,-0.1, 0.1, 0.2, 0.3, 0.4, 0.5]
        for i in range(10):
            close_time_simulated[:,i] = self.Time.Time2 + duration * r[i]
        return close_time_simulated
    