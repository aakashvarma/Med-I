import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


sns.set()

df = pd.read_csv('mri-and-alzheimers/oasis_longitudinal.csv')

df = df.loc[df['Visit']==1] # use first visit data only because of the analysis we're doing
df = df.reset_index(drop=True) # reset index after filtering first visit data
df['M/F'] = df['M/F'].replace(['F','M'], [0,1]) # M/F column
df['Group'] = df['Group'].replace(['Converted'], ['Demented']) # Target variable
df['Group'] = df['Group'].replace(['Demented', 'Nondemented'], [1,0]) # Target variable
df = df.drop(['MRI ID', 'Visit', 'Hand'], axis=1) # Drop unnecessary columns


def bar_chart(feature):
    Demented = df[df['Group']==1][feature].value_counts().astype(float)
    Nondemented = df[df['Group']==0][feature].value_counts()
    df_bar = pd.DataFrame([Demented,Nondemented])
    df_bar.index = ['Demented','Nondemented']
    df_bar.plot(kind='bar',stacked=True, figsize=(8,5))

bar_chart('M/F')
plt.xlabel('Group')
plt.ylabel('Number of patients')
plt.legend()
plt.title('Gender and Demented rate')


def analysis():
    #MMSE : Mini Mental State Examination
    # Nondemented = 0, Demented =1
    # Nondemented has higher test result ranging from 25 to 30. 
    #Min 17 ,MAX 30
    facet= sns.FacetGrid(df,hue="Group", aspect=3)
    facet.map(sns.kdeplot,'MMSE',shade= True)
    facet.set(xlim=(0, df['MMSE'].max()))
    facet.add_legend()
    plt.xlim(15.30)

    #bar_chart('ASF') = Atlas Scaling Factor
    facet= sns.FacetGrid(df,hue="Group", aspect=3)
    facet.map(sns.kdeplot,'ASF',shade= True)
    facet.set(xlim=(0, df['ASF'].max()))
    facet.add_legend()
    plt.xlim(0.5, 2)

    #eTIV = Estimated Total Intracranial Volume
    facet= sns.FacetGrid(df,hue="Group", aspect=3)
    facet.map(sns.kdeplot,'eTIV',shade= True)
    facet.set(xlim=(0, df['eTIV'].max()))
    facet.add_legend()
    plt.xlim(900, 2100)

    #'nWBV' = Normalized Whole Brain Volume
    # Nondemented = 0, Demented =1
    facet= sns.FacetGrid(df,hue="Group", aspect=3)
    facet.map(sns.kdeplot,'nWBV',shade= True)
    facet.set(xlim=(0, df['nWBV'].max()))
    facet.add_legend()
    plt.xlim(0.6,0.9)

    #AGE. Nondemented =0, Demented =0
    facet= sns.FacetGrid(df,hue="Group", aspect=3)
    facet.map(sns.kdeplot,'Age',shade= True)
    facet.set(xlim=(0, df['Age'].max()))
    facet.add_legend()
    plt.xlim(50,100)

    #'EDUC' = Years of Education
    # Nondemented = 0, Demented =1
    facet= sns.FacetGrid(df,hue="Group", aspect=3)
    facet.map(sns.kdeplot,'EDUC',shade= True)
    facet.set(xlim=(df['EDUC'].min(), df['EDUC'].max()))
    facet.add_legend()
    plt.ylim(0, 0.16)

    plt.show()



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

# Feature scaling
scaler = MinMaxScaler().fit(X_trainval)
X_trainval_scaled = scaler.transform(X_trainval)
X_test_scaled = scaler.transform(X_test)

# Dataset after dropping missing value rows
Y = df_dropna['Group'].values.astype(float) # Target for the model
X = df_dropna[['M/F', 'Age', 'EDUC', 'SES', 'MMSE', 'eTIV', 'nWBV', 'ASF']].astype(float) # Features we use

# splitting into three sets
X_trainval_dna, X_test_dna, Y_trainval_dna, Y_test_dna = train_test_split(X, Y, random_state=0)

# Feature scaling
scaler = MinMaxScaler().fit(X_trainval_dna)
X_trainval_scaled_dna = scaler.transform(X_trainval_dna)
X_test_scaled_dna = scaler.transform(X_test_dna)






# ################## classifier

from sklearn.linear_model import LogisticRegression
from sklearn.metrics import confusion_matrix, accuracy_score, recall_score, roc_curve, auc
from sklearn.tree import DecisionTreeClassifier


def predict():
        acc = []

        # Dataset with imputation
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

        test_score = SelectedDTModel.score(X_test_scaled, Y_test)
        PredictedOutput = SelectedDTModel.predict(X_test_scaled)
        return PredictedOutput


        # test_recall = recall_score(Y_test, PredictedOutput, pos_label=1)
        # fpr, tpr, thresholds = roc_curve(Y_test, PredictedOutput, pos_label=1)
        # test_auc = auc(fpr, tpr)
        # print("Best accuracy on validation set is:", best_score)
        # print("Best parameter for the maximum depth is: ", best_parameter)
        # print("Test accuracy with best parameter is ", test_score)
        # print("Test recall with best parameters is ", test_recall)
        # print("Test AUC with the best parameter is ", test_auc)

        # m = 'Decision Tree'
        # acc.append([m, test_score, test_recall, test_auc, fpr, tpr, thresholds])

        # print(PredictedOutput)
        # return PredictedOutput
print(X_test)

predict()


# [0., 0.36111111, 0.35294118, 0.25, 0.15384615, 0.17476852, 0.42767296, 0.72647059]


















