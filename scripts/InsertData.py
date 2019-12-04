import mysql.connector
import pandas as pd
from Machine_Learning.CombineData import Combine_Data

#Declaring MySQL Connections
mydb = mysql.connector.connect(
  host="localhost",
  user="root",
  passwd="realestate",
  database = "real_estate"
)
mycursor = mydb.cursor()

#Getting a dataframe of all the data
combined_data = Combine_Data()
all_data = combined_data.all_data
all_data = all_data.replace({pd.np.nan:None})

#economic table
econ = ["data_search",
      "date",
      "population",
      "employment",
      "unemployment",
      "unemployment_rates",
      "civilian_labor_force",
      "construction",
      "education_and_health_services",
      "financial_activities",
      "government",
      "information",
      "leisure_and_hospitality",
      "manufacturing",
      "mining_and_logging",
      "professional_and_business_services",
      "total_nonfarm",
      "trade_transportation_utilities",
      "other_services"]

sql_econ = "INSERT INTO economic (" \
      "data_search, " \
      "date, " \
      "population, " \
      "employment, " \
      "unemployment, " \
      "unemployment_rates, " \
      "civilian_labor_force, " \
      "construction, " \
      "education_and_health_services, " \
      "financial_activities, " \
      "government, " \
      "information, " \
      "leisure_and_hospitality, " \
      "manufacturing, " \
      "mining_and_logging," \
      "professional_and_business_services, " \
      "total_nonfarm, " \
      "trade_transportation_utilities, " \
      "other_services) " \
      "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

econ_data = all_data[econ]
econ_data_tuples = [tuple(x) for x in econ_data.values]
mycursor.executemany(sql_econ, econ_data_tuples)

#location table
location = ["data_search",
      "city",
      "state",
      "zip_code"]

sql_location = "INSERT INTO location (" \
      "data_search, " \
      "city, " \
      "state, " \
      "zip_code) " \
      "VALUES (%s,%s,%s,%s)"

location_data = all_data[location]
zip_codes = []
location_data_tuples = []
for i in range(0, len(location_data)):
    if location_data['zip_code'][i] not in zip_codes:
        data_search = location_data['data_search'][i]
        city = location_data['city'][i]
        state = location_data['state'][i]
        zip_code = int(location_data['zip_code'][i])
        location_data_tuples.append((data_search, city, state, zip_code))
        zip_codes.append(location_data['zip_code'][i])

mycursor.executemany(sql_location, location_data_tuples)

#houses table
houses = ["house_ID",
      "street",
      "zip_code",
      "sqft",
      "lot_size",
      "beds",
      "baths",
      "year_built",
      "property_type",
      "architecture",
      "exterior_finish",
      "flooring",
      "roofing",
      "water",
      "cooling",
      "heating",
      "fireplace",
      "pool",
      "spa",
      "garage",
      "patio",
      "elementary_dis",
      "middle_dis",
      "high_dis",
      "data_search"]

sql_houses = "INSERT INTO houses (" \
      "house_ID, " \
      "street, " \
      "zip_code, " \
      "sqft, " \
      "lot_size, " \
      "beds, " \
      "baths, " \
      "year_built, " \
      "property_type, " \
      "architecture, " \
      "exterior_finish, " \
      "flooring, " \
      "roofing, " \
      "water, " \
      "cooling," \
      "heating, " \
      "fireplace, " \
      "pool, " \
      "spa, " \
      "garage, " \
      "patio, " \
      "elementary_dis, " \
      "middle_dis, " \
      "high_dis, " \
      "data_search) " \
      "VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)"

house_data = all_data[houses]
house_data_tuples = []
house_IDS = []
for i in range(0, len(house_data)):
    if house_data['house_ID'][i] not in house_IDS:
        house_ID = int(house_data["house_ID"][i])
        street = house_data["street"][i]
        zip_code = int(house_data["zip_code"][i])
        sqft = house_data["sqft"][i]
        if type(house_data["lot_size"][i]) == type(None):
            lot_size = house_data["lot_size"][i]
        else:
            lot_size = round(house_data["lot_size"][i],2)

        beds = house_data["beds"][i]
        baths = house_data["baths"][i]
        year_built = house_data["year_built"][i]
        property_type = house_data["property_type"][i]
        architecture = house_data["architecture"][i]
        exterior_finish = house_data["exterior_finish"][i]
        flooring = house_data["flooring"][i]
        roofing = house_data["roofing"][i]
        water = house_data["water"][i]
        cooling = house_data["cooling"][i]
        heating = house_data["heating"][i]
        if type(house_data["fireplace"][i]) == type(None):
            fireplace = house_data["fireplace"][i]
        else:
            fireplace = int(house_data["fireplace"][i])

        if type(house_data["pool"][i]) == type(None):
            pool = house_data["pool"][i]
        else:
            pool = int(house_data["pool"][i])

        if type(house_data["spa"][i]) == type(None):
            spa = house_data["spa"][i]
        else:
            spa = int(house_data["spa"][i])

        if type(house_data["garage"][i]) == type(None):
            garage = house_data["garage"][i]
        else:
            garage = int(house_data["garage"][i])

        if type(house_data["patio"][i]) == type(None):
            patio = house_data["patio"][i]
        else:
            patio = int(house_data["patio"][i])

        if type(house_data["elementary_dis"][i]) == type(None):
            elementary_dis = house_data["elementary_dis"][i]
        else:
            elementary_dis = round(house_data["elementary_dis"][i],2)

        if type(house_data["middle_dis"][i]) == type(None):
            middle_dis = house_data["middle_dis"][i]
        else:
            middle_dis = round(house_data["middle_dis"][i],2)

        if type(house_data["high_dis"][i]) == type(None):
            high_dis = house_data["high_dis"][i]
        else:
            high_dis = round(house_data["high_dis"][i],2)

        data_search = house_data["data_search"][i]

        temp_tuple = (
            house_ID,
            street,
            zip_code,
            sqft,
            lot_size,
            beds,
            baths,
            year_built,
            property_type,
            architecture,
            exterior_finish,
            flooring,
            roofing,
            water,
            cooling,
            heating,
            fireplace,
            pool,
            spa,
            garage,
            patio,
            elementary_dis,
            middle_dis,
            high_dis,
            data_search
        )

        house_data_tuples.append(temp_tuple)
        house_IDS.append(house_ID)

mycursor.executemany(sql_houses, house_data_tuples)

#price_history table
history = ["house_ID",
      "date",
      "event",
      "price"]

sql_history = "INSERT INTO price_history (" \
      "house_ID, " \
      "date, " \
      "event, " \
      "price) " \
      "VALUES (%s,%s,%s,%s)"

history_data = all_data[history]
history_data_tuples = [tuple(x) for x in history_data.values]
mycursor.executemany(sql_history, history_data_tuples)

mydb.commit()
