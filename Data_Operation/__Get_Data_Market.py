from pandas import DataFrame , Timestamp
import requests


class Market_Data:
    
    def __init__(self,
        *,Url:str='http://135.181.53.203:8010/dfo_alpha_marketrawdata',
        Symbol:str,
        Start_Date:str,
        End_Data:str,
        Interval:str
    )-> None :

        self.__url = Url
        self.__parametr = {
            "startdate": Start_Date + 'Z',
            "enddate": End_Data + 'Z',
            "resample": Interval,
            "instrument": Symbol
        }
    
    @property
    def send_post_request(self)-> DataFrame:

        try :
            SPR = requests.post(url=self.__url,json=self.__parametr)
        except :
            raise ValueError('Check connection or URL')
        
        if len(SPR.text) > 0:
            return DataFrame(SPR.json()).applymap(
                lambda x : Timestamp(x) if (type(x) == str and ':' in x) else x
            )
        else:
            raise ValueError('Check  Symbol , Start_Date , End_Data , Interval also url')