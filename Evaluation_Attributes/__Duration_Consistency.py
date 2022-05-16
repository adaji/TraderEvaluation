from numpy import zeros , nan , around , timedelta64
from pandas import DataFrame , Series
import matplotlib.pyplot as plt


class Duration:

    def __init__(self,data:DataFrame)-> None:
        self.Duration_data = self.__Duration_Consistency(data)


    @staticmethod
    def __Duration_Consistency(Transaction_data : DataFrame )-> DataFrame:

        important_data = Transaction_data.loc[:,['Time','Symbol','Type','Price']].applymap(lambda x : nan if x == 0 else x).dropna()
        Du_Re = DataFrame(
            zeros((important_data.shape[0],2)),columns=['Position Duration (in minute)','Position Returns (in pip)']
        )
        # calculation Position Duration (in minute)-------------------------------------------------------------------------------
        Du_Re.loc[:,'Position Duration (in minute)'] = (important_data['Time'].iloc[:,1] - important_data['Time'].iloc[:,0]).apply(
            lambda x : around((x / timedelta64(1, 'm')),decimals=2)
        ).values
        # calculation Position Returns (in pip)-------------------------------------------------------------------------------
        Du_Re.loc[:,'Position Returns (in pip)'] = (((important_data['Price'].iloc[:,1] - important_data['Price'].iloc[:,0]) / 
        important_data['Price'].iloc[:,0]).values * important_data['Symbol'].apply(
            lambda x : 100 if (type(x)==str and (
                ( x.lower().find('jpy') != -1 or x.lower().find('xau') != -1)
            )) else 10000
        ).values) * important_data['Type'].apply(
            lambda x : -1 if type(x)==str and x.lower().find('sell') != -1 else 1
        ).values
        
        return Du_Re



    @property
    def plot(self)-> plt.scatter:
        plt.style.use('fivethirtyeight')
        plt.scatter(self.Duration_data.iloc[:,1],self.Duration_data.iloc[:,0],s=150,
        c=self.Duration_data.iloc[:,1].apply(lambda x : -1 if x > 0 else 1).values,
        cmap='RdBu_r',alpha=.5)
        plt.xlabel('Position Returns (in pip)')
        plt.ylabel('Position Duration (in minute)')
        plt.tight_layout()
        
        return plt.show()
