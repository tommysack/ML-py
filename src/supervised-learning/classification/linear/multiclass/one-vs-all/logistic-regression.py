import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.datasets import load_digits
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.linear_model import LogisticRegression
from sklearn.metrics import accuracy_score, log_loss

#Load data
digits = load_digits()

#General info
print(digits.DESCR) #Images 8x8 64 columns of pixels (every pixel has a value 0..16), and 1 column with the value integer rapresented
digits_df = pd.DataFrame(digits.data)
digits_df['target'] = digits.target
digits_df['target'].unique() #array([0, 1, 2, 3, 4, 5, 6, 7, 8, 9]) => multi-class classification
digits_df.head()
digits_df.describe() 
digits_df.shape #65 columns, 1797 rows
sns.countplot(data=digits_df, x='target') #Ok, the classes are quite distributed
digits_df.isnull().sum() 
np.isnan(digits_df).any() #Many algorithms do work only with numerical data

'''
The data are points in an hyperspace H of 65 dimensions.
The goal is to assign a class label Y (classification with values 0..9) to input X.
The one vs all approach consists in to split a multi-classification problem into multiple binary classifier method (building one model for every single class, 
predicting a new case over every model and taking the model with higher probability).
In this case we use LogisticRegression that uses "solver" to maximize Likelihood.
'''

#Separates data in Dataframe/Series columns data/target 
X = digits.data 
Y = digits.target 

#Separates data in rows train/test
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.1, random_state=0)

#Check if X needs to scaling (makes it easy for a model to learn and understand the problem)
print("\nBEFORE scaling")
print("X train min", np.amin(X_train))
print("X test min", np.amin(X_test))
print("X train max", np.amax(X_train))
print("X test max", np.amax(X_test))

#Normalize features (preferred vs. StandardScaler, the features upper/lower boundaries are known)
min_max_scaler = MinMaxScaler()
X_train = min_max_scaler.fit_transform(X_train)
X_test = min_max_scaler.transform(X_test)

#X after scaling
print("\nAFTER scaling")
print("X train min", np.amin(X_train))
print("X test min", np.amin(X_test))
print("X train max", np.amax(X_train))
print("X test max", np.amax(X_test))

logistic_regression = LogisticRegression(
  penalty='l2', #L2 regularization to avoid overfitting 
  C=0.1, #inverse of regularization strength (C lower => Higher regularization)
  solver='lbfgs', #algorithm to use
  verbose=True
) 
logistic_regression.fit(X_train, Y_train) 

Y_train_predicted = logistic_regression.predict(X_train) 
Y_train_predicted_proba = logistic_regression.predict_proba(X_train) 

#Model overfitting evaluation 
print("\nModel overfitting evaluation")
print("ACCURACY SCORE: ", accuracy_score(Y_train, Y_train_predicted)) 
print("LOG LOSS: ", log_loss(Y_train, Y_train_predicted_proba)) 

Y_test_predicted = logistic_regression.predict(X_test) 
Y_test_predicted_proba = logistic_regression.predict_proba(X_test) 

#Model evaluation 
print("\nModel evaluation")
print("ACCURACY SCORE: ", accuracy_score(Y_test, Y_test_predicted)) 
print("LOG LOSS: ", log_loss(Y_test, Y_test_predicted_proba)) 

'''
The model would appear to be appropriate for this problem.
'''

