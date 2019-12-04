from RealEstateTransformation import Real_Estate_Transformation as DET

phoenix_data = DET(homes_search = 'Phoenix',
                   file_read = '../data/JSON/Unorganized/RealEstate/AllPhoenixHomes.json',
                   file_export = '../data/JSON/Organized/RealEstate/PhoenixHomes.json',
                   min_id_range = 1000000000,
                   max_id_range = 1001999999)

schaumburg_data = DET(homes_search = 'Schaumburg',
                   file_read = '../data/JSON/Unorganized/RealEstate/AllSchaumburgHomes.json',
                   file_export = '../data/JSON/Organized/RealEstate/SchaumburgHomes.json',
                   min_id_range = 1020000000,
                   max_id_range = 1020999999)

redlands_data = DET(homes_search = 'Redlands',
                   file_read = '../data/JSON/Unorganized/RealEstate/AllRedlandsHomes.json',
                   file_export = '../data/JSON/Organized/RealEstate/RedlandsHomes.json',
                   min_id_range = 1031000000,
                   max_id_range = 1031999999)
