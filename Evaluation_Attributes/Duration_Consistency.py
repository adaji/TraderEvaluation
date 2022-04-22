import numpy as np 
import pandas as pd 
import matplotlib.pyplot as plt

class Duration_Consistency:

    def __init__(self,data:pd.DataFrame) -> None:
        self.pross = self.__Duration_Consistency(data)


    @staticmethod
    def __Duration_Consistency(Transaction_data : pd.DataFrame )-> pd.DataFrame:

        important_data = Transaction_data.loc[:,['Time','Price']].applymap(lambda x : np.nan if x == 0 else x).dropna()
        Duration = pd.DataFrame(
            np.zeros((important_data.shape[0],2)),columns=['Position Duration (in minute)','Position Returns (in pip)']
        )
        Duration.loc[:,'Position Duration (in minute)'] = (important_data['Time'].iloc[:,1] - important_data['Time'].iloc[:,0]).apply(
            lambda x : np.around((x / np.timedelta64(1, 'm')),decimals=2)
        ).values 
        Duration.loc[:,'Position Returns (in pip)'] = ((important_data['Price'].iloc[:,1] - important_data['Price'].iloc[:,0]) /
        important_data['Price'].iloc[:,0]).values * 10000
        
        return Duration


    @property
    def plot(self)-> plt.scatter:
        plt.style.use('fivethirtyeight')
        plt.scatter(self.pross.iloc[:,1],self.pross.iloc[:,0],s=150,
        c=self.pross.iloc[:,1].apply(lambda x : -1 if x > 0 else 1).values,
        cmap='RdBu_r',alpha=.5)
        plt.xlabel('Position Returns (in pip)')
        plt.ylabel('Position Duration (in minute)')
        plt.tight_layout()
        
        return plt.show()

    
