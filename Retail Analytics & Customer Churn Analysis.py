# -*- coding: utf-8 -*-
"""Project.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1FDC6nVq-B50PqpGOGaoTzE-DlR5LcDHu

# **Abstract**
In this project, I have used the retail transactional dataset from the UCI Machine Learning Repository. Based on the UCI website, the data contains the transactions of a UK-based and registered non-store online retail carried out between 01-12-2010 and 09-12-2011. The company is the main seller of unique all-occasion gifts and the customers of the company are mainly wholesalers. My aim in this project is to perform exploratory, descriptive, predictive, and prescriptive analysis to help organizations to improve their sale and revenue using transactional data. I have extended my research of the analysis conducted on this dataset, and performed exploratory data analysis, determined product performance based on the transactions using association rules, devised a Loyalty program based on customer segmentation using clustering algorithms, and strategy recommendations for customer retention using five comparative classification models. I have carried out the analysis and implemented the algorithms using Python programming. The preliminary results of my analysis are adequate for retail businesses to dive deep into the nuances of transactional models in retail and e-commerce industry.

## **Import Libraries**
"""

# Commented out IPython magic to ensure Python compatibility.
# Importing Libraries
import pandas as pd
import numpy as np
import warnings
import datetime
import datetime as dt
import seaborn as sns
import matplotlib.pyplot as plt
# %matplotlib inline

"""## **READ FILE**"""

# Importing csv file into the system.
dataframe = pd.read_excel('http://archive.ics.uci.edu/ml/machine-learning-databases/00352/Online%20Retail.xlsx')

df = pd.DataFrame(dataframe)

# Understanding the data.
df.head()

df.info()

df.shape

#Checking number of NULL VALUES in the dataframe
np.sum(df.isnull())

print("Customers missing: ", round(df['CustomerID'].isnull().sum() * 100 / len(df),3),"%" )

# Removing instances where Customer ID = NULL
df.dropna(subset=['CustomerID'],how='all',inplace=True)

# Removing negative values of Quantity in the dataframe if present.
df = df.drop(df[(df["Quantity"] < 0)].index)

# Dropping zero values of Unit Price
df = df.drop(df[(df["UnitPrice"] == 0)].index)

# Considering data for the year 2011 because for the year 2010, only December data is available.
df = df.query("InvoiceDate.dt.year != 2010")

df.head()

df.shape

# Removing all other values from Stock Code except Product Codes.
df = df.drop(df[df['StockCode'].astype('str') == 'M'].index)
df = df.drop(df[df['StockCode'].astype('str') == 'PAD'].index)
df = df.drop(df[df['StockCode'].astype('str') == 'C2'].index)
df = df.drop(df[df['StockCode'].astype('str') == 'BANK CHARGES'].index)
df = df.drop(df[df['StockCode'].astype('str') == 'POST'].index)
df = df.drop(df[df['StockCode'].astype('str') == 'DOT'].index)

df.shape

# Number of Unique Transactions 
print("Number of transactions: ", df['InvoiceNo'].nunique())
print("Number of products bought: ", df['StockCode'].nunique())
print("Number of customers:", df['CustomerID'].nunique())
print('Number of countries: ', df['Country'].nunique())

ux=["Transactions", "Products Sold", "Customers"]
uy = [df['InvoiceNo'].nunique(), df['StockCode'].nunique(), df['CustomerID'].nunique()]
unique = pd.DataFrame(np.column_stack([ux, uy]), columns=['Variables', 'Unique Count'])
unique.head()

fig = plt.figure()
a = fig.add_axes([0,0,1,1])
a.set_ylabel('Unique Counts')
a.set_xlabel('Variables')
a.bar(ux,uy, color=['#4970D1', '#EE59A6', '#FF9048'])
plt.title('Distinct values of Numerical Variables', fontsize = 16)

plt.show()

df.info()

df.head()

