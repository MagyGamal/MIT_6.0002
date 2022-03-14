# -*- coding: utf-8 -*-
"""
Created on Fri Jan 10 17:14:55 2020

@author: Magy Gamal
"""
import numpy as np
from sklearn import datasets ,linear_model
from sklearn.metrics import mean_squared_error, r2_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.cross_validation import train_test_split
from sklearn.metrics import confusion_matrix, accuracy_score, roc_curve
from sklearn.linear_model import LogisticRegression
from sklearn.neighbors import KNeighborsClassifier
diabetes_X, diabetes_y = datasets.load_diabetes(return_X_y=True)
# Split the data into training/testing sets
diabetes_X_train = diabetes_X[:-20]
diabetes_X_test = diabetes_X[-20:]
# Split the targets into training/testing sets
diabetes_y_train = diabetes_y[:-20]
diabetes_y_test = diabetes_y[-20:]
#Create linear regression object
regr = linear_model.LinearRegression()
# Train the model using the training sets
regr.fit(diabetes_X_train, diabetes_y_train)
# Make predictions using the testing set
diabetes_y_pred = regr.predict(diabetes_X_test)
print('Mean squared error: %.2f', mean_squared_error(diabetes_y_test, diabetes_y_pred))
print('Coefficient of determination: %.2f',r2_score(diabetes_y_test, diabetes_y_pred))

iris=datasets.load_iris()
X = iris.data
y = iris.target
clf_0= RandomForestClassifier()
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.70, random_state=5)
 # 70% training and 30% test
clf_0.fit(X_train, y_train)
random_forest_y_pred=clf_0.predict(X_test)
#print(roc_curve(y_test,random_forest_y_pred))
print("Confusion matrix of random forrest ",confusion_matrix(y_test,random_forest_y_pred))

clf_1= LogisticRegression(random_state=0).fit(X, y)
logistic_regression_y_pred=clf_1.predict(X_test)
print("Confusion Matrix of logistic regression",confusion_matrix(y_test,logistic_regression_y_pred))

neigh = KNeighborsClassifier(n_neighbors=3)
neigh.fit(X, y)
KNN_y_pred=neigh.predict(X_test)
print("Condusion matrix of KNN",confusion_matrix(y_test,KNN_y_pred))
