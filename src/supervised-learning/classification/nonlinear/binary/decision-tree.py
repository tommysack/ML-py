import pandas as pd
import seaborn as sns
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score
from sklearn.tree import DecisionTreeClassifier

#Load data
passengers_df = pd.read_csv("https://web.stanford.edu/class/archive/cs/cs109/cs109.1166/stuff/titanic.csv")

#General info
passengers_df.head()
passengers_df.describe() 
passengers_df.shape #8 columns, 887 rows
passengers_df['Survived'].unique() #array([0, 1]) => binary classification (Not Survived, Survived)
sns.countplot(data=passengers_df, x='Survived') #The 1 class are many more than 0 class
passengers_df.isnull().sum() 

#Correlation between features and class Survived (we assume moderate correlation from 0.5)
passengers_df= passengers_df.drop("Name",axis=1) #Drop column Name that is clearly irrelevant
mapping_sex = {'male': 0, 'female': 1}
passengers_df['Sex'] = passengers_df['Sex'].map(mapping_sex)
passengers_df.corr()['Survived'].sort_values() #There may be a correlation with Sex, Pclass and Age

#Draw correlation between classes Sex, Pclass, Age and class Survived
sns.barplot(data=passengers_df, x='Sex', y='Survived') #The female(1) have survival average more than male(0)
sns.barplot(data=passengers_df, x='Pclass', y='Survived') #The Pclass(3) flu the survival average 
def map_age(age): 
  return round(age / 10)
passengers_df['Age_block'] = passengers_df['Age'].apply(lambda age: map_age(age))
sns.barplot(data=passengers_df, x='Age_block', y='Survived')
sns.barplot(data=passengers_df, x='Age_block', y='Survived', hue='Sex') #The Age flu the survival average

'''
I would try with Decision Tree Classifier and the features Age, Pclass and Sex.
'''

'''
The data are points in an hyperspace H of 8 dimensions.
The goal is to assign a class label Y (binary classification with values 0 or 1) to input X.
In this case we use DecisionTreeClassifier that illustrate all possible outcomes of a decision
(In training it chooses the partition maximizing the purity of the points labeled contained in the split nodes). 
It make a non-linear binary (but is possible multi-class) non-probabilistic classifier. 
'''

#Separates data in numpy.ndarray columns data/target 
X = passengers_df[["Pclass", "Age", "Sex"]].values
Y = passengers_df["Survived"].values

X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=0)

#Decision trees are not sensitive to feature scaling

decision_tree_classifier = DecisionTreeClassifier(
  criterion="gini", #to measure the quality of a split
  max_depth=6 
)
decision_tree_classifier.fit(X_train, Y_train) 

Y_train_predicted = decision_tree_classifier.predict(X_train) 

#Model overfitting evaluation 
print("\nModel overfitting evaluation")
print("ACCURACY SCORE: ", accuracy_score(Y_train, Y_train_predicted)) 

Y_test_predicted = decision_tree_classifier.predict(X_test)

#Model evaluation 
print("\nModel evaluation")
print("ACCURACY SCORE: ", accuracy_score(Y_test, Y_test_predicted)) 

'''
The model would appear to be appropriate for this problem.
'''