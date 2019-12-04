import mysql.connector

try:
    #Declaring MySQL Connections
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="realestate"
    )
    mycursor = mydb.cursor()
    mycursor.execute("CREATE DATABASE real_estate")

except:
    #Declaring MySQL Connections
    mydb = mysql.connector.connect(
      host="localhost",
      user="root",
      passwd="realestate",
      database = "real_estate"
    )
    mycursor = mydb.cursor()

#Creating my tables
#Economic table
try:
    mycursor.execute("CREATE TABLE economic ("
                     "economic_ID INTEGER(8) NOT NULL AUTO_INCREMENT,"
                     "data_search VARCHAR(22) NOT NULL,"
                     "date DATE NOT NULL,"
                     "population INTEGER(9) NOT NULL,"
                     "employment INTEGER(9) NOT NULL,"
                     "unemployment INTEGER(9) NOT NULL,"
                     "unemployment_rates DECIMAL(5,2) NOT NULL,"
                     "civilian_labor_force INTEGER(9) NOT NULL,"
                     "construction INTEGER(9) NOT NULL,"
                     "education_and_health_services INTEGER(9) NOT NULL,"
                     "financial_activities INTEGER(9) NOT NULL,"
                     "government INTEGER(9) NOT NULL,"
                     "information INTEGER(9) NOT NULL,"
                     "leisure_and_hospitality INTEGER(9) NOT NULL,"
                     "manufacturing INTEGER(9) NOT NULL,"
                     "mining_and_logging INTEGER(9) NOT NULL,"
                     "professional_and_business_services INTEGER(9) NOT NULL,"
                     "total_nonfarm INTEGER(9) NOT NULL,"
                     "trade_transportation_utilities INTEGER(9) NOT NULL,"
                     "other_services INTEGER(9) NOT NULL,"
                     "PRIMARY KEY (economic_ID)"
                     ")")
except:
    print('Table already exists')

#Location Table
try:
    mycursor.execute("CREATE TABLE location ("
                     "zip_code INTEGER(5) NOT NULL,"
                     "city VARCHAR(22) NOT NULL,"
                     "state VARCHAR(13) NOT NULL,"
                     "data_search VARCHAR(22) NOT NULL,"
                     "PRIMARY KEY (zip_code)"
                     ")")
except:
    print('Table already exists')

#House Table
try:
    mycursor.execute("CREATE TABLE houses ("
                     "house_ID INTEGER(8) NOT NULL,"
                     "street VARCHAR(50) NOT NULL,"
                     "zip_code INTEGER(5) NOT NULL,"
                     "sqft INTEGER(6),"
                     "lot_size DECIMAL(4,2),"
                     "beds INTEGER(2),"
                     "baths DECIMAL(4,2),"
                     "year_built INTEGER(4),"
                     "property_type VARCHAR(25),"
                     "architecture VARCHAR(45),"
                     "exterior_finish VARCHAR(25),"
                     "flooring VARCHAR(25),"
                     "roofing VARCHAR(25),"
                     "water VARCHAR(25),"
                     "cooling VARCHAR(25),"
                     "heating VARCHAR(25),"
                     "fireplace BOOLEAN,"
                     "fencing VARCHAR(25),"
                     "pool BOOLEAN,"
                     "spa BOOLEAN,"
                     "garage BOOLEAN,"
                     "patio BOOLEAN,"
                     "elementary_dis DECIMAL(4,2),"
                     "middle_dis DECIMAL(4,2),"
                     "high_dis DECIMAL(4,2),"
                     "data_search VARCHAR(22),"
                     "PRIMARY KEY (house_ID),"
                     "FOREIGN KEY (zip_code) REFERENCES location(zip_code)"
                     ")")
except:
    print('Table already exists')

#Price history table
try:
    mycursor.execute("CREATE TABLE price_history ("
                     "history_ID INTEGER(8) NOT NULL AUTO_INCREMENT,"
                     "house_ID INTEGER(8) NOT NULL,"
                     "date DATE NOT NULL,"
                     "event VARCHAR(13) NOT NULL,"
                     "price INTEGER(8) NOT NULL,"
                     "PRIMARY KEY (history_ID),"
                     "FOREIGN KEY (house_ID) REFERENCES houses(house_ID)"
                     ")")
except:
    print('Table already exists')
