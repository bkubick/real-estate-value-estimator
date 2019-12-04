#Basic Libraries
import numpy as np
import pandas as pd

#Classification
from sklearn.svm import SVC
from sklearn.linear_model import LogisticRegression
from sklearn.tree import DecisionTreeClassifier
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB

#Performance Metrics
from sklearn import metrics

class Classification_Models:
    def __init__(self, X_train = None, y_train = None,
                       X_test = None, y_test = None):

        self.X_train = X_train
        self.y_train = y_train
        self.X_test = X_test
        self.y_test = y_test

        self.lr_pred = None
        self.lr_confusion = None

        self.dt_pred = None
        self.dt_confusion = None

        self.rfc_pred = None
        self.rfc_confusion = None

        self.nn_pred = None
        self.nn_acc = None

        self.svm_pred = None
        self.svm_confusion = None

        self.nb_pred = None
        self.nb_confusion = None

        self.knc_pred = None
        self.knc_confusion = None

        #This is declared to encode y_values
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

    def logistic_regression(self):
        if self.empty:
            return

        #Linear Regression Object to fit training set
        lr = LogisticRegression()
        lr.fit(self.X_train, self.y_train)
        self.lr_pred = lr.predict(self.X_test)
        self.__lr_test = True

        if np.any(self.y_test != None):
            self.lr_confusion = metrics.confusion_matrix(self.y_test, self.lr_pred)
        else:
            print('No y test data')

    #Done
    def decision_tree_classification(self):
        if self.empty:
            return

        #Decision Tree object fitting to practice training set
        dt = DecisionTreeClassifier()
        dt.fit(self.X_train, self.y_train)
        self.dt_pred = dt.predict(self.X_test)
        self.__dt_test = True

        if np.any(self.y_test != None):
            self.dt_confusion = metrics.confusion_matrix(self.y_test, self.dt_pred)
        else:
            print('No y test data')

    #Done
    def random_forest_classification(self, md = 20, n = 500):
        if self.empty:
            return

        #Decision Tree object fitting to practice training set
        rfc = RandomForestClassifier(max_depth = md, n_estimators = n)
        rfc.fit(self.X_train, self.y_train.values.ravel())
        self.rfc_pred = rfc.predict(self.X_test)
        self.__rfc_test = True

        if np.any(self.y_test != None):
            self.rfc_confusion = metrics.confusion_matrix(self.y_test, self.rfc_pred)
        else:
            print('No y test data')

    #Need to add
    def neural_network_classification(self, hidden_layers = 1):
        if self.empty:
            return

        self.__nn_test = True
        #PyTorch
        return

    def k_nearest_neighbors_classification(self, k_neighbors = 3):
        if self.empty:
            return

        knc = KNeighborsClassifier(n_neighbors = k_neighbors)
        knc.fit(self.X_train, self.y_train)
        self.knc_pred = knc.predict(self.X_test)
        self.__knc_test = True

        if np.any(self.y_test != None):
            self.knc_confusion = metrics.confusion_matrix(self.y_test, self.knc_pred)
        else:
            print('No y test data')

    def svm_classification(self, kernel = 'linear'):
        if self.empty:
            return

        svm = SVC(kernel = kernel)
        svm.fit(self.X_train, self.y_train)
        self.svm_pred = svm.predict(self.X_test)
        self.__svm_test = True

        if np.any(self.y_test != None):
            self.svm_confusion = metrics.confusion_matrix(self.y_test, self.svm_pred)
        else:
            print('No y test data')

    def naive_bayes_classification(self):
        if self.empty:
            return

        nb = GaussianNB()
        nb.fit(self.X_train, self.y_train)
        self.nb_pred = nb.predict(self.X_test)
        self.__nb_test = True

        if np.any(self.y_test != None):
            self.nb_confusion = metrics.confusion_matrix(self.y_test, self.nb_pred)
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
        self.lr_confusion = None

        self.dt_pred = None
        self.dt_confusion = None

        self.rfc_pred = None
        self.rfc_confusion = None

        self.nn_pred = None
        self.nn_acc = None

        self.svm_pred = None
        self.svm_confusion = None

        self.nb_pred = None
        self.nb_confusion = None

        self.empty = self.__is_empty()
