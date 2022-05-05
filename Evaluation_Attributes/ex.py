import numpy as np 
import pandas as pd 

class Experience:

    def __init__(self,Data:pd.DataFrame) -> None:
        self.__Leverage_Duration = self.__C_Leverage_Duration(Data)






    @staticmethod
    def __C_Leverage_Duration(data:pd.DataFrame)-> pd.DataFrame:
        """
        calculation Leverage and Duration 
        """
        data['Position Returns (in pip)'] = ((data['Price'].iloc[:,1] - data['Price'].iloc[:,0]) 
        /data['Price'].iloc[:,0]).values * 10000
        #----------------- for sell postion -----------------
        targhet_type_list = ['Sell Stop','Sell','Sell Limit']
        for i in np.arange(0,data.shape[0]):
            if data.loc[i,'Type'] in targhet_type_list:
                data.loc[i,'Position Returns (in pip)'] = data.loc[i,'Position Returns (in pip)'] * -1
        #----------------------------------------------------
        data['lever_profit'] = data.loc[:,'Profit'] - ((data.loc[:,['Commission','Swap']]).sum(1))
        #----------------------------------------------------
        data['Balance'] = data['Profit'].cumsum()
        #data['Balance'].shift(periods=1)
        #----------------------------------------------------
        data['Symbol'] = data['Symbol'].apply(lambda x : str(x))
        #----------------------------------------------------
        for i in np.arange(1,data.shape[0]):
            if data.loc[i,'Symbol'].find('JPY') > 0:
                data.loc[i,'Leverage'] = ((data.loc[i,'lever_profit']/data.loc[i,'Position Returns (in pip)'])*(data.loc[i,'Price'][0]*100)) / data.loc[i-1,'Balance']
            elif data.loc[i,'Symbol'].find('XAU') > 0:
                data.loc[i,'Leverage'] = ((data.loc[i,'lever_profit']/data.loc[i,'Position Returns (in pip)'])*(data.loc[i,'Price'][0]*100)) / data.loc[i-1,'Balance']
            else :
                data.loc[i,'Leverage'] = ((data.loc[i,'lever_profit']/data.loc[i,'Position Returns (in pip)'])*(data.loc[i,'Price'][0]*10000)) / data.loc[i-1,'Balance']
            
        #----------------------------------- can add more symbol---------------
        D_lever = data.loc[:,['Time','Symbol','Leverage']].applymap(lambda x : np.nan if x == 0 else x).dropna()
        D_lever.loc[:,'Position Duration (in minute)'] = (D_lever['Time'].iloc[:,1] - D_lever['Time'].iloc[:,0]).apply(
            lambda x : np.around((x / np.timedelta64(1, 'm')),decimals=2)
        ).values
        
        return D_lever.loc[:,['Symbol','Leverage','Position Duration (in minute)']]