from Data_APIs.BLS import BLS
import Constants
import pandas as pd

def bls_series(area_series_ids, filenames):
    for series_ids, filename in zip(area_series_ids, filenames):
            bls = BLS(series_id = series_ids,
                      start_year = Constants.start_year,
                      end_year = Constants.end_year)
            bls.set_all_data()
            bls.export_data('local', filename)

#Getting city Data
local_series_ids = [Constants.az_bls_series_ids,
                       Constants.ca_bls_series_ids,
                       Constants.il_bls_series_ids]

local_filenames = ['phoenixEconomic',
                   'redlandsEconomic',
                   'schaumburgEconomic']

bls_series(local_series_ids, local_filenames)

#Storing populations found on U.S Census Bureau
local_pop = pd.read_csv('../data/CSV/Economic/local_population.csv')
local_pop.to_json('../data/JSON/Unorganized/Economic/local/local_population.json',
                  orient = 'records')
