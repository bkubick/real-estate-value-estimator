#Basic Libraries
import numpy as np
import pandas as pd

#Plotting Libraries
import matplotlib.pyplot as plt

#Performance Metrics
from sklearn import metrics
from sklearn.model_selection import cross_val_score

class Data_Analysis:
    def __init__(self, X = None, y = None):
        self.X = X #Pandas Dataframe Matrix
        self.y = y #Pandas Datafame Vector
        self.data = None
        self.correlation_matrix = None
        self.correlation_vector = None
        self.independent_statistics = None
        self.dependent_statistics = None
        self.all_statistics = None
        self.small_correlations = None
        self.set_all()

    #Done
    def set_X(self, X):
        self.X = X

    #Done
    def set_y(self, y):
        self.y = y

    #Done
    def set_all(self):
        if self.__is_empty():
            return

        self.data = pd.concat([self.X, self.y], axis=1)

    #Done #Pick data: all, independent, dependent
    def set_summary_statistics(self, data = 'all'):
        #Checking X values
        if self.__X_is_empty():
            return None

        if data == 'independent':
            self.independent_statistics = self.X.describe()

        #Checking y values
        if self.__y_is_empty():
            return None
        elif data == 'dependent':
            self.dependent_statistics = self.y.describe()
        else:
            self.all_statistics = self.data.describe()


    #Done
    def set_correlation_matrix(self, absolute = True):
        if self.__is_empty():
            return

        #Correlation Matrix
        if absolute:
            self.correlation_matrix = self.data.corr().abs()
        else:
            self.correlation_matrix = self.data.corr()

    def set_correlation_vector(self, absolute = True):
        if self.__is_empty():
            return

        self.set_correlation_matrix(absolute = absolute)

        #Correlation Vector
        self.correlation_vector = self.correlation_matrix.iloc[:-1,-1]

    #Done
    def min_correlation(self, min_correlation = 0.25):
        if np.any(self.correlation_matrix == None):
            self.set_correlation_vector()

        self.small_correlations = []
        for correlation, column in zip(self.correlation_vector, self.correlation_matrix):
            if abs(correlation) < min_correlation:
                self.small_correlations.append(column)

    #Done: Need to test
    def normal_distribution_plots(self):
        if self.__is_empty():
            return

        headings = list(self.X)
        plot_columns = 3
        plot_rows = len(headings)/plot_columns
        if len(headings)%plot_columns > 0:
            plot_rows += 1

        #Creating distribution plots below
        fig, axs = plt.subplots(plot_columns, plot_rows, figsize=(20,15))
        k = 0
        for i in range(0,plot_columns):
            for j in range(0,plot_rows):
                axs[i, j].hist(train[headings[k]], bins=50)
                axs[i, j].set_xlabel(headings[k])
                k = k + 1

    #Done
    def __X_is_empty(self):
        if np.any(self.X == None):
            print('No dependent variables selected')
            return True

    #Done
    def __y_is_empty(self):
        if np.any(self.y == None):
            print('No independent variable selected')
            return True

    #Done
    def __is_empty(self):
        if self.__X_is_empty() and self.__y_is_empty():
            return True
