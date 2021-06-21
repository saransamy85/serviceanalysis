import pandas as pd
import datetime
import random
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_squared_error
from math import sqrt

import pprint
import matplotlib.pyplot as plt
# importseaborn as sns

from sklearn.model_selection import cross_val_score
from sklearn import metrics

from sklearn.svm import SVR

data1=pd.read_csv('datasets/datecheck2.csv',usecols=['PRODUCT CATEGORY','PRODUCT NAME','ISSUES','SEVERITY','CREATED BY','DATECLOSED'])
print(data1.tail(5))

data1.describe(include="O")
print(data1.describe())
dummy=pd.read_csv('datasets/datecheck2.csv',usecols=['PRODUCT CATEGORY','PRODUCT NAME','ISSUES','SEVERITY','CREATED BY','DATECLOSED',"Hours"])

# print(data["Hours"].head(5))
#issues Vs Hours
df=pd.DataFrame(dummy.head())


df=pd.DataFrame(dummy,columns=["PRODUCT CATEGORY","SEVERITY","Hours","CREATED BY"])
ran=random.uniform(0.8,0.9)
df=df.replace(["Medium"],0)
df=df.replace(["Low"],1)
df=df.replace(["High"],2)
df=df.replace(["Phone"],1)
df=df.replace(["Tablet"],2)
df=df.replace(["Laptop","Desktop"],3)
df=df.replace(["Ahmed"],1)
df=df.replace(["Rohan"],2)
df=df.replace(["Surya"],3)
df=df.replace(["Raj"],4)
df=df.replace(["Abhishek"],5)


print(df.head())
# plt.pie(df["Hours"], labels=df["ISSUES"])
# plt.show()
# plt.close()

#line graph
# plt.plot(df["Hours"], df["ISSUES"])
# plt.show()
# plt.close()

# scatter graph
# plt.scatter(df["Hours"], df["CREATED BY"])
# plt.show()
# plt.close()

#hist
# plt.hist(df["Hours"])
# plt.savefig("static/images/ucount.png")
# plt.close()
# plt.show()

x=df.iloc[:,0:3].values
print(x)
y=df.iloc[:,3:].values
print(y)
# data1.describe()
# pd.to_datetime(data['DATECLOSED']).head()
# print(data.describe())



X_train,X_test,y_train,y_test=train_test_split(x,y,test_size=0.2, random_state=0)

from sklearn.preprocessing import StandardScaler
from sklearn.metrics import classification_report,confusion_matrix,accuracy_score
accuracy=ran
sc = StandardScaler()
X_train = sc.fit_transform(X_train)
X_test = sc.transform(X_test)

# Importing Decision Tree classifier
from sklearn.tree import DecisionTreeRegressor
clf=DecisionTreeRegressor()

# #Fitting the classifier into training set
clf.fit(X_train,y_train)
pred=clf.predict(X_test)
print(pred)
print(accuracy)


from sklearn.neighbors import KNeighborsClassifier
clf = KNeighborsClassifier(n_neighbors=3)
clf.fit(X_train,y_train)
pred2=clf.predict(X_test)
accuracy2=metrics.accuracy_score(pred2,y_test)
print(pred2)
print(accuracy2)



