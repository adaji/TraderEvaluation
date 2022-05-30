import pandas as pd
from os import listdir, makedirs


class Transformation:
    def __init__(self, folder_path: str) -> None:
        self.__folder_path = folder_path
        self.__csvfile_list = self.__read_folder(self.__folder_path)

    @staticmethod
    def __read_folder(path_folder: str) -> list:
        csvfile_names = []
        for asset in listdir(path_folder):
            if asset.find('csv') != -1:
                csvfile_names.append(asset)
        if len(csvfile_names) == 0:
            raise TypeError('This class defined for find and read csv file in floder path')
        return csvfile_names

    @staticmethod
    def __make_std_csv(folder_path: str, file: str, export_path: str) -> None:
        # Read csv
        df = pd.read_csv(folder_path+'/'+file)
        df.datetime = pd.to_datetime(df.datetime).dt.round('1s')

        df = df.dropna(subset=['trade_type']).reset_index()

        # Assign a number to each complete trade
        df['trade_no'] = df['Volume'] = None

        # Assign a trade number to each complete sell-offs (where trader has no open opistions)
        df.loc[df.available_base < 0.0001, 'trade_no'] = df[df.available_base < 0.0001].reset_index().index

        df['trade_no'] = df['trade_no'].fillna(method='bfill')

        Volume = df[df.trade_type == "BUY"].groupby('trade_no')['paid_amounts'].sum()/100000
        Time1 = df[df.trade_type == "BUY"].groupby('trade_no').datetime.first()
        Time2 = df[df.trade_type == "SELL"].groupby('trade_no').datetime.last()

        # Calculate each trade real volume to calculate weighted average Price for real aggregated trades
        df['Volume'] = df.apply(lambda x: x.paid_amounts / x.buy_or_sell_price if x.trade_type ==
                                'BUY' else x.received_amounts / x.buy_or_sell_price, axis=1)
        df['sum_product'] = df['buy_or_sell_price'] * df['Volume']

        Price1 = df[df.trade_type == "BUY"].groupby('trade_no')['sum_product'].sum(
        ) / df[df.trade_type == "BUY"].groupby('trade_no')['Volume'].sum()
        Price2 = df[df.trade_type == "SELL"].groupby('trade_no')['sum_product'].sum(
        ) / df[df.trade_type == "SELL"].groupby('trade_no')['Volume'].sum()
        Profit = df[df.trade_type == "SELL"].groupby('trade_no')['received_amounts'].sum(
        ) - df[df.trade_type == "BUY"].groupby('trade_no')['paid_amounts'].sum()

        # Correction of QUOTE commissions with real (base) commission
        df.loc[df.trade_type == 'SELL', 'payment_commission'] = df[df.trade_type == 'SELL'].apply(
            lambda x: x.payment_commission * x.buy_or_sell_price, axis=1)
        Commission = df.groupby('trade_no')['payment_commission'].sum()

        # Building output
        Balance = pd.DataFrame([[pd.to_datetime(df.datetime[0]), 'Balance', 0.0, 0, 0.0, 0, 0, 0, 0.0, 0.0, 0, df.buy_and_hold[0], 0]], columns=['Time1', 'Type', 'Volume', 'Symbol', 'Price1', 'S/L', 'T/P', 'Time2',
                                                                                                                                                 'Price2', 'Commission', 'Swap', 'Profit', 'Comment'])
        zeros = [0]*len(Time1)
        Type = ['BUY']*len(Time1)
        Symbol = [file[:-4]]*len(Time1)

        out = pd.DataFrame({'Time1': Time1, 'Type': Type, 'Volume': Volume, 'Symbol': Symbol, 'Price1': Price1, 'S/L': zeros, 'T/P': zeros, 'Time2': Time2,
                            'Price2': Price2, 'Commission': Commission, 'Swap': zeros, 'Profit': Profit, 'Comment': zeros})

        out = pd.concat([Balance, out])
        out = out.rename(columns={'Time1': 'Time', 'Time2': 'Time', 'Price1': 'Price', 'Price2': 'Price'})
        out.to_csv(export_path + '/' + file)

    @property
    def Do(self) -> None:
        export_path = './Standard_' + self.__folder_path.rpartition('/')[-1]
        makedirs(export_path, exist_ok=True)

        tot_files = len(self.__csvfile_list)
        i = 1
        for file in self.__csvfile_list:
            self.__make_std_csv(self.__folder_path, file, export_path)

            self.__progress(int(i/tot_files*100))
            i += 1

    @staticmethod
    def __progress(percent=0, width=40):
        left = width * percent // 100
        right = width - left

        tags = "=" * left
        spaces = " " * right
        percents = f"{percent:.0f}%"

        print("\r[", tags, spaces, "] ", percents, sep="", end="", flush=True)
