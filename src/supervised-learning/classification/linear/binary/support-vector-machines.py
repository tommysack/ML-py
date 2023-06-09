import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from sklearn.svm import LinearSVC
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import accuracy_score

#Load data
breast_cancer = load_breast_cancer()

#General info
print(breast_cancer.DESCR)
breast_cancer_df = pd.DataFrame(breast_cancer.data, columns=breast_cancer.feature_names)
breast_cancer_df['diagnosis'] = breast_cancer.target 
breast_cancer_df.head()
breast_cancer_df.describe() 
breast_cancer_df.shape #32 columns, 569 rows
breast_cancer_df['diagnosis'].unique() #array([0, 1]) => binary classification
sns.countplot(data=breast_cancer_df, x='diagnosis') #Ok, the classes are quite distributed
breast_cancer_df.isnull().sum() 
np.isnan(breast_cancer_df.drop('diagnosis',axis=1)).any() #Many algorithms do work only with numerical data

#Correlation between features and class diagnosis (we assume moderate correlation from 0.5)
breast_cancer_df.corr()['diagnosis'].sort_values() #There are many features mildly correlated with target

#Draw correlation between numerical worst concave points, worst perimeter and class diagnosis
sns.scatterplot(x=breast_cancer_df['worst concave points'], y=breast_cancer_df['worst perimeter'], hue=breast_cancer_df['diagnosis'], palette='viridis')
plt.title("Correlation between worst concave points, worst perimeter and diagnosis")
plt.xlabel("worst concave points")
plt.ylabel("worst perimeter")
plt.show()

'''
As you can see as worst concave points and worst perimeter increase, then diagnosis goes towards the value 0.
I would try with Linear SVC and all features.
'''

'''
The data are points in an hyperspace H of 32 dimensions.
The goal is to assign a class label Y (binary classification with values "M" or "B") to input X.
Technically you need to find the "best" hyperplane of 31 dimensions which best separates the points classified in H.
The "best": in this case we use LinearSVC (linear support vector classification) to minimize loss function.
Behind the scenes it working finds hyperplane that maximise the width between the two categories. 
It make a linear (but can perform non-linear using kernel) binary (but is possible multi-class one vs all) non-probabilistic 
classifier. 
'''

#Separates data in numpy.ndarray columns data/target 
X = breast_cancer.data
Y = breast_cancer.target

#Separates data in rows train/test
X_train, X_test, Y_train, Y_test = train_test_split(X,Y, test_size=0.1, random_state=0)

#Check if X needs to scaling
print("\nBEFORE scaling")
print("X train min", np.amin(X_train))
print("X test min", np.amin(X_test))
print("X train max", np.amax(X_train))
print("X test max", np.amax(X_test))

#Standardize features (preferred vs. MinMaxScaler, the features upper/lower boundaries aren't known)
standard_scaler = StandardScaler()
X_train = standard_scaler.fit_transform(X_train)
X_test = standard_scaler.transform(X_test)

#X after scaling
print("\nAFTER scaling")
print("X train min", np.amin(X_train))
print("X test min", np.amin(X_test))
print("X train max", np.amax(X_train))
print("X test max", np.amax(X_test))

svc = LinearSVC(
  penalty='l2', #L2 regularization to avoid overfitting  
  C=0.01, #inverse of regularization strength (C lower => Higher regularization)
  verbose=True
)
svc.fit(X_train, Y_train) 

Y_train_predicted = svc.predict(X_train) 

#Model overfitting evaluation 
print("\nModel overfitting evaluation")
print("ACCURACY SCORE: ", accuracy_score(Y_train, Y_train_predicted)) 

Y_test_predicted = svc.predict(X_test) 

#Model evaluation 
print("\nModel evaluation")
print("ACCURACY SCORE: ", accuracy_score(Y_test, Y_test_predicted)) 

'''
The model would appear to be appropriate for this problem.
'''


