'''
Constants used in data
'''
#JSON Files stored
REAL_ESTATE_FILES = ['../data/JSON/Organized/RealEstate/PhoenixHomes.json',
                     '../data/JSON/Organized/RealEstate/SchaumburgHomes.json',
                     '../data/JSON/Organized/RealEstate/RedlandsHomes.json'
                     ]

ECONOMIC_FILES = ['../data/JSON/Organized/Economic/phoenixEconomic.json',
                  '../data/JSON/Organized/Economic/schaumburgEconomic.json',
                  '../data/JSON/Organized/Economic/redlandsEconomic.json'
                     ]

#Data preprocessing
MISSING_DATA_THRESHOLD = 0.2
COLUMNS_TO_DROP = ['data_search',
                   'street',
                   'city',
                   'state',
                   'house_ID']

COLUMNS_TO_ENCODE = ['property_type',
                     'exterior_finish',
                     'roofing',
                     'fencing',
                     'flooring',
                     'water',
                     'cooling',
                     'heating',
                     'architecture',
                     'zip_code']

#Divide these columns by COLUMNS_TO_DIVIDE_BY and change to COLUMNS_TO_ADD
COLUMNS_TO_DIVIDE =  ['employment',
                      'civilian_labor_force',
                      'construction',
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
                      'trade_transportation_utilities',
                      'unemployment']

COLUMNS_TO_DIVIDE_BY = ['population']

COLUMNS_TO_ADD = ['emp_norm',
                  'clf_norm',
                  'con_norm',
                  'edu_hel_norm',
                  'fin_norm',
                  'gov_norm',
                  'info_norm',
                  'leis_norm',
                  'manuf_norm',
                  'min_norm',
                  'other_norm',
                  'prof_bus_norm',
                  'nonfarm_norm',
                  'trade_norm',
                  'unemp_norm']

ECON_DATA = ['population',
              'employment',
              'civilian_labor_force',
              'construction',
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
              'trade_transportation_utilities',
              'unemployment',
              'unemployment_rates']


TEST_YEARS = [2019]

#BLS Constants
start_year = 2000
end_year = 2019

az_bls_series_ids = {'unemployment_rates': 'LAUMT043806000000003',
                     'unemployment': 'LAUMT043806000000004',
                     'employment': 'LAUMT043806000000005',
                     'civilian_labor_force': 'LAUMT043806000000006',
                     'total_nonfarm': 'SMU04380600000000001',
                     'mining_and_logging': 'SMU04380601000000001',
                     'construction': 'SMU04380602000000001',
                     'manufacturing': 'SMU04380603000000001',
                     'trade_transportation_utilities': 'SMU04380604000000001',
                     'information': 'SMU04380605000000001',
                     'financial_activities': 'SMU04380605500000001',
                     'professional_and_business_services': 'SMU04380606000000001',
                     'education_and_health_services': 'SMU04380606500000001',
                     'other_services': 'SMU04380608000000001',
                     'government': 'SMU04380609000000001',
                     'leisure_and_hospitality': 'SMU04380607000000001',
                     }

ca_bls_series_ids = {'unemployment_rates': 'LAUMT064014000000003',
                     'unemployment': 'LAUMT064014000000004',
                     'employment': 'LAUMT064014000000005',
                     'civilian_labor_force': 'LAUMT064014000000006',
                     'total_nonfarm': 'SMU06401400000000001',
                     'mining_and_logging': 'SMU06401401000000001',
                     'construction': 'SMU06401402000000001',
                     'manufacturing': 'SMU06401403000000001',
                     'trade_transportation_utilities': 'SMU06401404000000001',
                     'information': 'SMU06401405000000001',
                     'financial_activities': 'SMU06401405500000001',
                     'professional_and_business_services': 'SMU06401406000000001',
                     'education_and_health_services': 'SMU06401406500000001',
                     'other_services': 'SMU06401408000000001',
                     'government': 'SMU06401409000000001',
                     'leisure_and_hospitality': 'SMU06401407000000001',
                     }

il_bls_series_ids = {'unemployment_rates': 'LAUMT171698000000003',
                     'unemployment': 'LAUMT171698000000004',
                     'employment': 'LAUMT171698000000005',
                     'civilian_labor_force': 'LAUMT171698000000006',
                     'total_nonfarm': 'SMU17169800000000001',
                     'mining_and_logging': 'SMU17169801000000001',
                     'construction': 'SMU17169802000000001',
                     'manufacturing': 'SMU17169803000000001',
                     'trade_transportation_utilities': 'SMU06401404000000001',
                     'information': 'SMU17169805000000001',
                     'financial_activities': 'SMU17169805500000001',
                     'professional_and_business_services': 'SMU17169806000000001',
                     'education_and_health_services': 'SMU17169806500000001',
                     'other_services': 'SMU17169808000000001',
                     'government': 'SMU17169809000000001',
                     'leisure_and_hospitality': 'SMU17169807000000001',
                     }
