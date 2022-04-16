

class Duration_Consistency:

    def __init__(self) -> None:
        pass


    def Duration_Consistency(Transaction_data : pd.DataFrame )-> pd.DataFrame:

    important_data = Transaction_data.loc[:,['Time','Price']].applymap(lambda x : np.nan if x == 0 else x).dropna()
    Duration = pd.DataFrame(
        np.zeros((important_data.shape[0],2)),columns=['Position Duration','Position Returns']
    )
    Duration.loc[:,'Position Duration'] = (important_data['Time'].iloc[:,1] - important_data['Time'].iloc[:,0]).apply(
        lambda x : x / np.timedelta64(1, 'm')
    )
    return Duration


    