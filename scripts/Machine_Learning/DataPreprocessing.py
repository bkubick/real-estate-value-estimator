import Constants
import pandas as pd
import numpy as np
from Machine_Learning.CombineData import Combine_Data
from sklearn.preprocessing import StandardScaler
from sklearn.impute import SimpleImputer

class Data_Preprocessing:
    def __init__(self, city = 'all'):
        #Need to write all the code it is going to do in this for simplifying
        cd = Combine_Data(city = city)
        self.__all_data = cd.all_data
        #Initializing all Data and
        self.cleaned_data = self.__all_data

        '''Below are the training and test sets and should be created last'''
        #Reression training and test sets
        self.X_reg_train_set = None
        self.X_reg_test_set = None
        self.y_reg_train_set = None
        self.y_reg_test_set = None
        #Classification training and test sets
        self.X_class_train_set = None
        self.X_class_test_set = None
        self.y_class_train_set = None
        self.y_class_test_set = None

    def standard_preprocess(self, econ = True):
        #1: Dropping Non-important columns (DONE)
        self.drop_columns()

        #2: Finding columns that are missing more than the percent threshold
        self.remove_missing_data_columns()

        #3: Creating Age column (Need to adjust)
        if 'year_built' in list(self.cleaned_data):
            self.date_year_subtraction()
        else:
            self.drop_columns(['date'])

        #4: Filling in all the missing data (DONE)
        self.missing_data()

        if econ:
            #5: Normalize economic DATA (DONE)
            self.columns_divided()

    def original_preprocess(self, econ = True):
        #Steps to filtering this data
        #Steps 1-5
        self.standard_preprocess(econ = econ)

        #6: Encode strings
        self.encode_values()

        #7: Creating the training and test sets
        self.set_training_and_test_set_by_event()
        
        #8: Normalize Values
        self.normalize_values()

    def housing_features_only_preprocess(self, original = True):
        #1. Drop Econ Data
        self.drop_columns(columns = list(Constants.ECON_DATA))

        #2. Preprocess
        if original:
            self.original_preprocess(econ = False)
        else:
            self.standard_preprocess(econ = False)


    #Done
    def drop_columns(self, columns = list(Constants.COLUMNS_TO_DROP)):
        columns_dropping = list(columns)
        columns_dropping = list(self.__check_columns_in_list(columns_dropping))
        
        if np.any(columns_dropping == None):
            return
        elif len(columns_dropping) == 0:
            print('Already dropped all columns listed')
            return

        self.cleaned_data = self.cleaned_data.drop(columns = columns_dropping)

    def drop_categorical_columns(self):
        columns = list(self.cleaned_data)
        string_columns = []
        for column in columns:
            if type(self.cleaned_data.iloc[0][column]) == str and column != 'event':
                string_columns.append(column)

        self.drop_columns(string_columns)

    #Done
    def normalize_values(self):
        sc = StandardScaler()
        self.X_reg_train_set = sc.fit_transform(self.X_reg_train_set)
        self.X_reg_test_set = sc.transform(self.X_reg_test_set)

        sc = StandardScaler()
        self.X_class_train_set = sc.fit_transform(self.X_class_train_set)
        self.X_class_test_set = sc.transform(self.X_class_test_set)

    def columns_divided(self, column_numerators = list(Constants.COLUMNS_TO_DIVIDE),
                              column_denominator = list(Constants.COLUMNS_TO_DIVIDE_BY),
                              new_columns = list(Constants.COLUMNS_TO_ADD)):

        column_numerators = self.__check_columns_in_list(column_numerators)
        column_denominator = self.__check_columns_in_list(column_denominator)
        if len(column_numerators) == 0:
            print('Columns in numerator already dropped')
            return
        elif len(column_denominator) == 0:
            print('Column in denominator already dropped')
            return
        elif self.__check_if_column_exists(new_columns):
            return

        for new, col in zip(new_columns, column_numerators):
            self.cleaned_data[new] = self.cleaned_data[col].div(self.cleaned_data[column_denominator[0]],
                                                                axis = 'index')

        self.cleaned_data = self.cleaned_data.drop(columns = column_numerators)
        self.cleaned_data = self.cleaned_data.drop(columns = column_denominator)

    def date_year_subtraction(self, column_1 = 'year_built', column_2 = 'date', new_column = 'age'):
        self.cleaned_data[new_column] = self.cleaned_data[column_2].dt.year - self.cleaned_data[column_1]
        self.cleaned_data[new_column] = self.cleaned_data[new_column].abs()
        self.cleaned_data = self.cleaned_data.drop(columns = [column_1, column_2])

    def subtract_data(self, column_1, column_2, new_column, absolute_value = False):
        columns = self.__check_columns_in_list([columns_1, columns_2])
        if len(columns) < 2:
            print('One of the columns listed doesnt exist')
            return

        self.cleaned_data[new_column] = self.cleaned_data[columns[1]] - self.cleaned_data[columns[0]]
        if absolute_value:
            self.cleaned_data[new_column] = self.cleaned_data[new_column].abs()

        self.cleaned_data = self.cleaned_data.drop(columns = columns)

    #Creates seperate columns for each variable in a column
    def encode_values(self, columns = list(Constants.COLUMNS_TO_ENCODE)):
        columns = self.__check_columns_in_list(columns)
        
        for column in columns:
            one_hot_encoder = pd.get_dummies(self.cleaned_data[column])
            self.cleaned_data = self.cleaned_data.drop(column, axis=1)
            self.cleaned_data = self.cleaned_data.join(one_hot_encoder)


    #Done
    def remove_missing_data_columns(self, percent = Constants.MISSING_DATA_THRESHOLD):
        num_rows = len(self.cleaned_data)

        for column in self.cleaned_data:
            missing_data = np.where(self.cleaned_data[column].isna())
            if float(len(missing_data[0])/num_rows) > percent:
                self.cleaned_data = self.cleaned_data.drop(column, axis = 1)

    #Done: strat = 'constant', 'mean', 'median', 'most_frequent'
    #('constant' enters 'missing_value' for strings and 0 for numbers
    def missing_data(self, floats = 'average', ints = '0'):
        for column in list(self.cleaned_data):
            if type(self.cleaned_data.iloc[0][column]) is np.int64:
                if ints == '0':
                    self.cleaned_data[column] = self.cleaned_data[column].fillna(0, axis = 0)
                elif ints == 'average':
                    self.cleaned_data[column] = self.cleaned_data[column].fillna(self.cleaned_data[column].mean(), axis = 0)
                else: #Might change this later
                    self.cleaned_data[column] = self.cleaned_data[column].fillna(0, axis = 0)
            elif type(self.cleaned_data.iloc[0][column]) is np.float64:
                if floats == 'average':
                    self.cleaned_data[column] = self.cleaned_data[column].fillna(self.cleaned_data[column].mean(), axis = 0)
                elif floats == '0':
                    self.cleaned_data[column] = self.cleaned_data[column].fillna(0, axis = 0)
                else: #Might change this later
                    self.cleaned_data[column] = self.cleaned_data[column].fillna(0, axis = 0)
            elif type(self.cleaned_data.iloc[0][column]) is str:
                self.cleaned_data[column] = self.cleaned_data[column].replace(np.NaN, column + ' missing')

    #This is the second to last step in any preprocessing
    def set_training_and_test_set_by_event(self):
        if 'event' not in list(self.cleaned_data):
            print('No events column')
            return

        self.X_reg_headers = list(self.cleaned_data)
        self.X_reg_headers.remove('price')
        self.X_reg_headers.remove('event')
        self.y_reg_header = ['price']

        self.X_class_headers = list(self.cleaned_data)
        self.X_class_headers.remove('event')
        self.y_class_header = ['event']


        #Sorting in order of event type
        self.cleaned_data = self.cleaned_data.sort_values(['event'])

        decrease_start_index = 0
        sale_end_index = len(self.cleaned_data)-1

        for i in range(1, len(self.cleaned_data)):
            if self.cleaned_data.iloc[i]['event'] == 'increase' and self.cleaned_data.iloc[i-1]['event'] =='decrease':
                decrease_end_index = i-1
                increase_start_index = i
            elif self.cleaned_data.iloc[i]['event'] == 'listed' and self.cleaned_data.iloc[i-1]['event'] =='increase':
                increase_end_index = i-1
                listed_start_index = i
            elif self.cleaned_data.iloc[i]['event'] == 'sale' and self.cleaned_data.iloc[i-1]['event'] =='listed':
                listed_end_index = i-1
                sale_start_index = i

        self.X_reg_train_set = self.cleaned_data.iloc[sale_start_index:sale_end_index][self.X_reg_headers]
        self.y_reg_train_set = self.cleaned_data.iloc[sale_start_index:sale_end_index][self.y_reg_header]
        self.X_reg_test_set = self.cleaned_data.iloc[listed_start_index:listed_end_index][self.X_reg_headers]
        self.y_reg_test_set = self.cleaned_data.iloc[listed_start_index:listed_end_index][self.y_reg_header]

        self.X_class_train_set = pd.concat([self.cleaned_data.iloc[decrease_start_index:increase_end_index][self.X_class_headers],
                                       self.cleaned_data.iloc[sale_start_index:sale_end_index][self.X_class_headers]])
        self.y_class_train_set = pd.concat([self.cleaned_data.iloc[decrease_start_index:increase_end_index][self.y_class_header],
                                       self.cleaned_data.iloc[sale_start_index:sale_end_index][self.y_class_header]])
        self.X_class_test_set = self.cleaned_data.iloc[listed_start_index:listed_end_index][self.X_class_headers]

        #Note: this data doesnt have an answer so the model cant be tested
        #self.y_class_test_set = self.cleaned_data.iloc[listed_start_index:listed_end_index][self.y_class_header]


    def __check_columns_in_list(self, columns):
        if np.any(columns == None):
            print('None column')
            return None
        new_columns = list(columns)
        missing_columns = []
        
        for column in list(new_columns):
            if column not in list(self.cleaned_data):
                missing_columns.append(column)
                
        for i in range(0,len(missing_columns)):
            new_columns.remove(missing_columns[i])

        return new_columns

    def __check_if_column_exists(self, columns):
        for column in columns:
            if column in list(self.cleaned_data):
                print('Duplicate Column: ' + column)
                return True


    def reset_data(self):
        self.cleaned_data = self.__all_data
        #Reression training and test sets
        self.X_reg_train_set = None
        self.X_reg_test_set = None
        self.y_reg_train_set = None
        self.y_reg_test_set = None
        #Classification training and test sets
        self.X_class_train_set = None
        self.X_class_test_set = None
        self.y_class_train_set = None
        self.y_class_test_set = None
