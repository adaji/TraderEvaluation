

from Data_Preparation import Preparation
#from Open_Close_Strategy  import OS_CS
import pandas as pd
import matplotlib.pyplot as plt


class Loss_Aversion:
    
  
   
      
      
      
      
    def __init__(self,rename_cols=True) -> None:
        
        self.data_set = Preparation(folder_path = 'E:\DFO\TradeEvaluation\Traders csv data')
        self.df= self.data_set.Get
        self.rename_cols=rename_cols
      
        
        if self.rename_cols == True:
            cols=pd.Series(self.df.columns)
            for dup in self.df.columns[self.df.columns.duplicated(keep=False)]: 
                cols[self.df.columns.get_loc(dup)] = ([dup + '.' + str(d_idx) 
                                         if d_idx != 0 
                                         else dup 
                                         for d_idx in range(self.df.columns.get_loc(dup).sum())]
                                        )
            self.df.columns=cols
        
        self.df["NewProfit"]= (self.df["Price.1"]-self.df["Price"] )* 10**4
        NewProfit=list(self.df["NewProfit"].values)
        Type= list(self.df["Type"].values)
        
        for i in range(0,len(Type)):
            if Type[i]=="Sell":
                NewProfit[i]=NewProfit[i]*(-1)
        
        
        self.df["NewProfit"] =NewProfit
        self.df["Type"]=Type 
        
        
        
        
    @staticmethod
    def clean_df(df,max_size_plot):
        df_pos= df[(df["NewProfit"] >0)]
        df_neg= df[(df["NewProfit"] <0)]
        
        if max_size_plot !=False :
            df_pos=df_pos[(df_pos["NewProfit"] <max_size_plot)]
            
            df_neg=df_neg[(df_neg["NewProfit"] >max_size_plot * (-1))]

        return df_pos , df_neg
    
    def plot(self, max_size_plot =1000 ):
        
        df_pos , df_neg = Loss_Aversion.clean_df(self.df,max_size_plot)
        plt.style.use('fivethirtyeight')
        
        plt.bar(df_pos.index, df_pos["NewProfit"],color='g')
        plt.bar(df_neg.index, df_neg["NewProfit"],color='r')
        plt.xlabel('Position Opened ')
        plt.ylabel('Profit returned')
        plt.tight_layout()
        
        return plt.show()
        
    
'''    
A=Loss_Aversion()    
A.plot(max_size_plot =1000) # You can set  max_size_plot = False if not needed
'''    
    