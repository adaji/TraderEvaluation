from Data_Preparation import Preparation
from Open_Close_Strategy  import OS_CS
import pandas as pd
import matplotlib.pyplot as plt


class Capacity:

     
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
        
        self.df["NewProfit"]= (self.df["Price.1"]-self.df["Price"] )
        NewProfit=list(self.df["NewProfit"].values)
        Type= list(self.df["Type"].values)
        
        for i in range(0,len(Type)):
            if Type[i]=="Sell":
                NewProfit[i]=NewProfit[i]*(-1)
        
        
        self.df["NewProfit"] =NewProfit
        self.df["Type"]=Type 
        self.df["NewProfit_0.2"]= self.df["NewProfit"] * 0.2
        self.df["NewProfit_0.5"] = self.df["NewProfit"] * 0.5
        self.df["NewProfit_1.5"] = self.df["NewProfit"] * 1.5
        self.df["NewProfit_2.0"] = self.df["NewProfit"] * 2.0
        
        
    def plot(self):
        self.df=self.df.sort_values(by="Time")
       
     #   plt.style.use('fivethirtyeight')
                          
        plt.plot(self.df["Time"] , self.df["NewProfit"])
        plt.plot(self.df["Time"] , self.df["NewProfit_0.2"])
        plt.plot(self.df["Time"] , self.df["NewProfit_0.5"])
        plt.plot(self.df["Time"] , self.df["NewProfit_1.5"])
        plt.plot(self.df["Time"] , self.df["NewProfit_2.0"])
        
        lst=["1",'0.2','0.5','1.5',"2"]
        plt.xlabel('Position Opened ')
        plt.ylabel('Profit returned')
        plt.legend(labels=lst)
        plt.tight_layout()
        return plt.show()
    