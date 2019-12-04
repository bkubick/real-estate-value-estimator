import wbdata as wb
import pandas as pd

class WorldBankCountry:

    def __init__(self, indicators = None, country = None, source = None):
        self.country = country
        self.indicators = indicators
        self.source = source

    #Setters
    def set_Country(self, countries):
        self.country = countries

    def set_indicators(self, indicators):
        self.indicators = indicators

    def set_source(self, source):
        self.source = source

    #Searchers
    def search_sources(self):
        wb.get_source()

    def search_countries(self, search = 'United States'):
        return wb.search_countries(search)

    def search_indicators(self, search):
        return wb.search_indicators(search)

    #Getters
    def get_indicator(self):
        if self.source == None:
            print('No source Selected')
            self.search_sources()
        else:
            return wb.get_indicator(self.source)

    def get_incomelevel(self):
        return wb.get_incomelevel()

    def get_country_info(self):
        if self.country != None:
            return wb.get_country(country_id = self.country)
        else:
            return None

    def get_dataframe(self):
        if self.indicators != None and self.country != None:
            return wb.get_dataframe(self.indicators, country = self.country,
            convert_date = False)
        else:
            return None

    #Exporters
    def dataframe_to_json(self, filename):
        filename = '../data/Unorganized/Economic/' + filename + '.json'
        df = self.get_dataframe()

        if df != None:
            df.to_json(filename)
        elif self.country == None and self.indicators != None:
            print('No country selected')
        elif self.indicators == None and self.country != None:
            print('No indicators selected')
        else:
            print('Select country and indicators')
