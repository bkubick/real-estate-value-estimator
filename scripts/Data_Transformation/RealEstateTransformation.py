import numpy as np
import pandas as pd
import string
import random

class Real_Estate_Transformation:
    def __init__(self, homes_search, file_read, file_export, min_id_range, max_id_range):
        self.min_id_range = min_id_range
        self.max_id_range = max_id_range
        self.homes_search = homes_search
        self.id_list = []

        #Reading in the dataframe
        data = pd.read_json(file_read)
        houses = data.iloc[:, :].to_numpy()

        #DF Indices
        address_index = data.columns.get_loc("address")
        details_index = data.columns.get_loc("details")
        history_index = data.columns.get_loc("pricing")
        schools_index = data.columns.get_loc("schools")
        sqft_index = data.columns.get_loc("sqft")

        #Declaring the indices for the elementary, middle, and high school
        elem_index = 0
        mid_index = 1
        high_index = 2

        #Creating the dataframes for each corresponding year
        df = pd.DataFrame()
        for house in houses:
            #Removing any house without an address, city or state
            if len(house[address_index]) == 1:
                continue

            #setting the house_ID
            house_ID = self.id_generator()

            #Seperating the address to street, city, state, and zip_code
            street = house[address_index][0]
            location = self.word_seperator(house[address_index][1])
            city = ' '.join(location[0:-2])

            #The scraped website had a lot of spelling errors with phoenix
            city_lower = city.lower()
            if 'ph' in city_lower and 'x' in city_lower and 'i' in city_lower:
                city = 'Phoenix'

            state = location[-2]
            zip_code = location[-1]

            #Setting the Sqft
            if len(house[sqft_index])>0 and '--' not in house[sqft_index]:
                sqft = self.intify(house[sqft_index])
            else:
                sqft = None

            #Setting the school distances
            if len(house[schools_index])>=3 and '--' not in house[schools_index]:
                elementary_dis = self.floatify(house[schools_index][elem_index][1][0])
                if elementary_dis is not None:
                    elementary_dis = round(elementary_dis, 2)

                middle_dis = self.floatify(house[schools_index][mid_index][1][0])
                if middle_dis is not None:
                    middle_dis = round(middle_dis, 2)

                high_dis = self.floatify(house[schools_index][high_index][1][0])
                if high_dis is not None:
                    high_dis = round(high_dis, 2)
            else:
                elementary_dis = None
                middle_dis = None
                high_dis = None

            #Initializing the detailed variables
            house_variables = {
                'house_ID': house_ID,
                'date': None,
                'event': None, #enum
                'price': None,
                'street': street,
                'city': city,
                'state': state,
                'zip_code': zip_code,
                'sqft': sqft,
                'elementary_dis': elementary_dis,
                'middle_dis': middle_dis,
                'high_dis': high_dis,
                'beds': None,
                'baths': None,
                'property_type': None, #string
                'year_built': None,
                'lot_size': None,
                'exterior_finish': None,
                'fireplace': None,
                'roofing': None,
                'fencing': None,
                'pool': None,
                'spa': None,
                'flooring': None,
                'water': None,
                'cooling': None,
                'heating': None,
                'garage': None,
                'patio': None,
                'architecture': None,
                'data_search': self.homes_search
            }

            #Setting the details of the house
            house_details = house[details_index]
            for detail in house_details:
                if len(detail) == 1:
                    continue

                detail_name = detail[0].lower()
                detail_parameter = detail[1]

                if '--' in detail_parameter:
                    continue

                if detail_name == 'beds':
                    house_variables['beds'] = self.intify(detail_parameter)

                elif detail_name == 'baths':
                    house_variables['baths'] = self.intify(detail_parameter)

                elif detail_name == 'property type':
                    detail_parameter = detail_parameter.lower()

                    #Alot of roof details had extra words in it
                    if 'residential' in detail_parameter:
                        detail_parameter = 'residential'
                    elif 'condominium' in detail_parameter:
                        detail_parameter = 'condominium'
                    elif 'townhouse' in detail_parameter:
                        detail_parameter = 'townhouse'
                    elif 'multi' in detail_parameter:
                        detail_parameter = 'multi family'
                    elif 'mobile' in detail_parameter:
                        detail_parameter = 'mobile'
                    elif 'single' in detail_parameter:
                        detail_parameter = 'single family'
                    else:
                        detail_parameter = 'other type'

                    house_variables['property_type'] = detail_parameter

                elif detail_name == 'year built':
                    house_variables['year_built'] = self.intify(detail_parameter)

                elif detail_name == 'lot size':
                    if '-' in detail_parameter:
                        detail_parameter = detail_parameter[0]

                    lot_size = self.floatify(detail_parameter)
                    if lot_size > 50:
                        lot_size = self.sqft_to_acre(lot_size)
                    house_variables['lot_size'] = lot_size

                elif detail_name == 'exterior finish':
                    detail_parameter = detail_parameter.lower()

                    #Alot of roof details had extra words in it
                    if 'concrete' in detail_parameter:
                        detail_parameter = 'concrete exterior'
                    elif 'wood' in detail_parameter:
                        detail_parameter = 'wood exterior'
                    elif 'metal' in detail_parameter:
                        detail_parameter = 'metal exterior'
                    elif 'brick' in detail_parameter:
                        detail_parameter = 'brick exterior'
                    elif 'stucco' in detail_parameter:
                        detail_parameter = 'stucco exterior'
                    elif 'stone' in detail_parameter:
                        detail_parameter = 'stone exterior'
                    else:
                        detail_parameter = 'other exterior'

                    house_variables['exterior_finish'] = detail_parameter

                elif detail_name == 'fireplace':
                    if detail[1] == 'yes':
                        house_variables['fireplace'] = 1
                    else:
                        house_variables['fireplace'] = 0

                elif detail_name == 'roof':
                    detail_parameter = detail_parameter.lower()

                    #Alot of roof details had extra words in it
                    if 'shingle' in detail_parameter:
                        detail_parameter = 'shingle roof'
                    elif 'tile' in detail_parameter:
                        detail_parameter = 'tile roof'
                    elif 'metal' in detail_parameter:
                        detail_parameter = 'metal roof'
                    elif 'asphalt' in detail_parameter:
                        detail_parameter = 'asphalt roof'
                    elif 'cement' in detail_parameter:
                        detail_parameter = 'cement roof'
                    elif 'rock' in detail_parameter:
                        detail_parameter = 'rock roof'
                    elif 'clay' in detail_parameter:
                        detail_parameter = 'clay roof'
                    elif 'composition' in detail_parameter:
                        detail_parameter = 'composition roof'
                    elif 'roll' in detail_parameter:
                        detail_parameter = 'roll roof'
                    elif 'foam' in detail_parameter:
                        detail_parameter = 'foam roof'
                    else:
                        detail_parameter = 'other roof'

                    house_variables['roofing'] = detail_parameter

                elif detail_name == 'fencing':
                    detail_parameter = detail_parameter.lower()

                    if 'wire' in detail_parameter:
                        detail_parameter = 'wire fencing'
                    elif 'chain' in detail_parameter:
                        detail_parameter = 'chain fencing'
                    elif 'wood' in detail_parameter:
                        detail_parameter = 'wood fencing'
                    elif 'concrete' in detail_parameter:
                        detail_parameter = 'concrete fencing'
                    else:
                        detail_parameter = 'other fencing'

                    house_variables['fencing'] = detail_parameter

                elif detail_name == 'pool':
                    if 'no' in detail[1]:
                        house_variables['pool'] = 0
                    else:
                        house_variables['pool'] = 1

                elif detail_name == 'spa':
                    if 'no' in detail_parameter:
                        house_variables['spa'] = 0
                    else:
                        house_variables['spa'] = 1

                elif detail_name == 'flooring':
                    detail_parameter = detail_parameter.lower()

                    if 'stone' in detail_parameter:
                        detail_parameter = 'stone flooring'
                    elif 'tile' in detail_parameter:
                        detail_parameter = 'tile flooring'
                    elif 'carpet' in detail_parameter:
                        detail_parameter = 'carpet flooring'
                    elif 'ceramic' in detail_parameter:
                        detail_parameter = 'ceramic flooring'
                    elif 'wood' in detail_parameter:
                        detail_parameter = 'wood flooring'
                    elif 'vinyl' in detail_parameter:
                        detail_parameter = 'vinyl flooring'
                    elif 'laminate' in detail_parameter:
                        detail_parameter = 'laminate flooring'
                    elif 'linoleum' in detail_parameter:
                        detail_parameter = 'linoleum flooring'
                    else:
                        detail_parameter = 'other flooring'

                    house_variables['flooring'] = detail_parameter

                elif detail_name == 'water':
                    detail_parameter = detail_parameter.lower()

                    if 'city' in detail_parameter:
                        detail_parameter = 'city'
                    elif 'well' in detail_parameter:
                        detail_parameter = 'well'
                    elif 'lake' in detail_parameter:
                        detail_parameter = 'lake'
                    elif 'none' in detail_parameter or 'not' in detail_parameter:
                        detail_parameter = 'no'
                    else:
                        detail_parameter = 'other'

                    house_variables['water'] = detail_parameter

                elif detail_name == 'cooling':
                    detail_parameter = detail_parameter.lower()

                    if 'refrig' in detail_parameter:
                        detail_parameter = 'refrigeration cooling'
                    elif 'thmstat' in detail_parameter:
                        detail_parameter = 'thmstat cooling'
                    elif 'evap' in detail_parameter:
                        detail_parameter = 'evaporation cooling'
                    elif 'central' in detail_parameter:
                        detail_parameter = 'central air cooling'
                    elif 'gas' in detail_parameter:
                        detail_parameter = 'gas cooling'
                    elif 'a/c' in detail_parameter:
                        detail_parameter = 'a/c cooling'
                    elif 'fan' in detail_parameter:
                        detail_parameter = 'fans cooling'
                    elif 'none' in detail_parameter or 'no' in detail_parameter:
                        detail_parameter = 'no cooling'
                    else:
                        detail_parameter = 'other cooling'

                    house_variables['cooling'] = detail_parameter

                elif detail_name == 'heating':
                    detail_parameter = detail_parameter.lower()

                    if 'elec' in detail_parameter:
                        detail_parameter = 'electric heating'
                    elif 'gas' in detail_parameter:
                        detail_parameter = 'gas heating'
                    elif 'central' in detail_parameter:
                        detail_parameter = 'central air heating'
                    elif 'furnace' in detail_parameter:
                        detail_parameter = 'furnace heating'
                    elif 'fire' in detail_parameter:
                        detail_parameter = 'fireplace heating'
                    elif 'fan' in detail_parameter:
                        detail_parameter = 'fans heating'
                    elif 'no' in detail_parameter:
                        detail_parameter = 'no heating'
                    else:
                        detail_parameter = 'other heating'

                    house_variables['heating'] = detail_parameter

                elif detail_name == 'garage':
                    if 'no' in detail_parameter:
                        house_variables['garage'] = 0
                    else:
                        house_variables['garage'] = 1

                elif detail_name == 'patio':
                    if 'no' in detail_parameter:
                        house_variables['patio'] = 0
                    else:
                        house_variables['patio'] = 1

                elif detail_name == 'architecture':
                    detail_parameter = detail_parameter.lower()

                    if 'custom' in detail_parameter:
                        detail_parameter = 'custom architecture'
                    elif 'ranch' in detail_parameter:
                        detail_parameter = 'ranch architecture'
                    elif 'contemp' in detail_parameter:
                        detail_parameter = 'contemporary architecture'
                    elif 'modern' in detail_parameter:
                        detail_parameter = 'modern architecture'
                    elif 'spanish' in detail_parameter:
                        detail_parameter = 'spanish architecture'
                    elif 'medit' in detail_parameter:
                        detail_parameter = 'mediterranean architecture'
                    elif 'victorian' in detail_parameter:
                        detail_parameter = 'victorian architecture'
                    elif 'bungalow' in detail_parameter:
                        detail_parameter = 'bungalow architecture'
                    else:
                        detail_parameter = 'other architecture'

                    house_variables['architecture'] = detail_parameter

            #Separating the entries by dates between 2000 and 2019
            history = house[history_index]
            for his in history:
                #making sure the date is between 2000 and 2019
                year = self.intify(his[0][-4:])
                if year < 2000:
                    continue

                #Storing the other variables
                house_variables['date'] = his[0][0:2] + '/' + his[0][-4:]
                house_variables['event'] = his[1]
                house_variables['price'] = self.intify(his[3])

                df = df.append(house_variables, ignore_index = True)

        df.to_json(file_export,orient='records')

    #Functions
    def list_to_array(self, list_type):
        array_type = []
        for i in range(0, len(list_type)):
            if len(list_type[i]) == 0:
                array_type.append(list_type[i])
            else:
                array_type.append(list_type[i][0])
        return array_type

    def no_comma(self, string_array):
        no_comma_array = []

        for i in range(0, len(string_array)):
            if len(string_array[i]) == 0:
                no_comma_array.append(string_array[i])
            else:
                no_comma_array.append(string_array[i].replace(',', ''))
        return no_comma_array

    def string_to_int_array(self, string_array):
        int_array = []
        for str in string_array:
            if len(str) == 0:
                int_array.append(str)
            else:
                int_array.append(int(float(str)))
        return int_array

    def word_seperator(self, sentence):
        if len(sentence) == 0:
            return string_array

        sentence = self.remove_punctuation(sentence)
        if sentence[0] == " ":
            sentence = sentence.replace(" ", "", 1)

        return sentence.split(" ")

    def remove_punctuation(self, str):
        return "".join(l for l in str if l not in string.punctuation)

    def remove_letters(self, str):
        new = ''
        for letter in str:
            if not letter.isalpha():
                new += letter
        return new

    def intify(self, str):
        str = self.remove_letters(str)
        str = self.remove_punctuation(str)
        str = str.replace(" ", "")
        if len(str)==0:
            return None
        return int(float(str))

    def floatify(self, str):
        str = self.remove_letters(str)
        str = str.replace(" ", "")
        if len(str)==0:
            return None

        if '/' in str:
            temp = str.split("/")
            str = float(temp[0]) / float(temp[1])
        return float(str)

    def id_generator(self):
        id = random.randint(self.min_id_range, self.max_id_range)

        while id in self.id_list:
            id = random.randint(self.min_id_range, self.max_id_range)

        self.id_list.append(id)

        return id
    def sqft_to_acre(self, sqft):
        return sqft/43560.0
