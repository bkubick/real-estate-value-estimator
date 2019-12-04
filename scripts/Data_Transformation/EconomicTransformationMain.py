import pandas as pd

#List of filenames
unorg_directory = '../data/JSON/Unorganized/Economic/local/'
org_directory = '../data/JSON/Organized/Economic/'
filenames = ['PhoenixEconomic.json',
             'RedlandsEconomic.json',
             'SchaumburgEconomic.json']

populations = pd.read_json(unorg_directory + 'local_population.json')

column_numer = ['construction',
                  'education_and_health_services',
                  'financial_activities',
                  'government',
                  'information',
                  'leisure_and_hospitality',
                  'manufacturing',
                  'mining_and_logging',
                  'other_services',
                  'professional_and_business_services',
                  'total_nonfarm',
                  'trade_transportation_utilities']

#Reading into array of dfs
temp_data = []
for file in filenames:
    temp_df = pd.read_json(unorg_directory + file)
    temp_df[column_numer] = temp_df[column_numer]*1000

    temp_data.append(temp_df)

#Combining the years population with the year data
data = []
k = 0
for temp, file in zip(temp_data, filenames):
    if 'Pho' in file:
        data.append(pd.merge(temp, populations, on = 'year'))
        data[k]['population'] = data[k]['phoenix_pop']
        area = ['Phoenix']*(len(data[k]))
        data[k]['data_search'] = area

    elif 'Red' in file:
        data.append(pd.merge(temp, populations, on = 'year'))
        data[k]['population'] = data[k]['redlands_pop']
        area = ['Redlands']*(len(data[k]))
        data[k]['data_search'] = area

    elif 'Schaum' in file:
        data.append(pd.merge(temp, populations, on = 'year'))
        data[k]['population'] = data[k]['chicago_pop']
        area = ['Schaumburg']*(len(data[k]))
        data[k]['data_search'] = area

    data[k] = data[k].drop(columns = ['chicago_pop', 'phoenix_pop', 'redlands_pop', 'year'])
    k += 1

#Storing all economic data to new files in organized json files
for d, file in zip(data, filenames):
    d.to_json((org_directory + file), orient = 'records')
