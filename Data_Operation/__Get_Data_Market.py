from turtle import st
from pandas import DataFrame , Timestamp
import requests
from os import getenv

class Market_Data:
    
    def __init__(self,
        *,Url:str='http://135.181.53.203:8010/dfo_alpha_marketrawdata',
        Symbol:str,
        Start_Date:str,
        End_Data:str,
        Interval:str,
        ApiCode_Name_on_dotenv_file:str = "ApiCode",
        HashCode_Name_on_dotenv_file:str= "HashCode"
    )-> None :

        self.__url = Url

        self.__parametr = {
            "startdate": Start_Date + 'Z',
            "enddate": End_Data + 'Z',
            "resample": Interval,
            "instrument": Symbol,
            "apicode" : str(getenv(ApiCode_Name_on_dotenv_file)),
            "hashcode" : str(getenv(HashCode_Name_on_dotenv_file))
        }
    
    @property
    def send_post_request(self)-> DataFrame:

        try :
            SPR = requests.post(url=self.__url,json=self.__parametr)
        except :
            raise ValueError('Check connection or URL or Apicode and Hash code')
        
        if SPR.json()['rawdatas'] != None:
            return DataFrame( SPR.json()['rawdatas'] ).applymap(
                lambda x : Timestamp(x) if (type(x) == str and ':' in x) else x
            )
        else:
            raise ValueError('Check  Symbol , Start_Date , End_Data , Interval also url')