from numpy import nan
from pandas import DataFrame , Timestamp
import requests
from os import getenv
from dotenv import load_dotenv

class Market_Data:
    
    def __init__(self,
        *,Url:str='http://135.181.53.203:8010/dfo_alpha_marketrawdatasimple',
        Symbol:str,
        Start_Date:str,
        End_Data:str,
        Interval:str,
        ApiCode_Name_on_dotenv_file:str = "ApiCode",
        HashCode_Name_on_dotenv_file:str= "HashCode"
    )-> None :

        self.__envExist = load_dotenv()

        if self.__envExist == True :

            self.__parametr = {
                "startdate": Start_Date + 'Z',
                "enddate": End_Data + 'Z',
                "instrument": Symbol,
                "apicode" : str(getenv(ApiCode_Name_on_dotenv_file)),
                "hashcode" : str(getenv(HashCode_Name_on_dotenv_file))
            }
            self.__url = Url

        else :

            raise ValueError(' You must define a .env file ')


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
            return nan

#################################################################################################
#///////////////////////////////////////////////////////////////////////////////////////////////#
#################################################################################################
class OpenClose_data:

    def __init__(self,
        *,Url:str='http://135.181.53.203:8010/dfo_alpha_open_close_strategy',
        Symbol:str,
        Start_Date:str,
        End_Data:str,
        ApiCode_Name_on_dotenv_file:str = "ApiCode",
        HashCode_Name_on_dotenv_file:str= "HashCode"
    )-> None :

        self.__envExist = load_dotenv()

        if self.__envExist == True :

            self.__parametr = {
                "startdate": Start_Date + 'Z',
                "enddate": End_Data + 'Z',
                "instrument": Symbol,
                "apicode" : str(getenv(ApiCode_Name_on_dotenv_file)),
                "hashcode" : str(getenv(HashCode_Name_on_dotenv_file))
            }
            self.__url = Url

        else :

            raise ValueError(' You must define a .env file ')
        
    @property
    def send_post_request(self)-> DataFrame:

        try :
            SPR = requests.post(url=self.__url,json=self.__parametr)
        except :
            raise ValueError('Check connection or URL or Apicode and Hash code')
        
        if SPR.json()['data'] != None:
            return DataFrame( SPR.json()['data'] ).applymap(
                lambda x : Timestamp(x) if (type(x) == str and ':' in x) else x
            )
        else:
            raise ValueError('Check connection or URL or Apicode and Hash code and instrument ')
            