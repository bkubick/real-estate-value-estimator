#Basic Libraries
import numpy as np
import pandas as pd

#Regression
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.tree import DecisionTreeRegressor
from sklearn.ensemble import RandomForestRegressor
from sklearn.neighbors import KNeighborsRegressor

#Performance Metrics
from sklearn import metrics

class Regression_Models:
    def __init__(self, X_train = None, y_train = None,
                       X_test = None, y_test = None):

        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

        self.lr_pred = None
        self.lr_acc = None

        self.pl_pred = None
        self.pl_acc = None

        self.dt_pred = None
        self.dt_acc = None

        self.rfr_pred = None
        self.rfr_acc = None

        self.nn_pred = None
        self.nn_acc = None

        self.knr_pred = None
        self.knr_acc = None
        self.empty = self.__is_empty()

    #Done
    def set_training_data(self, X_train, y_train):
        self.X_train = X_train
        self.y_train = y_train

        self.empty = self.__is_empty()

    def set_test_data(self, X_test, y_test):
        self.X_test = X_test
        self.y_test = y_test

        self.empty = self.__is_empty()

    def set_data(self, X_train, y_train, X_test, y_test):
        self.set_training_data()
        self.set_test_data()

        self.empty = self.__is_empty()

    def linear_regression(self):
        if self.empty:
            return

        #Linear Regression Object to fit training set
        lr = LinearRegression()
        lr.fit(self.X_train, self.y_train)
        self.lr_pred = lr.predict(self.X_test)
        self.__lr_test = True

        if np.any(self.y_test != None):
            self.lr_acc = metrics.r2_score(self.y_test, self.lr_pred)
        else:
            print('No y test data')

    #Done: Need to check
    def polynomial_regression(self, degree = 2):
        if self.empty:
            return

        #Linear Regression Object to fit testing set
        pr = PolynomialFeatures(degree = degree)
        X_train_ = pr.fit_transform(self.X_train)
        X_test_ = pr.fit_transform(self.X_test)
        lr = LinearRegression()
        lr.fit(X_train_, self.y_train)
        self.pl_pred = lr.predict(X_test_)
        self.__pl_test = True

        if np.any(self.y_test != None):
            self.pl_acc = metrics.r2_score(self.y_test, self.pl_pred)
        else:
            print('No y test data')

    #Done
    def decision_tree_regression(self):
        if self.empty:
            return

        #Decision Tree object fitting to practice training set
        dt = DecisionTreeRegressor()
        dt.fit(self.X_train, self.y_train)
        self.dt_pred = dt.predict(self.X_test)
        self.__dt_test = True

        if np.any(self.y_test != None):
            self.dt_acc = metrics.r2_score(self.y_test, self.dt_pred)
        else:
            print('No y test data')

    #Done
    def random_forest_regression(self, md = 20, n = 500):
        if self.empty:
            return

        #Decision Tree object fitting to practice training set
        rfr = RandomForestRegressor(max_depth = md, n_estimators = n)
        rfr.fit(self.X_train, self.y_train.values.ravel())
        self.rfr_pred = rfr.predict(self.X_test)
        self.__rfr_test = True

        if np.any(self.y_test != None):
            self.rfr_acc = metrics.r2_score(self.y_test, self.rfr_pred)
        else:
            print('No y test data')

    #Need to add
    def neural_network_regression(self, hidden_layers = 1):
        if self.empty:
            return
        self.__nn_test = True
        #PyTorch
        return

    def k_nearest_neighbors_regression(self, k_neighbors = 3):
        if self.empty:
            return

        knr = KNeighborsRegressor(n_neighbors = k_neighbors)
        knr.fit(self.X_train, self.y_train)
        self.knr_pred = knr.predict(self.X_test)
        self.__knr_test = True

        if np.any(self.y_test != None):
            self.knr_acc = metrics.r2_score(self.y_test, self.knr_pred)
        else:
            print('No y test data')

    #Done
    def __is_empty(self):
        if np.any(self.X_train == None):
            print('No X_train data')
            return True
        elif np.any(self.y_train == None):
            print('No y_train data')
            return True
        elif np.any(self.X_test == None):
            print('No X_test data')
            return True
        else:
            return False

    def reset_data(self,X_train = None, y_train = None,
                       X_test = None, y_test = None):

        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test
        self.lr_pred = None
        self.lr_acc = None
        self.pl_pred = None
        self.pl_acc = None
        self.dt_pred = None
        self.dt_acc = None
        self.rfr_pred = None
        self.rfr_acc = None
        self.nn_pred = None
        self.nn_acc = None
        self.empty = self.__is_empty()
