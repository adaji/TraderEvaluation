

class Duration_Consistency:

    def __init__(self) -> None:
        pass



def Duration_Consistency(Transaction_data : pd.DataFrame )-> pd.DataFrame:

    important_data = Transaction_data.loc[:,['Time','Price']].applymap(lambda x : np.nan if x == 0 else x).dropna()
    Duration = pd.DataFrame(
        np.zeros((important_data.shape[0],2)),columns=['Position Duration (in minute)','Position Returns (in pip)']
    )
    Duration.loc[:,'Position Duration (in minute)'] = (important_data['Time'].iloc[:,1] - important_data['Time'].iloc[:,0]).apply(
        lambda x : np.around((x / np.timedelta64(1, 'm')),decimals=2)
    ).values 
    Duration.loc[:,'Position Returns (in pip)'] = (important_data['Price'].iloc[:,1] - important_data['Price'].iloc[:,0]).values * 10000
    
    return Duration

    