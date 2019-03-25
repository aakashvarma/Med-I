import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

df = pd.read_csv('mri-and-alzheimers/oasis_longitudinal.csv')
df = df.loc[df['Visit']==1] # use first visit data only because of the analysis we're doing
df = df.reset_index(drop=True) # reset index after filtering first visit data
df['M/F'] = df['M/F'].replace(['F','M'], [0,1]) # M/F column
df['Group'] = df['Group'].replace(['Converted'], ['Demented']) # Target variable
df['Group'] = df['Group'].replace(['Demented', 'Nondemented'], [1,0]) # Target variable
df = df.drop(['MRI ID', 'Visit', 'Hand'], axis=1) # Drop unnecessary columns

############## Removing rows with missing values #################

# Dropped the 8 rows with missing values in the column, SES
df_dropna = df.dropna(axis=0, how='any')
pd.isnull(df_dropna).sum()

df_dropna['Group'].value_counts()


############### Imputation ###############

# Draw scatter plot between EDUC and SES
x = df['EDUC']
y = df['SES']

ses_not_null_index = y[~y.isnull()].index
x = x[ses_not_null_index]
y = y[ses_not_null_index]

# Draw trend line in red
z = np.polyfit(x, y, 1)
p = np.poly1d(z)
plt.plot(x, y, 'go', x, p(x), "r--")
plt.xlabel('Education Level(EDUC)')
plt.ylabel('Social Economic Status(SES)')

# plt.show()

df.groupby(['EDUC'])['SES'].median()


df["SES"].fillna(df.groupby("EDUC")["SES"].transform("median").astype(float), inplace=True)
pd.isnull(df['SES']).value_counts()

############### Splitting Train/Validation/Test Sets ###############

from sklearn.model_selection import train_test_split
from sklearn import preprocessing
from sklearn.preprocessing import MinMaxScaler 
from sklearn.model_selection import cross_val_score

# Dataset with imputation
Y = df['Group'].values.astype(float) # Target for the model
X = df[['M/F', 'Age', 'EDUC', 'SES', 'MMSE', 'eTIV', 'nWBV', 'ASF']].astype(float) # Features we use

# splitting into three sets
X_trainval, X_test, Y_trainval, Y_test = train_test_split(X, Y, random_state=0)

scaler = MinMaxScaler().fit(X_trainval)
X_trainval_scaled = scaler.transform(X_trainval)
X_test_scaled = scaler.transform(X_test)

# Feature scaling
def getScalledData(inputData):
        X_test_scaled = scaler.transform(inputData)
        return X_test_scaled

# Dataset after dropping missing value rows
Y = df_dropna['Group'].values.astype(float) # Target for the model
X = df_dropna[['M/F', 'Age', 'EDUC', 'SES', 'MMSE', 'eTIV', 'nWBV', 'ASF']].astype(float) # Features we use

# splitting into three sets
X_trainval_dna, X_test_dna, Y_trainval_dna, Y_test_dna = train_test_split(X, Y, random_state=0)

# Feature scaling
scaler = MinMaxScaler().fit(X_trainval_dna)
X_trainval_scaled_dna = scaler.transform(X_trainval_dna)
X_test_scaled_dna = scaler.transform(X_test_dna)



# print X_test_scaled


# ################## classifier

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, roc_curve, auc
from sklearn.tree import DecisionTreeClassifier

def predict(X_test_scaled):
        acc = []
        kfolds = 5
        best_score = 0

        for md in range(1, 9): # iterate different maximum depth values
        # train the model
                treeModel = DecisionTreeClassifier(random_state=0, max_depth=md, criterion='gini')
                # perform cross-validation
                scores = cross_val_score(treeModel, X_trainval_scaled, Y_trainval, cv=kfolds, scoring='accuracy')
                
                # compute mean cross-validation accuracy
                score = np.mean(scores)
                
                # if we got a better score, store the score and parameters
                if score > best_score:
                        best_score = score
                        best_parameter = md

        # a model on the combined training and validation set        
        SelectedDTModel = DecisionTreeClassifier(max_depth=best_parameter).fit(X_trainval_scaled, Y_trainval )
        PredictedOutput = SelectedDTModel.predict(X_test_scaled)
        return PredictedOutput


# getdata = getScalledData([[144, 0.0, 76.0, 3.0, 26.0, 1391.0, 0.705, 1.262]])
# print(predict(getdata))




















