from Data_Operation import Cal_volatil , Comput_pipV
from .__Duration_Consistency import Duration
import pandas as pd 
import numpy as np 


class Risk_Adjusment:

    #________________________________________________________________Start.__init__
    def __init__(
        self,
        *,
        Base_Currency:str = 'USD',
        Base_pair_Currency:str = 'AUDUSD',
        dataframe:pd.DataFrame
    )-> None:
        
        self.D_Leverage_Duration = self.__DLD_M(
            Base_Currency=Base_Currency,
            Base_pair_Currency=Base_pair_Currency,
            dataframe= dataframe
        )
    #__________________________________________________________________end.__init__

    #________________________________________________________________Start.__DLD_M
    def __DLD_M(
        self,
        *,
        Base_Currency:str = 'USD',
        Base_pair_Currency:str = 'AUDUSD',
        dataframe:pd.DataFrame
    )-> pd.DataFrame:

        DLD = self.__DLeverage(
            Base_Currency=Base_Currency,
            Base_pair_Currency=Base_pair_Currency,
            dataframe_add_B= self.__add_B(
                dataframe=dataframe
            )
        )

        DLD.loc[:,'Position Duration'] = Duration(
            dataframe
        ).Duration_data.loc[:,'Position Duration (in minute)']
        DLD.loc[:,'Exposure'] = DLD.loc[:,'D-Leverage'] * np.sqrt(DLD.loc[:,'Position Duration'])

        return DLD
    #__________________________________________________________________end.__DLD_M

    #__________________________________________________________________Start.__add_b
    @staticmethod
    def __add_B(dataframe:pd.DataFrame)-> pd.DataFrame:

        dataframe['Balance'] = dataframe['Profit'].cumsum().shift()
        added_b = dataframe.loc[:,['Time','Symbol','Volume','Balance','Price']].applymap(
            lambda x : np.nan if x == 0 else x
        ).dropna()
        added_b.loc[:,'Volume'] = added_b.loc[:,'Volume'] * 100000

        return added_b
    #____________________________________________________________________end.__add_b

    #__________________________________________________________________Start.__DLeverage
    @staticmethod
    def __DLeverage(
        *,
        Base_Currency:str = 'USD',
        Base_pair_Currency:str = 'AUDUSD',
        dataframe_add_B:pd.DataFrame
    )-> pd.DataFrame:
         
        DLD_frame = pd.DataFrame(
            np.zeros([dataframe_add_B.shape[0],2]),
            columns=['D-Leverage','Position Duration']
        )

        for roW in np.arange(0,dataframe_add_B.shape[0]):

            DLD_frame.loc[:,'D-Leverage'].iloc[roW] = (
                (
                    (
                        (
                            (dataframe_add_B.iloc[roW,:]['Volume'] * dataframe_add_B.iloc[roW,:]['Price'][0]) * (
                                Comput_pipV(
                                    Base_Currency=Base_Currency,
                                    Pair_Currency=dataframe_add_B.iloc[roW,:]['Symbol'],
                                    Target_time=dataframe_add_B.iloc[roW,:]['Time'][0].isoformat()
                                ).send_post_request
                            )
                        ) / dataframe_add_B.iloc[roW,:]['Balance']
                    ) * (
                        Cal_volatil(
                            Base_Currency=Base_pair_Currency,
                            Pair_Currency=dataframe_add_B.iloc[roW,:]['Symbol'],
                            Start_Date=dataframe_add_B.iloc[roW,:]['Time'][0].isoformat(),
                            End_Data=dataframe_add_B.iloc[roW,:]['Time'][1].isoformat()
                        ).send_post_request
                    )
                )
            )
        
        return DLD_frame
    #__________________________________________________________________end.__DLeverage
