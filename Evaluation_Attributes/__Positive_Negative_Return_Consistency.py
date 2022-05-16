from pandas import DataFrame
from .__Duration_Consistency import Duration



class R_plus_minus(Duration):

    def __init__(self, data:DataFrame)-> None:
        Duration.__init__(self,data) 