#EXPLORING Top 5 COUNTRIES on the basis of Customers per Country:-
top_5_countries = pd.DataFrame(df.groupby('Country')['CustomerID'].nunique())
top_5_countries.columns = ['Customers_by_Country']
top_5_countries.sort_values('Customers_by_Country', inplace=True, ascending=False)
top_5_countries = top_5_countries[:5][:]

figure, axis = plt.subplots(figsize=(6,4),dpi=100)
axis=sns.barplot(x=top_5_countries.index, y=top_5_countries['Customers_by_Country'])
axis.set_xticklabels(axis.get_xticklabels(), rotation=0, fontsize=9, ha="center")

for i in axis.patches: axis.annotate("%.2f" % i.get_height(), (i.get_x() + i.get_width() / 2., i.get_height()),
                 ha='center', va='center', fontsize=9, color='gray', xytext=(0, 4), textcoords='offset points')
plt.xlabel('Country')
plt.ylabel('Number of Customers')
plt.title('Customers per Country')
plt.show()

# Considering data for United Kingdom because it has maximum customers.
df_uk = df[df['Country'] =="United Kingdom"]

df_uk.shape

"""**TOP 5 Product ID (StockCode)**"""

# Considering Top 5 StockCode on the basis of Count of Description
pro = df_uk[['StockCode','Description']].groupby(['StockCode'])['Description'].size().nlargest(5).reset_index(name='Count')

pro.head()

fig, axis = plt.subplots(figsize=(6,4),dpi=100)
axis=sns.barplot(x=pro['StockCode'], y=pro['Count'])
axis.set_xticklabels(axis.get_xticklabels(), rotation=0, fontsize=9, ha="center")
plt.title("Top 5 products purchased")
plt.xlabel("Product Code")
plt.ylabel("Quantity Sold")

for i in axis.patches:
             axis.annotate("%.2f" % i.get_height(), (i.get_x() + i.get_width() / 2., i.get_height()),
                 ha='center', va='center', fontsize=9, color='gray', xytext=(0, 4),
                 textcoords='offset points')

plt.show()

df_uk['Date'], df_uk['Time'] = df_uk['InvoiceDate'].dt.normalize(), df_uk['InvoiceDate'].dt.time
# Adding 1 because we want to start days from Monday rather than Sunday.
df_uk.insert(loc=10, column='Day', value=(df_uk.InvoiceDate.dt.dayofweek)+1)
# Generating new feature Revenue by multiplying Quantity and Unit Price.
df_uk['Total_revenue'] = df_uk['Quantity'] * df_uk['UnitPrice']

df_uk.head()

# Aggregating Total Revenue generated each day. 
df_revenue = df_uk.groupby(['Date'],as_index=False).agg({'Total_revenue': 'sum'})

df_revenue.head()

# Converting into date format just to ensure that each instance is in date format.
df_revenue['Date'] = pd.to_datetime(df_revenue['Date'])
df_revenue['Date'] = pd.to_datetime(df_revenue['Date'], format="%Y-%m-%d")
df_revenue.set_index('Date', inplace=True)

df_revenue.head()

# Time Series Plot.
df_revenue.plot(figsize = (15,6))
plt.xlabel('Date',fontsize = 13)
plt.ylabel('Total Revenue', fontsize = 13)
plt.xticks(rotation=0, ha='center')
plt.title('Revenue trend over the period of year 2011', fontsize = 16)
plt.show()

# Month wise purchase pattern of Customers.
dtc = (df_uk['Date'].dt.strftime("%b")).value_counts(sort=True)
plt.subplots(figsize=(10,6),dpi=100)
plt.bar(dtc.index, dtc)
plt.title("Month wise purchase pattern (Highest to Lowest)")
plt.ylabel("Number of Customers")
plt.xlabel("Month")
plt.show()

# Daywise purchase pattern of Customers.
axis = df_uk.groupby('InvoiceNo')['Day'].unique().value_counts().sort_index().plot(kind='bar', figsize=(10,6))
axis.set_xlabel('Day',fontsize=12)
axis.set_ylabel('Number of Orders',fontsize=12)
axis.set_title('Number of orders for different Days',fontsize=12)
axis.set_xticklabels(('Mon','Tue','Wed','Thur','Fri','Sun'), rotation='horizontal', fontsize=12)
plt.show()

