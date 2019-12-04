import Constants
import pandas as pd
import numpy as np

class Combine_Data:
    def __init__(self, city = 'all'):
        #Initializing all constants in this class
        self.real_estate_data = None
        self.economic_data = None
        self.all_headers = None
        self.all_data = None

        #Combining the data in the files listed in Constants.py
        self.__combine_data(city = city)

    def __combine(self, files):

        data = []
        for file in files:
            data.append(pd.read_json(file))

        if len(data) == 1:
            return data[0]
        else:
            return pd.concat(data)

    def __combine_data(self, city):
        if city.lower() == 'all':
            self.real_estate_data = self.__combine(Constants.REAL_ESTATE_FILES)
            self.economic_data = self.__combine(Constants.ECONOMIC_FILES)
        elif city.lower() == 'phoenix':
            self.real_estate_data = self.__combine([Constants.REAL_ESTATE_FILES[0]])
            self.economic_data = self.__combine([Constants.ECONOMIC_FILES[0]])
        elif city.lower() == 'schaumburg':
            self.real_estate_data = self.__combine([Constants.REAL_ESTATE_FILES[1]])
            self.economic_data = self.__combine([Constants.ECONOMIC_FILES[1]])
        elif city.lower() == 'redlands':
            self.real_estate_data = self.__combine([Constants.REAL_ESTATE_FILES[2]])
            self.economic_data = self.__combine([Constants.ECONOMIC_FILES[2]])

        self.all_data = pd.merge(self.real_estate_data,
                                 self.economic_data,
                                 on = ['data_search', 'date'])
