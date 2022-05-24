import requests 
from os import getenv
from dotenv import load_dotenv

class Comput_pipV:
    
    def __init__(self,
        *,Url:str='http://135.181.53.203:8010/dfo_alpha_marketevaluation/comput_pipv',
        Base_Currency:str='USD',
        Pair_Currency:str,
        Target_time:str,
        ApiCode_Name_on_dotenv_file:str = "ApiCode",
        HashCode_Name_on_dotenv_file:str= "HashCode"
    )-> None :

        self.__envExist = load_dotenv()

        if self.__envExist == True :

            self.__parametr = {
                "base_currency" : Base_Currency,
                "pair_currency" : Pair_Currency,
                "targetdatetime": Target_time + 'Z',
                "apicode" : str(getenv(ApiCode_Name_on_dotenv_file)),
                "hashcode" : str(getenv(HashCode_Name_on_dotenv_file))
            }
            self.__url = Url

        else :

            raise ValueError(' You must define a .env file ')

    @property
    def send_post_request(self)-> float:

        try :
            SPR = requests.post(url=self.__url,json=self.__parametr)
        except :
            raise ValueError('Check connection or URL or Apicode and Hash code')
        
        if SPR.json()['value'] != None:
            return float(SPR.json()['value'])
        
        else :

            raise ValueError('Check connection or URL or Apicode and Hash code and instrument ')

#################################################################################################
#///////////////////////////////////////////////////////////////////////////////////////////////#
#################################################################################################
class Cal_volatil:

    def __init__(self,
        *,Url:str='http://135.181.53.203:8010/dfo_alpha_marketevaluation/cal_volatil',
        Base_Currency:str='AUDUSD',
        Pair_Currency:str,
        Start_Date:str,
        End_Data:str,
        ApiCode_Name_on_dotenv_file:str = "ApiCode",
        HashCode_Name_on_dotenv_file:str= "HashCode"
    )-> None :

        self.__envExist = load_dotenv()

        if self.__envExist == True :

            self.__parametr = {
                "base_currency" : Base_Currency,
                "pair_currency" : Pair_Currency,
                "startdate": Start_Date + 'Z',
                "enddate" : End_Data + 'Z',
                "apicode" : str(getenv(ApiCode_Name_on_dotenv_file)),
                "hashcode" : str(getenv(HashCode_Name_on_dotenv_file))
            }
            self.__url = Url

        else :

            raise ValueError(' You must define a .env file ')

    @property
    def send_post_request(self)-> float:

        try :
            SPR = requests.post(url=self.__url,json=self.__parametr)
        except :
            raise ValueError('Check connection or URL or Apicode and Hash code')
        
        if SPR.json()['value'] != None:
            return float(SPR.json()['value'])
        
        else :

            raise ValueError('Check connection or URL or Apicode and Hash code and instrument ')




"""
def Cal_volatil(
    *,Base_Pair_Currency:str ='AUDUSD',
    Pair_Currency:str,
    Open_Posithon_TimeStamp,
    Close_Posithon_TimStamp)-> float:

    return float(
        (
            Market_Data(
                Symbol = Pair_Currency,
                Start_Date = Open_Posithon_TimeStamp.isoformat(),
                End_Data = Close_Posithon_TimStamp.isoformat(),
                Interval = '1min'
            ).send_post_request['close'].pct_change().dropna().std()
        ) / (
            Market_Data(
                Symbol = Base_Pair_Currency,
                Start_Date = Open_Posithon_TimeStamp.isoformat(),
                End_Data = Close_Posithon_TimStamp.isoformat(),
                Interval = '1min'
            ).send_post_request['close'].pct_change().dropna().std()
        )
    )
    
###########################################################################
#/////////////////////////////////////////////////////////////////////////#
###########################################################################

def Comput_pipV(*,
                Base_Currency:str='USD',
                Pair_Currency:str,
                Target_time)->float:
    #---------------------------------------------------------
    if len(Pair_Currency) == 6:     
        #---------------------------------------------------------#
        if Pair_Currency.upper().find(Base_Currency.upper()) == 3:
            return float(
                Market_Data(
                    Symbol=Pair_Currency,
                    Start_Date=Target_time.isoformat(),
                    End_Data=Target_time.isoformat(),
                    Interval='1min'
                ).send_post_request['open'].values
            )
        #---------------------------------------------------------#
        elif Pair_Currency.upper().find(Base_Currency.upper()) == 0:
            return float(
                1 / Market_Data(
                    Symbol=Pair_Currency,
                    Start_Date=Target_time.isoformat(),
                    End_Data=Target_time.isoformat(),
                    Interval='1min'
                ).send_post_request['open'].values
            )
        #---------------------------------------------------------#
        else :
            #---------------------------------------------------------#
            if Pair_Currency.upper()[0:3] in ['EUR','AUD','NZD','GBP','XAU']:
                return float(
                    (
                        1 / Market_Data(
                            Symbol=Pair_Currency,
                            Start_Date=Target_time.isoformat(),
                            End_Data=Target_time.isoformat(),
                            Interval='1min'
                        ).send_post_request['open'].values
                    ) * (
                        Comput_pipV(
                            Base_Currency= Base_Currency.upper(),
                            Pair_Currency= Pair_Currency.upper()[0:3] + Base_Currency.upper(),
                            Target_time=Target_time
                        )
                    )
                )
            #---------------------------------------------------------#
            else :
                return float(
                    (
                        1 / Market_Data(
                            Symbol=Pair_Currency,
                            Start_Date=Target_time.isoformat(),
                            End_Data=Target_time.isoformat(),
                            Interval='1min'
                        ).send_post_request['open'].values
                    ) * (
                        1 / Comput_pipV(
                            Base_Currency= Base_Currency.upper(),
                            Pair_Currency= Base_Currency.upper() + Pair_Currency.upper()[0:3],
                            Target_time=Target_time                
                        )
                    )                    
                )
    #---------------------------------------------------------
    else :
        return float(
            Market_Data(
                Symbol=Pair_Currency,
                Start_Date=Target_time.isoformat(),
                End_Data=Target_time.isoformat(),
                Interval='1min'
            ).send_post_request['open'].values
        )
"""