import pyzillow.pyzillow as pz
import pandas as pd

class Zillow:
    def __init__(self):
        self.ZWSID =  'X1-ZWz182iruzkidn_9hc6e'
        self.zillow_data = pz.ZillowWrapper(self.ZWSID)


class Property(Zillow):
    def __init__(self, address, zip_code, city = None, state = None):
        Zillow.__init__(self)
        self.address = address
        self.city = city
        self.state = state
        self.zipCode = zip_code
        self.deepSearchResult = self.DeepSearchResult(address, zip_code)
        self.attributes = self.__Home_Attributes()
        #self.updatedPropertyResult = self.__UpdatedPropertyResult(int(self.attributes['Zillow_ID']))
        #self.updatedAttributes = self.__Updated_Details()

    def DeepSearchResult(self, address, zip_code):
        deep_search_response = self.zillow_data.get_deep_search_results(address, zip_code)
        return pz.GetDeepSearchResults(deep_search_response)

    def __UpdatedPropertyResult(self, zillow_id):
        updated_property_details_response = self.zillow_data.get_updated_property_details(zillow_id)
        return pz.GetUpdatedPropertyDetails(updated_property_details_response)

    def __Home_Attributes(self):
        attributes = {
            'Zillow_ID' : self.deepSearchResult.zillow_id,
            'home_type' : self.deepSearchResult.home_type,
            'tax_year' : self.deepSearchResult.tax_year,
            'tax_value' : self.deepSearchResult.tax_value,
            'year_built' : self.deepSearchResult.year_built,
            'property_size' : self.deepSearchResult.property_size,
            'home_size' : self.deepSearchResult.home_size,
            'bathrooms' : self.deepSearchResult.bathrooms,
            'bedrooms' : self.deepSearchResult.bedrooms,
            'last_sold_date' : self.deepSearchResult.last_sold_date,
            'last_sold_price' : self.deepSearchResult.last_sold_price
            }

        return attributes


    def __Updated_Details(self):
        attributes = {
            'Zillow_ID' : self.updatedPropertyResult.zillow_id,
            'home_type' : self.updatedPropertyResult.home_type,
            'year_built' : self.updatedPropertyResult.year_built,
            'property_size' : self.updatedPropertyResult.property_size,
            'home_size' : self.updatedPropertyResult.home_size,
            'bathrooms' : self.updatedPropertyResult.bathrooms,
            'bedrooms' : self.updatedPropertyResult.bedrooms,
            'home_info' : self.updatedPropertyResult.home_info,
            'year_updated' : self.updatedPropertyResult.year_updated,
            'floors' : self.updatedPropertyResult.floors,
            'basement' : self.updatedPropertyResult.basement,
            'roof' : self.updatedPropertyResult.roof,
            'view' : self.updatedPropertyResult.view,
            'heating_sources' : self.updatedPropertyResult.heating_sources,
            'heating_system' : self.updatedPropertyResult.heating_system,
            'rooms' : self.updatedPropertyResult.rooms,
            'neighborhood' : self.updatedPropertyResult.neighborhood,
            'school_district' : self.updatedPropertyResult.school_district,
            }

        return attributes
