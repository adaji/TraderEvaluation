import pandas as pd
import numpy as np
import requests
import datetime

class Experience:
  #calcuulate experience 

  def __init__(self, num_trading:int = 18 ,num_days_from_first_trade:int= 15 ):
    self.num_trading = num_trading
    self.num_days_from_first_trade = num_days_from_first_trade

  def _find_volatility_of_symbol(self,symbol : str ,volatility_data : pd.DataFrame)-> float:
    return float((volatility_data.iloc[(np.where(volatility_data == symbol)[0])]['normal volatility']).values)

  def calc_representative_decisions(self, Transaction_data : pd.DataFrame ,volatility_data : pd.DataFrame  )-> pd.DataFrame:
    
    result = pd.DataFrame()

    important_data = Transaction_data.loc[:, ['Time', 'Symbol', 'Leverage'
            ]].applymap(lambda x: (np.nan if x == 0 else x))
    important_data = important_data.dropna()
    important_data['sqrt Position Duration (in minute)'] = \
        (important_data['Time'].iloc[:, 1] - important_data['Time'].iloc[:,
        0]).apply(lambda x: np.sqrt(np.around(x / np.timedelta64(1, 'm'),
                  decimals=2))).values
    important_data['pos_Time'] = important_data['Time'].iloc[:, 0]
    important_data = important_data.drop('Time', axis=1)

    important_data = important_data.sort_values(by=['pos_Time'])
    important_data = important_data.reset_index(drop=True)

    important_data['delevrage'] = important_data['Symbol'].apply(lambda x: \
            self._find_volatility_of_symbol(x, volatility_data)).values \
        * important_data['Leverage']
    important_data['Exponential'] = important_data['delevrage'] \
        * important_data['sqrt Position Duration (in minute)']

    first_day = pd.to_datetime(important_data['pos_Time'], errors='coerce',
                              infer_datetime_format=True).min()
    _index = 0

    while True:

        sec = first_day + datetime.timedelta(days=self.num_days_from_first_trade)
        exp_data = important_data.loc[(important_data['pos_Time']
                                      >= first_day)
                                      & (important_data['pos_Time'] < sec),
                                      :]
        if exp_data.shape[0] < self.num_trading:
            exp_data = important_data[_index:_index + self.num_trading]
        _index = _index + exp_data.shape[0]

        max_exponential = exp_data['Exponential'].max()
        exp_data['Representative Decisions'] = exp_data.loc[:, 'Exponential'
                ] / max_exponential
        sum = exp_data['Representative Decisions'].sum()

        result = result.append({
            'Time': first_day,
            'score': self.score(sum),
            'num_trade': exp_data.shape[0],
            'sum': sum,
            }, ignore_index=True)
        if _index >= important_data.shape[0]:
            break
        first_day = important_data.iloc[_index]['pos_Time']

    return result

  def score(self, num : float) -> int:
    range_1=1.2
    range_2=2.4
    range_3=3.2
    range_4=4.8
    range_5=6
    range_6=7.2
    range_7=8.4
    range_8=9.6
    range_9=10.8
    range_10=12

    if range_10 <= num: return 10
    if range_9 <= num: return 9
    if range_8 <= num: return 8
    if range_7 <= num: return 7
    if range_6 <= num: return 6
    if range_5 <= num: return 5
    if range_4 <= num: return 4
    if range_3 <= num: return 3
    if range_2 <= num: return 2
    if range_1 <= num: return 1
    return 0

  def calculate_experince(self, Transaction_data : pd.DataFrame ,volatility_data : pd.DataFrame  )->  pd.DataFrame:
    return self.calc_representative_decisions(Transaction_data ,volatility_data)

import datetime
from backtest.data_con.data_con import DataCon
 

class Volatility:
 
  @staticmethod
  def _get_symbol_price_API(symbol : str,start_year : int ,start_month : int ,start_day : int  ,for_days : int ) -> pd.DataFrame:
    start_date = datetime.date(start_year, start_month, start_day)
    dc = DataCon('http://185.235.43.95:6263')
    print(start_date)
    data=pd.DataFrame()
    for i in range(for_days):
      try:
        data = pd.concat([data, dc.get_m1_data(symbol, start_date + datetime.timedelta(days=i))])
      except:
        pass
    print(data)
    return data

  
  @staticmethod
  def _calculate_symbol_voliality(symbol : str,start_year : int ,start_month : int 
                                  ,start_day : int  ,for_days : int )-> float:


    df = Volatility._get_symbol_price_API(symbol=symbol ,start_year=start_year 
                                    ,start_month=start_month,start_day=start_day,for_days = for_days)
    if df.empty:
      return np.NAN

    df['log returns'] = np.log(df['close']/df['close'].shift(1))
    volatility = df['log returns'].std()
    print(volatility)
    return volatility

  def _normal_volatility(volatility_data,start_year : int ,start_month : int 
                           ,start_day : int  ,for_days : int ,index_volatility : str='EURUSD')-> pd.DataFrame:
    index_value=(volatility_data[volatility_data.eq(index_volatility).any(1)]['volatility']).values
    if index_value>0:
      volatility_data['normal volatility'] = volatility_data['volatility']/index_value
    else:
      index_value = Volatility._calculate_symbol_voliality(index_volatility,start_year ,start_month  ,start_day  ,for_days )
      volatility_data['normal volatility'] = volatility_data['volatility']/index_value
    return volatility_data
  
  def voliality_calculator(symbols_data : pd.DataFrame  , start_year : int ,start_month : int 
                           ,start_day : int  ,for_days : int ,index_volatility: str ='EURUSD' )-> pd.DataFrame:

    symbols = symbols_data['Symbol'].apply(lambda x : np.nan if x == 0 else x).dropna().unique()


    symbols_df=pd.DataFrame(symbols,columns=['Symbol'])
    print(symbols_df)


    symbols_df['volatility']=symbols_df.apply(lambda row: Volatility._calculate_symbol_voliality(str(row['Symbol']),start_year=start_year 
                                    ,start_month=start_month,start_day=start_day,for_days = for_days), axis=1)
    symbols_df = Volatility._normal_volatility(symbols_df,start_year,start_month,start_day,for_days,index_volatility)                                    
    return symbols_df
