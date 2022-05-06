import pandas as pd
import numpy as np
import datetime
from backtest.data_con.data_con import DataCon



class volatility:

    """
    Calculate the Volatility of Historic Stock Prices
    """

    def __init__(self, full_url: str, start_year: int,
                 start_month: int, start_day: int, for_days: int, benchmark_symbol: str = 'EURUSD') -> None:
        
        self.full_url = full_url
        self.start_year = start_year
        self.start_month = start_month
        self.start_day = start_day
        self.for_days = for_days
        self.benchmark_symbol = benchmark_symbol
        self.volatility_data = pd.DataFrame()


    def __fetch_symbol_price_from_API(self, symbol: str) -> pd.DataFrame:

        start_date = datetime.date(self.start_year, self.start_month, self.start_day)
        dc = DataCon(self.full_url)
        data = pd.DataFrame()
        for i in range(self.for_days):
            try:
                data = pd.concat([data, dc.get_m1_data(symbol, start_date + datetime.timedelta(days = i))])
            except:
                pass
        return data

    #Calculate symbol volatility
    def __calculate_symbol_volatility(self, symbol: str , use_history_data : bool ) -> float:

        if use_history_data:
            symbol_index_in_history = self.volatility_data [self.volatility_data.eq(symbol).any(1)].index.values
            if symbol_index_in_history.size > 0:
                return self.volatility_data.at[symbol_index_in_history[0],'Volatility']
            else:

                df = self.__fetch_symbol_price_from_API(symbol = symbol)
                if df.empty:
                    return np.NAN
                df['log returns'] = np.log(df['close'] / df['close'].shift(1))
                volatility = df['log returns'].std()
                return volatility
            
    #Calculate the ratio of each volatility to the value of the benchmark volatility
    def __relative_to_benchmark(self, volatility_df : pd.DataFrame )-> pd.DataFrame:
        
        #sereach benchmark symbol in current volatility data
        benchmark_index = volatility_df [volatility_df.eq(self.benchmark_symbol).any(1)].index.values
        if benchmark_index.size > 0:
            benchmark_value = volatility_df.at[benchmark_index[0],'Volatility']
            volatility_df['Relative Volatility'] = volatility_df['Volatility'] / benchmark_value
            
        #sereach benchmark symbol in historical volatility data
        else:
            benchmark_index = self.volatility_data [self.volatility_data.eq(self.benchmark_symbol).any(1)].index.values
            if benchmark_index.size > 0:
                benchmark_value = self.volatility_data.at[benchmark_index[0],'Volatility']
                volatility_df['Relative Volatility'] = volatility_df['Volatility'] / benchmark_value
                
            #get benchmark symbol data and calclate volatility 
            else :
                benchmark_value = self.__calculate_symbol_volatility(self.benchmark_symbol,False)
                if not(np.isnan(benchmark_valu)) and  benchmark_valu> 0:
                    volatility_df['Relative Volatility'] = volatility_df['Volatility'] / benchmark_value
                else:
                    volatility_df['Relative Volatility']=np.nan
        return volatility_df

    #calculate volatility of trader positions datafram
    def volatility_calculator(self , symbols_data: pd.DataFrame , use_history_data = True ) -> pd.DataFrame:

        symbols = symbols_data['Symbol'].apply(lambda x: np.nan
            if x == 0 else x).dropna().unique()
        symbols_df = pd.DataFrame(symbols, columns = ['Symbol'])
        symbols_df['Volatility'] = symbols_df.apply(lambda row: self.__calculate_symbol_volatility(str(row['Symbol']),use_history_data), axis = 1)
        symbols_df = self.__relative_to_benchmark(symbols_df)
        self.volatility_data = pd.concat([self.volatility_data, symbols_df ])
        return symbols_df
