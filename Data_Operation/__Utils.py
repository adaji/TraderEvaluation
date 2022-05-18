from .__Get_Data_Market import Market_Data

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