import requests
import json
import pandas as pd

class BLS:
    def __init__(self, series_id = None,
                headers = {'Content-type': 'application/json'},
                start_year = None, end_year = None):

        self.set_series_id(series_id)
        self.headers = headers #dictionary
        self.start_year = str(start_year) #string
        self.end_year = str(end_year) #string
        self.all_data = None
        self.data = None

    def set_series_id(self, series_id = None):
        if series_id == None:
            self.series_id = None
            self.series = None
        elif type(series_id) != dict:
            print('Series_id is not a dictionary')
            self.series_id = None
            self.series = None
        else:
            self.series_id = []
            self.series = []
            for k, v in series_id.items():
                self.series_id.append(v)
                self.series.append(k)

    def set_start_year(self, start_year):
        if start_year == None:
            print('No start year entered')
        else:
            self.start_year = str(start_year)

    def set_end_year(self, end_year):
        if end_year == None:
            print('No end year entered')
        elif end_year < self.start_year:
            print('Start Year is greater than end year')
            return
        else:
            self.end_year = str(end_year)

    def set_all_data(self):
        if self.series_id == None:
            print("No series selected")
            return
        elif self.start_year == None:
            print("No start year selected")
            return
        elif self.end_year == None:
            print("No end year selected")
            return

        #Adjusting date if it has a greater than 10 year time gap
        self.__adjust_date()

        self.json_data = []
        for start_year, end_year in zip(self.start_year, self.end_year):
            #Getting the data from bls
            data = json.dumps({"seriesid": self.series_id,
                               "startyear": start_year,
                               "endyear": end_year})
            p = requests.post('https://api.bls.gov/publicAPI/v2/timeseries/data/',
                              data=data, headers=self.headers)
            self.json_data.append(json.loads(p.text))

        #Storing all the data to a list of DataFrames for each series
        self.__all_data = []
        for js in self.json_data:
            series = js['Results']['series']
            for s in series:
                self.__all_data.append(pd.DataFrame(s['data']))

        #Combining
        self.__combine_years()

        self.__set_data()

    #Turning dates to a list of dates
    def __adjust_date(self):
        if (int(self.end_year) - int(self.start_year) + 1) < 10:
            self.start_year = [self.start_year]
            self.end_year = [self.end_year]

        else:
            diff = int(self.end_year) - int(self.start_year) + 1
            start_year_fin = int(self.start_year)
            end_year_fin = int(self.end_year)
            sy = start_year_fin
            ey = sy + 9

            self.start_year = []
            self.end_year = []

            if int(diff % 10) == 0:
                periods_of_ten = int(diff / 10)
            else:
                periods_of_ten = int(diff / 10) + 1

            for i in range(0, periods_of_ten ):
                self.start_year.append(str(sy))
                self.end_year.append(str(ey))
                sy = ey + 1

                if int((end_year_fin - sy + 1 ) / 10) > 0:
                    ey = sy + 9
                else:
                    leftover = (end_year_fin - sy + 1) % 10
                    ey = ey + leftover


    #Combining all years for the same series
    def __combine_years(self):
        self.all_data = []
        k = 0
        for i in range(0, len(self.series)):
            same_series = []
            k = i
            for j in range(0, len(self.start_year)):
                same_series.append(self.__all_data[k])
                k += len(self.series)
            self.all_data.append(pd.concat(same_series))

    def __set_data(self):
        self.__data = []

        for d, s in zip(self.all_data, self.series):
            temp = {
                'year': None,
                'date': None,
                }

            temp[s] = None

            value = []
            month = []
            year = []
            for key in d:
                if key == 'value':
                    for val in d[key]:
                      value.append(val)


                elif key == 'period':
                    for p in d[key]:
                        if p == 'M01':
                            month.append('01')
                        elif p == 'M02':
                            month.append('02')
                        elif p == 'M03':
                            month.append('03')
                        elif p == 'M04':
                            month.append('04')
                        elif p == 'M05':
                            month.append('05')
                        elif p == 'M06':
                            month.append('06')
                        elif p == 'M07':
                            month.append('07')
                        elif p == 'M08':
                            month.append('08')
                        elif p == 'M09':
                            month.append('09')
                        elif p == 'M10':
                            month.append('10')
                        elif p == 'M11':
                            month.append('11')
                        elif p == 'M12':
                            month.append('12')

                elif key == 'year':
                    for y in d[key]:
                        year.append(y)

            date = []
            for m, y in zip(month, year):
                date.append(m + '/' + y)

            temp['date'] = date
            temp['year'] = year
            temp[s] = value
            self.__data.append(pd.DataFrame(temp))
            self.__combine_data()

    def __combine_data(self):
        self.data = pd.DataFrame()
        for d in self.__data:
            if len(self.data) == 0:
                self.data = d
            else:
                self.data = pd.merge(self.data, d, on = ['year','date'])
        self.data = self.data.sort_values(by = ['year', 'date'])

    def export_data(self, folder, filename = None):
        if filename == None:
            print('Select a filename')
        else:
            filename = '../data/JSON/Unorganized/Economic/' + folder + '/' + filename + '.json'
            self.data.to_json(filename, orient = 'records')