# Converting Time Feature into 24 intervals of 1 hour each.
s = df_uk['InvoiceDate'].dt.floor('1H')
df_uk['Time'] = s.dt.strftime('%H:%M')

# Hourly Purchase pattern of Customers.
dtc = (df_uk['Time']).value_counts(sort=False).sort_index(ascending=True)
plt.subplots(figsize=(10,6),dpi=100)
plt.bar(dtc.index, dtc)
plt.title("Peak Load purchase pattern per year")
plt.ylabel("Number of Customers")
plt.xlabel("Hourly intervals")
plt.show()

"""# **Association Rules**"""

# Importing libraries for Association Rules.
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# Dividing each Invoice on the basis of Description.
case_UK = (df_uk.groupby(['InvoiceNo', 'Description'])['Quantity'].sum().unstack().reset_index().fillna(0).set_index('InvoiceNo'))

case_UK

# One Hot Encoding.
def OHE(x): 
    while(x<=0): return 0
    while(x>=1): return 1

case_encoded = case_UK.applymap(OHE) 
case_UK = case_encoded

case_encoded

# Building the asociation model with Minimum Support.
support_items = apriori(case_UK, min_support = 0.01, use_colnames = True)

# Itemsets in the descending order based on their support.
support_items.sort_values(by=['support'], ascending=False)

# Applying Association Rule and sorting in descending order on the basis of "Confidence" and "Lift".
associationRule = association_rules(support_items, metric ="lift", min_threshold = 1) 
associationRule = associationRule.sort_values(['confidence', 'lift'], ascending =[False, False])

associationRule

"""# **Clustering Analysis**"""

# Importing libraries for KMeans and PCA.
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans
from sklearn.decomposition import PCA

# Performing RFM analysis for Customer Segmentation. 
dfRecency = df_uk.groupby('CustomerID', as_index=False)['Date'].max()
dfRecency.columns = ['CustomerID', 'RecentBuyDate']
dfRecency.head()

# Calculating Recency by Feature Engineering using Recent Buy Date. 
dfRecency['RecentBuyDate'] = pd.to_datetime(dfRecency['RecentBuyDate']).dt.date
dfRecency['Recency'] = dfRecency['RecentBuyDate'].apply(lambda current: (dt.date(2011,12,9) - current).days)
dfRecency.drop('RecentBuyDate', axis=1, inplace=True)
# Sorting Recency in Descending Order.
dfRecency.sort_values(by='Recency', ascending=False).head()

# Check and drop any dupicates for "Invoice No." and "Customer ID" if present.
dfFreqUk = pd.DataFrame(df_uk)
dfFreqUk.drop_duplicates(subset=['InvoiceNo', 'CustomerID'], inplace=True)

# Calculating Frequency by Feature Engineering using Customer ID.
dfFrequency = dfFreqUk.groupby('CustomerID', as_index=False)['InvoiceNo'].count()
dfFrequency.columns = ['CustomerID','Frequency']
dfFrequency.head()

# Calculating Monetary by Feature Engineering using Total Revenue. 
dfMonetary = df_uk.groupby('CustomerID', as_index=False).agg({'Total_revenue': 'sum'})
dfMonetary.columns = ['CustomerID', 'Monetary']
dfMonetary.head()

# Grouping "Recency", "Frequency", "Monetary" 
dfMerge1 = dfRecency.merge(dfFrequency, on='CustomerID')
dfMerge = dfMerge1.merge(dfMonetary,on='CustomerID')
dfMerge.set_index('CustomerID',inplace=True)
dfMerge.head()

# Making Quantiles
classOfValues = dfMerge.quantile(q=[0.25,0.5,0.75])
classOfValues

# Generating RQuartile, FQuartile and MQuartile and assigning values- (1,2,3,4) 
# Value is denoted by a, recency denoted by r, quartiles denoted by x
def RecencyQuartile(a,r,x):
    if a <= x[r][0.25]: return 4
    elif a <= x[r][0.50]: return 3
    elif a <= x[r][0.75]: return 2
    else: return 1
