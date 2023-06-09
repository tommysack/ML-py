import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_breast_cancer
from skfeature.function.similarity_based import fisher_score

'''
It is commonly used to select the variable that minimizes the Fisher's score.
The Fisher's score is the gradient or the derivative of the log-likelihood, then when the score = 0
we have the maximum likelihood.
'''

#Load data
breast_cancer = load_breast_cancer()

breast_cancer_df = pd.DataFrame(breast_cancer.data, columns=breast_cancer.feature_names)

#Separates data in numpy.ndarray columns data/target 
X = breast_cancer.data
Y = breast_cancer.target

ranks = fisher_score.fisher_score(X, Y)

#Draw the importances of all features
breast_cancer_df_len = len(breast_cancer_df.columns)
breast_cancer_df_importances = pd.Series(ranks, breast_cancer_df.columns[0:breast_cancer_df_len])
sns.barplot(x=breast_cancer_df_importances.values, y=breast_cancer_df_importances.index, color='#BB0000')
plt.show()

