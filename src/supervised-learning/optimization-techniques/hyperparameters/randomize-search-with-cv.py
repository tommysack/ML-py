import pandas as pd
import numpy as np
import seaborn as sns
from sklearn.datasets import load_digits
from sklearn.model_selection import RandomizedSearchCV, train_test_split
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVC

'''
Randomize Search performes hyperparameter tuning to determine the optimal values, and uses cross validation method.
It randomly sampling different combinations of hyperparameter from predefined ranges or distributions.

PROS: efficiency and scalability.
CONS: while it explores the space it may not allocate enough resources to exploit regions that show good performance.
'''

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
digits_df.isnull().sum() 
sns.countplot(data=digits_df, x='target') #Ok, the classes are quite distributed
np.isnan(digits_df).any() #Many algorithms do work only with numerical data

'''
The data are points in an hyperspace H of 65 dimensions.
The goal is to assign a class label Y (classification with values 0..9) to input X.
In this case we use SVC.
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

svc = SVC() #Support Vector Machine (search estimator: must implement the scikit estimator interface)
param_grid = { #Hyperparameter to tuning
  "C": [1, 10, 100, 1000],
  "kernel": ["linear", "rbf", "sigmoid", "poly"],  
  "gamma": [0.1, 1, "auto"],
  "decision_function_shape": ["ovo", "ovr"]
}
randomized_search_cv = RandomizedSearchCV(
  estimator=svc, 
  param_distributions=param_grid, #dictionary with parameters names
  cv=10 #num of folds in a KFold
)
randomized_search_cv.fit(X_train, Y_train)

#print(randomized_search_cv.best_params_)
#Output:
#{'kernel': 'poly',
# 'gamma': 'auto',
# 'decision_function_shape': 'ovr',
# 'C': 1000}

svc = randomized_search_cv.best_estimator_

#Model evaluation 
print("\nModel overfitting evaluation")
print("ACCURACY SCORE: ", svc.score(X_train, Y_train)) 

#Model evaluation
print("\nModel evaluation")
print("ACCURACY SCORE: ", svc.score(X_test, Y_test)) 

'''
The model would appear to be appropriate for this problem.
'''