# Value is denoted by a, Frequency-Monetary denoted by m, quartiles denoted by x
def FrequencyMonetaryQuartile(a,m,x):
    if a <= x[m][0.25]: return 1
    elif a <= x[m][0.50]: return 2
    elif a <= x[m][0.75]: return 3
    else: return 4

# Build RFM Segmentation Table.
dfSeg = pd.DataFrame(dfMerge)
dfSeg['RQuartile'] = dfSeg['Recency'].apply(RecencyQuartile, args=('Recency',classOfValues))
dfSeg['FQuartile'] = dfSeg['Frequency'].apply(FrequencyMonetaryQuartile, args=('Frequency',classOfValues))
dfSeg['MQuartile'] = dfSeg['Monetary'].apply(FrequencyMonetaryQuartile, args=('Monetary',classOfValues))

dfSeg.head()

# Grouping RQuartile, FQuartile and MQuartile to generate new feature Group which provides insights regarding customer behaviour.
dfSeg['Group'] = dfSeg.RQuartile.map(str) + dfSeg.FQuartile.map(str) + dfSeg.MQuartile.map(str)
dfSeg.head()

# Converting Group Variable into Score so that Intervals can be formed.
dfSeg['Score'] = dfSeg[['RQuartile', 'FQuartile', 'MQuartile']].sum(axis = 1)
dfSeg.head()

dfSeg.shape

# Distribution plot for Recency, Frequency and Monetary to visualize each generated feature.
plt.figure(figsize=(16,4))
plt.subplot(1, 3, 1)
#Distribution plot for Recency
axis = sns.distplot(dfSeg['Recency'], color = 'red')
plt.title("Distribution plot for Recency")
plt.subplot(1, 3, 2)
#Distribution plot for Frequency
axis = sns.distplot(dfSeg['Frequency'], color='limegreen')
plt.title("Distribution plot for Frequency")
plt.subplot(1, 3, 3)
#Distribution plot for Monetary
axis = sns.distplot(dfSeg['Monetary'], color = 'blue')
plt.title("Distribution plot for Monetary")
plt.show()

# Logarithmic transformation for Recency, Frequency and Monetary features.
# Adding delta(0.05) component for zero and negative values to handle infinite numbers generated during log transformation as Log(0)=undefined
rfm_r_log = np.log(dfSeg['Recency']+0.05)
rfm_f_log = np.log(dfSeg['Frequency']+0.001) 
rfm_m_log = np.log(dfSeg['Monetary']+0.05)
dfLog = pd.DataFrame({'Monetary': rfm_m_log, 'Recency': rfm_r_log, 'Frequency': rfm_f_log})

# As recency can never be negative so ensuring that condition.
dfLog = dfLog.drop(dfLog[(dfLog["Recency"] < 0)].index)

dfLog

# Correlation Plot for RFM values without and with log transformation.
plt.figure(figsize=(16,4))
plt.subplot(1, 2, 1)
sns.heatmap(dfSeg[['Recency', 'Frequency', 'Monetary']].corr(), annot = True, cmap="BuPu")
plt.yticks(va="center")
plt.title("Correlation Plot of RFM")
plt.subplot(1, 2, 2)
sns.heatmap(dfLog.corr(), annot = True, cmap="BuPu")
plt.yticks(va="center")
plt.title("Correlation Plot of log values of RFM")
plt.show()

# Segmenting customers on the basis of Loyalty Class by generating intervals from Score variable.
dfSeg['Interval'] = pd.cut(x=dfSeg['Score'], bins=[0, 3, 6, 10, 12])
dfSeg['LoyaltyClass'] = pd.cut(x=dfSeg['Score'], bins=[0, 3, 6, 10, 12], labels=['Bronze', 'Silver', 'Gold', 'Platinum'])
dfSeg.head()

