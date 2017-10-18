# -*- coding: utf-8 -*-
"""
Created on Wed Oct 18 03:13:58 2017

@author: Andrea
"""

#Loading the relevant libraries
import pandas as pd
import numpy as np
import sklearn
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn import preprocessing
from sklearn import linear_model
from sklearn import model_selection
from sklearn.model_selection import KFold

def reading_csv(filename):
    """This function reads a csv file a returns
    a data matri and a vector labels.
    We are assuming the labels are in the last position."""
    data = pd.read_csv(filename)
    last_column_index= data.shape[1] - 1 #0-based numeration
    X= data.iloc[:,0:last_column_index]
    y= data.iloc[:,last_column_index:]
    return X, y

def split_training(Data_Matrix, Label_Vector, Train_Size, Seed):
    """This function takes as an input the Data Matrix and the
    Label Vector we are working with, shuffles the data according
    to a Seed given as an input and splits according to the proportion
    decided by the user.
    It returns four elements: the training and test Data Matrix,
    the training and testing Label Vectors"""
    X_train, X_test, y_train, y_test= train_test_split(Data_Matrix, Label_Vector,
                                                       train_size= Train_Size,
                                                       random_state= Seed,
                                                       shuffle= True,
                                                       stratify= Label_Vector)
    return X_train, X_test, y_train, y_test

def normalise(X_train, X_test):
    """This function performs a normalisation by subtracting the mean
    and then dividing by the standard deviation.
    It computes the mean value and standard deviation only on the training
    matrix and apply the same transformation to both matrices."""
    # Create a standard processor object
    scaler= StandardScaler()
    # Create an object to transform the data to fit standard processor
    x_scaled= scaler.fit_transform(X_train)
    # Run the normalizer on the dataframes
    X_train = pd.DataFrame(x_scaled)
    X_test= pd.DataFrame(scaler.transform(X_test))
    return X_train, X_test

def rename_columns(X_train, X_test, y_train, y_test, Column_Names, Label_Name):
    """This function changes the name of the columns of training and
    data set and of the label vectors, using the same for the two.
    It assumes that Column_Names and Label_Name are tuple of strings of the
    right dimensions."""
    X_train.columns= Column_Names
    y_train.columns= Label_Name
    X_test.columns= Column_Names
    y_test.columns= Label_Name
    return X_train, X_test, y_train, y_test

def display_data(Data_Matrix, Label_Vector):
    """This function allows to visualise the data and print
    some information"""
    print("Printing the first ten rows...")
    print(Data_Matrix.head(10)) #printing the first ten rows
    print("\nPrinting summary statistics...")
    print(Data_Matrix.describe()) #Getting some information
    print("\nPrinting scatterplots considering the class")
    pd.plotting.scatter_matrix(Data_Matrix, alpha=0.8, figsize=(6, 6),
                               diagonal='kde', c= Label_Vector)


def preprocess_data(filename, Train_Size, Seed, Column_Names, Label_Name=['Class']):
    """Encapsulating all the work done insofar.
        Taking as input the filename, the relative
        size of the training set, the seed for the
        random reshuffling and the names we are willing to give to the columns"""
    X, y= reading_csv(filename)
    X_train, X_test, y_train, y_test= split_training(X, y, Train_Size, Seed)
    X_train, X_test= normalise(X_train, X_test)
    X_train, X_test, y_train, y_test= rename_columns(X_train, X_test, y_train, y_test, Column_Names, Label_Name)
    print("Display information for the training set.")
    display_data(X_train, y_train)
    return X_train, X_test, y_train, y_test

filename= 'TP1-data.csv'
Train_Size= 0.66
Seed= 10182017
Column_Names= ['Variance', 'Skewness', 'Curtosis', 'Entropy']
X_train, X_test, y_train, y_test= preprocess_data(filename, Train_Size, Seed, Column_Names)
   

# TODO: make this a function 
CV_data= []
for i in range(0,80):
    inverse_penalisation= pow(2,i)/100000
    logistic = linear_model.LogisticRegression(penalty='l2', C= inverse_penalisation)
    logistic.fit(X_train, y_train.values.ravel())
    cv_eval = model_selection.cross_val_score(logistic, X_train, y_train.values.ravel(), cv=KFold(n_splits=5,random_state=52222,shuffle=True))
    CV_data.append([inverse_penalisation, np.mean(cv_eval), np.std(cv_eval)])

CV_data= pd.DataFrame(CV_data)
CV_data.columns= ["InvPenalisation", "CVMean", "CVStd"]

