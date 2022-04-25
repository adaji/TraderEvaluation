from datetime import date
from .connection import Connection
from .utils import retry
import pandas as pd
import os
import pickle


class DataCon():
    """
    This class is used to connect api project and get data from eikon and dukascopy.
    """

    def __init__(self, server_address: str):
        """
        Parameters
        ----------
        server_address: str required
            the address of the server that is going to be used
        """
        self.server_address = server_address
        self.con = Connection()

    @retry(tries=5, delay=1, print_excp=True)
    def get_daily_data(self, ticker: list[str], start_date: date, end_date: date):
        """
        get daily data from api

        Parameters
        ----------
        ticker: list of str required
            list of tickers that are going to be used
        start_date: date required
            the start date of the data
        end_date: date required
            the end date of the data
        """
        url = self.server_address + "/daily/"
        data = {'ticker': t for t in ticker}
        data['start_date'] = start_date.strftime('%Y-%m-%d')
        data['end_date'] = end_date.strftime('%Y-%m-%d')
        df = self.con.fetch(url, data)
        df = pd.DataFrame(df)
        return df

    def get_m1_data(self, ticker: str, d_date: date):
        """
        get m1 data from api

        Parameters
        ----------
        ticker: str required
            the ticker that is going to be used
        d_date: date required
            the date of the data
        """
        url = self.server_address + "/m1/"
        data = {'ticker': ticker, 'date': d_date.strftime('%Y-%m-%d')}
        df = self.con.fetch(url, data)
        df = pd.DataFrame(df)
        return df