dfSegB = pd.DataFrame(dfSeg)
dfSegB.reset_index(drop=True, inplace=True)
dfSegBox = dfMerge1.merge(dfMonetary,on='CustomerID')
dfSegBox.set_index('CustomerID',inplace=False)
dfSegBox.reset_index(drop=True, inplace=True)
dfSegBox.head()
dfSegBoxCon = pd.concat([dfSegBox, dfSeg.iloc[:,-1]], axis=1)

dfSegBoxCon.head()

# Number of customers in each Loyalty class.
axis = sns.countplot(x="LoyaltyClass", data=dfSegBoxCon)
for i in axis.patches:
    h = i.get_height()
    axis.text(i.get_x()+i.get_width()/2.,h+10,
              '{:1.2f}%'.format(h/len(dfSegBoxCon)*100),ha="center",fontsize=10) 
plt.xlabel('Loyalty classes')
plt.ylabel('Number of Customers')
plt.title('Number of Customers in each Cluster')
plt.show()

# Revenue generated from each cluster , and taking revenue less than 7000 for visualization purpose. 
z = dfSegBoxCon[dfSegBoxCon["Monetary"]<7000]
sns.boxplot(x="LoyaltyClass", y="Monetary", data=z)
plt.xlabel('Loyalty classes')
plt.ylabel('Revenue')
plt.title('Monetary value for each Cluster')
plt.show()

len(dfSegBoxCon)

# Using values of revenue less than 7000, instances decreases by 117 so just for visualization in boxplot it won't make much difference.
len(z)

# Distribution plot for log transformed values of Recency, Frequency and Monetary.
plt.figure(figsize=(16,4))
plt.subplot(1, 3, 1)
#Distribution plot for Recency
axis = sns.distplot(dfLog['Recency'], color = 'red')
plt.title("Distribution plot for Recency")
plt.subplot(1, 3, 2)
#Distribution plot for Frequency
axis = sns.distplot(dfLog['Frequency'], color='limegreen')
plt.title("Distribution plot for Frequency")
plt.subplot(1, 3, 3)
#Distribution plot for Monetary
axis = sns.distplot(dfLog['Monetary'], color = 'blue')
plt.title("Distribution plot for Monetary")
plt.show()

"""**PCA and K-means** \
PCA will be carried out on Log transformed data because as observed in the above graph, Recency and Monetary are approximately normal, whereas frequency is right skewed, i.e., 20% of the customers are frequent.
"""

# Scatter plot for Frequency and Recency of Customers.
plt.figure(figsize=(10,6))
plt.scatter(dfLog["Recency"],dfLog["Frequency"])
plt.xlabel("Recency")
plt.ylabel("Frequency")
plt.title("Relationship between Recency and Frequency of the Customers")
plt.show()

# Scaling the data to achieve normalized values.
s = StandardScaler()
segm_std = s.fit_transform(dfLog)

pca = PCA()
pca.fit(segm_std)

# Obtaining Explained variance for 3 factors.
pca.explained_variance_ratio_

# Plotting the explained variance by components to get number of components.
plt.figure(figsize = (10,6))
plt.plot(range(1,4),pca.explained_variance_ratio_.cumsum(), marker = 'o', linestyle = "dashdot")
plt.title("Explained Variance by Components")
plt.xlabel("Number of Components")
plt.ylabel("Cumulative Explained Variance")
plt.show()

pca = PCA(n_components=2)

pca.fit(segm_std)

# Obtaining PCA scores.
scoresPCA = pca.transform(segm_std)

# Using PCA scores in K Means algorithm.
SS = []
for i in range(1,7):
  model = KMeans(n_clusters=i,init='k-means++',random_state=30)
  model.fit(scoresPCA)
  SS.append(model.inertia_)

# Obtaining Silhoutte_Score to know number of clusters.
from sklearn.metrics import silhouette_score
for n_clusters in range(2,7):
    km = KMeans(init='k-means++', n_clusters = n_clusters, n_init=100)
    km.fit(dfLog)
    clusters = km.predict(dfLog)
    silhouette_avg = silhouette_score(dfLog, clusters)
    print("For n_clusters =", n_clusters, "The average silhouette_score is :", silhouette_avg)

