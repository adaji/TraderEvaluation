from pandas import DataFrame


class Loss_Aversion:

    def __init__(self,Dataframe:DataFrame) -> None:
        
        self.LossAversion = self.__Balance_add(Dataframe)  

    @staticmethod
    def __Balance_add(dataframe)->DataFrame :
        dataframe['Balance'] = dataframe['Profit'].cumsum()

        return dataframe.loc[:,['Volume','Balance','Price']].applymap(
            lambda x : np.nan if x == 0 else x
        ).dropna().loc[:,'Balance'].pct_change().dropna()