from .__Duration_Consistency import Duration 
from pandas import DataFrame
from numpy import zeros


class Capacity :

    def __init__(self,*, dataframe ,Max_Slippage:int = 2)-> None:
        
        self.Returns_Capacity = self.__calCapa(
            Duration(dataframe).Duration_data['Position Returns (in pip)'],
            Max_Slippage = Max_Slippage
        )

    @staticmethod
    def __calCapa(Time_seris,Max_Slippage)-> DataFrame:
        calCapa = DataFrame(
            zeros([Time_seris.shape[0],5]),
            columns= ['Max_Slippage','1/2 Max_Slippage','1/4 Max_Slippage','1/5 Max_Slippage','Position Returns (in pip)']
        )
        calCapa.loc[:,'Position Returns (in pip)'] = Time_seris.values
        calCapa.loc[:,'Max_Slippage'] = ( Time_seris.values - Max_Slippage)
        calCapa.loc[:,'1/2 Max_Slippage'] = ( Time_seris.values - ( Max_Slippage * .5 ))
        calCapa.loc[:,'1/4 Max_Slippage'] = ( Time_seris.values - ( Max_Slippage * .25))
        calCapa.loc[:,'1/5 Max_Slippage'] = ( Time_seris.values - ( Max_Slippage * .2))
    
        return calCapa