# Using Elbow method to find number of clusters.
plt.figure(figsize = (10,6))
plt.plot(range(1,7), SS, marker ='o', linestyle ='dashdot')
plt.xlabel("Number of Clusters")
plt.ylabel("Sum of Squared Errors")
plt.title("K-Means with PCA")
plt.show()

model = KMeans(n_clusters=2, init='k-means++', random_state=30)

# Fitting Kmeans model on the basis of PCA scores.
model.fit(scoresPCA)

dfPCA = pd.concat([dfLog.reset_index(drop=True),pd.DataFrame(scoresPCA)],axis=1)
dfPCA.columns.values[-2:] = ["Component-1","Component-2"]
dfPCA["ClassPCA"] = model.labels_

dfPCA.head()

# Plotting 2 clusters formed by PCA.
plt.figure(figsize = (10,6))
sns.scatterplot(dfPCA["Component-1"], dfPCA["Component-2"], hue = dfPCA["ClassPCA"], palette=['r','y'])
plt.title("Clusters by PCA Components")
plt.show()

dfPCA

# Generating new dataframe to divide revenue generated by each class.
dfPCA_ = pd.DataFrame(dfPCA)
dfPCA_.head()

# Converting logarithmic values of monetary to numeric values.
dfPCA_['Monetary'] = np.exp(dfPCA_["Monetary"])

# Obtaining sum of revenue and percentage of revenue for each class. 
dfPCA_ = dfPCA_.groupby('ClassPCA',as_index=False).agg({'Monetary': 'sum'})
dfPCA_['Percentage'] = round(dfPCA_['Monetary']/sum(dfPCA_['Monetary'])*100,2)

dfPCA_

# Plotting revenue for each PCA component using barplot.
axis = sns.barplot(x="ClassPCA", y="Percentage", data=dfPCA_)
for i in axis.patches:
             axis.annotate("%.2f" % i.get_height(), (i.get_x() + i.get_width() / 2., i.get_height()),
                 ha='center', va='center', fontsize=11, color='black', xytext=(0, 5),
                 textcoords='offset points')
plt.xlabel('PCA Components (Clusters)')
plt.ylabel('Revenue %')
plt.title('Percentage Revenue from each Cluster')
plt.show()

"""# **CLASSIFICATION**
## **LOGISTIC REGRESSION**
"""

# Importing libraries for Classification.
from sklearn.linear_model import LogisticRegression
from sklearn import metrics
from sklearn.model_selection import train_test_split
import statsmodels.api as sm
from sklearn.metrics import confusion_matrix
from sklearn.metrics import balanced_accuracy_score
import warnings 
warnings.filterwarnings("ignore")

# Assigning "Recency", "Frequency", "Monetary" in X , while "Loyalty Class" in y.
X = dfSeg[["Recency", "Frequency", "Monetary"]]
y = dfSeg["LoyaltyClass"]

# Splitting into train and test data.
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=0, shuffle=False)

# Model 1 :- Logistic Regression 
model_1 = LogisticRegression()
model_1.fit(X_train, y_train)

y_pred_1 = model_1.predict(X_test)

# Confusion Matrix for Logistic Regression
from sklearn.metrics import confusion_matrix, classification_report
confusionMatrix = confusion_matrix(y_test, y_pred_1)
print(confusionMatrix)

# Plotting Confusion Matrix for logistics regression.
from mlxtend.plotting import plot_confusion_matrix
matrix = np.array(confusionMatrix)

classNames = [{'Platinum' : 0, 'Gold': 1, 'Silver': 2, 'Bronze': 3}]

fig, ax = plot_confusion_matrix(conf_mat = matrix,
                                colorbar = True,
                                show_absolute = False,
                                show_normed = True,
                                cmap="YlGnBu")

plt.show()

# Accuracy and Balanced Accuracy for Logistics Regression.
print('Accuracy         : {}%'.format(round(metrics.accuracy_score(y_test, y_pred_1)*100,2)))

