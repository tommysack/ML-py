import pandas as pd
import seaborn as sns
from sklearn import metrics
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import BernoulliNB

#Load data
reviews_df = pd.read_csv("../../../../../data/movie_review.csv")

#General info
reviews_df.head()
reviews_df.describe() 
reviews_df.shape #6 columns, 64720 rows
reviews_df['tag'].unique() #array(['pos', 'neg'], dtype=object) => binary classification
sns.countplot(data=reviews_df, x='tag') #Ok, the classes are quite distributed
reviews_df.isnull().sum() 

#Correlation between data/target
#The column "text" contains phrases in natural language, it's not possible check correlation with corr() that  works only for numbers

'''
The data are phrases in natural language.
The goal is to assign a class label Y (binary classification with values "pos" or "neg") to input X.
In this case we use BernoulliNB that use Naive Bayes algorithm and it works on Bernoulli distribution.
It makes a binary classifier. 
'''

#Separates data in numpy.ndarray columns data/target 
X = reviews_df["text"].values 
Y = reviews_df["tag"].values

#Separates data in rows train/test
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.3, random_state=42)

bernoulli = BernoulliNB()

#BernoulliNB is designed for binary/boolean features, than we need one-hot encoding. 
#We can encode X with "bag of words" CountVectorizer using binary=True parameter (One-hot).
#It returns scipy.sparse._csr.csr_matrix that is allowed for train_test_split 
count_vectorizer = CountVectorizer(binary=True, lowercase=True, stop_words='english')

X_train_vector = count_vectorizer.fit_transform(X_train) 

bernoulli.fit(X_train_vector, Y_train) #Building model

Y_train_predicted = bernoulli.predict(X_train_vector)

#Model overfitting evaluation (the Harmonic Precision-Recall Mean)
print("\nModel overfitting evaluation")
print("F1 SCORE: ", metrics.f1_score(Y_train, Y_train_predicted, average='macro')) #Best possible score is 1.0

X_test_vector = count_vectorizer.transform(X_test)

Y_test_predicted = bernoulli.predict(X_test_vector)

#Model evaluation (the Harmonic Precision-Recall Mean)
print("\nModel evaluation")
print("F1 SCORE: ", metrics.f1_score(Y_test, Y_test_predicted, average='macro')) #Best possible score is 1.0

'''
The metric makes me think that there is moderate overfitting.
'''

#Try to predict a new case

x = ["I liked soundtrack, photography and the cast but the film was really long and it lacked of a good plot."]
x = count_vectorizer.transform(x)

y = bernoulli.predict(x)
print("\nSentiment analysis of review: ", y[0])

