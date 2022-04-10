from pandas import read_csv 
from os import listdir



class Preparation:

    def __init__(self,folder_path:str)-> None:

        self.__csvfile_list = self.__read_folder(folder_path)
                    


    @staticmethod
    def __read_folder(path:str)-> list:
        csvfile_name = []
        for asset in listdir(path):
            if asset.find('csv') != -1 : csvfile_name.append(asset)
        if len(csvfile_name) == 0 :
            raise TypeError (
                'this class defined for find and read csv file in floder path '
            )
        return csvfile_name
        