print('Balanced Accuracy: {}%'.format(round(balanced_accuracy_score(y_test, y_pred_1)*100,2)))

print(classification_report(y_test, y_pred_1))

"""## **DECISION TREES**"""

# Importing libraries for Decision Trees
from sklearn import tree
from sklearn.tree import DecisionTreeClassifier, export_graphviz
from sklearn import metrics

# Model 2 :- Decision Trees
from sklearn.metrics import accuracy_score, classification_report
model_2 = DecisionTreeClassifier(min_samples_split=100)
model_2.fit(X_train, y_train)
y_pred_2 = model_2.predict(X_test)

# Confusion Matrix for Decision Tree
from sklearn.metrics import confusion_matrix, classification_report
confusionMatrix = confusion_matrix(y_test, y_pred_2)
print(confusionMatrix)

# Plotting Decision Tree.
tree.plot_tree(model_2)
import graphviz
treeData = tree.export_graphviz(model_2, out_file=None)
network = graphviz.Source(treeData)
network.render("Retail")

# Accuracy and Balanced Accuracy for Decision Tree.
print('Accuracy         : ',round(accuracy_score(y_test, y_pred_2)*100,2),'%')
print('Balanced Accuracy: ',round(balanced_accuracy_score(y_test, y_pred_2)*100,2),'%')

print(classification_report(y_test, y_pred_2))

"""## **NAIVE BAYES**"""

# Importing Libraries for Naive Bayes.
from sklearn.naive_bayes import MultinomialNB
# Model 3 :- Naive Bayes
model_3 = MultinomialNB()
model_3.fit(X_train,y_train)
y_pred_3 = model_3.predict(X_test)
# Accuracy and Balanced Accuracy for Naive Bayes.
print('Accuracy         : ',round(accuracy_score(y_pred_3,y_test)*100,2),'%')
print('Balanced Accuracy: ',round(balanced_accuracy_score(y_pred_3, y_test)*100,2),'%')

# Confusion Matrix for Decision Tree.
from sklearn.metrics import confusion_matrix, classification_report
confusionMatrix = confusion_matrix(y_test, y_pred_3)
print(confusionMatrix)

print(classification_report(y_test, y_pred_3))

"""## **KNN**"""

# Importing Libraries for KNN.
from sklearn.neighbors import KNeighborsClassifier
# Model 4 :- K Nearest Neighbour.
model_4 = KNeighborsClassifier(n_neighbors=3)
model_4.fit(X_train,y_train)
y_pred_4 = model_4.predict(X_test)
# Accuracy and Balanced Accuracy for KNN.
print('Accuracy         : ',round(accuracy_score(y_pred_4,y_test)*100,2),'%')
print('Balanced Accuracy: ',round(balanced_accuracy_score(y_pred_4,y_test)*100,2),'%')

# Confusion Matrix for KNN.
from sklearn.metrics import confusion_matrix, classification_report
confusionMatrix = confusion_matrix(y_test, y_pred_4)
print(confusionMatrix)

print(classification_report(y_test, y_pred_4))

"""## **RANDOM FOREST**"""

# Importing Libraries for Random Forest.
from sklearn.ensemble import RandomForestClassifier
from sklearn.datasets import make_classification
# Model 5 :- Random Forest
model_5 = RandomForestClassifier(max_depth = 3, random_state=0)
model_5.fit(X_train, y_train)
y_pred_5 = model_5.predict(X_test)
# Accuracy and Balanced Accuracy for Random Forest.
print('Accuracy         : ',round(accuracy_score(y_pred_5, y_test)*100,2),'%')
print('Balanced Accuracy: ',round(balanced_accuracy_score(y_pred_5, y_test)*100,2),'%')

# Confusion Matrix for Random Forest.
from sklearn.metrics import confusion_matrix, classification_report
confusionMatrix = confusion_matrix(y_test, y_pred_5)
print(confusionMatrix)

print(classification_report(y_test, y_pred_5))

# Model Comparison on the basis of Accuracy and Balanced Accuracy of each model.
models = {'Classification Model': ['Logistic Regression','Decision Trees','Naive Bayes','K-Nearest Neighbor', 'Random Forest'],
        'Accuracy': [round(accuracy_score(y_pred_1,y_test)*100,2),
                     round(accuracy_score(y_pred_2,y_test)*100,2),
                     round(accuracy_score(y_pred_3,y_test)*100,2),
                     round(accuracy_score(y_pred_4,y_test)*100,2),
                     round(accuracy_score(y_pred_5,y_test)*100,2)],
        'Balanced Accuracy': [round(balanced_accuracy_score(y_pred_1,y_test)*100,2),
                     round(balanced_accuracy_score(y_pred_2,y_test)*100,2),
                     round(balanced_accuracy_score(y_pred_3,y_test)*100,2),
                     round(balanced_accuracy_score(y_pred_4,y_test)*100,2),
                     round(balanced_accuracy_score(y_pred_5,y_test)*100,2)]
        }
models_df = pd.DataFrame(models, columns = ['Classification Model', 'Accuracy', 'Balanced Accuracy'])

models_df

# Model Comparison Plot based on Balanced Accuracy
plt.figure(figsize=(10,6))
axis = sns.barplot(x=models_df['Balanced Accuracy'], y=models_df['Classification Model'], data=models_df, orient='h', saturation=0.8)
axis.axes.set_title("Classification model comparison", fontsize=16)
axis.set_yticklabels(models_df['Classification Model'], fontsize=13)
axis.set_xticklabels([0, 20, 40, 60, 80, 100], fontsize=13) 
plt.xlabel("Balanced Accuracy", fontsize = 13)
plt.ylabel("", fontsize = 10)
plt.subplots_adjust(left=1, right=1.8, top=2.4, bottom=1.8)

for i, p in enumerate(axis.patches):
    axis.annotate("%.2f %%" % (p.get_width()),
                (p.get_x() + p.get_width(), p.get_y() + 0.7),
                xytext=(-48, 10), textcoords='offset points')

plt.show()

"""# **Conclusion**
Retail analytics is mainly focused on customer retention, product performance and revenue optimization. Based on our analysis using the transactional data, we conclude the following: \

*   Top 5 items based on Support value were obtained by performing association rule mining using Apriori algorithm. As an instance, item with description ???White Hanging Heart T-Light Holder??? was observed having maximum support of 0.110385, which implied that this product has highest importance in the Online Retail transactions.
*   Product relationships were determined and identified based on Confidence, Lift, and Leverage metrics. As observed for the maximum confidence, customers purchased (Herb Marker Rosemary) whenever they purchase (Herb Marker Thyme). This association was observed with 95.24% confidence and 84.67% expectation that these item set will be purchased. Similar product relationships were determined for all the products in the transactions which gave an idea of high and low performing products.
*   Customers were segmented into 4 groups using Recency-Frequency-Monetary analysis. Based on these groups, we proposed a Loyalty program model having 4 loyalty classes i.e., Platinum, Gold, Silver and Bronze, to provide customers with pricing and promotions based on how recently the purchase has been carried out by the customer (Recency), how frequently a customer purchases (Frequency), and amount spent by the customer (Monetary)
*   Clusters were formed using Principal Component Analysis and K-means clustering to understand two major clusters which commensurate with 80-20 Pareto Principle by explained variance ratio. This also suggested the fact that there are mainly two types of customers i.e., loyal customers who contribute towards 80% of the revenue, and the others, who have infrequent purchase behaviour.
*   To propose suitable loyalty class to the new customers, multiple classification models were performed using train and test data, having accuracies in the following order: \
Decision Tree ??? Random Forest > K-nearest Neighbour > Logistic Regression > Na??ve Bayes
*   Based on the above supervised and unsupervised machine learning algorithms, we performed a complete retail analytics solution for different aspects of transactional data i.e., customers, products, and transactions, which can be used for revenue optimization, improving product performance and increasing customer retention rate.
"""