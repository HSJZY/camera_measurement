import numpy as np
import pandas as pd
from pandas import DataFrame

# machine learning
from sklearn.linear_model import LogisticRegression
from sklearn.svm import SVC, LinearSVC
from sklearn.ensemble import RandomForestClassifier
from sklearn.neighbors import KNeighborsClassifier
from sklearn.naive_bayes import GaussianNB
from sklearn.linear_model import Perceptron
from sklearn.linear_model import SGDClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.externals import joblib

def main():
    train_images,train_labels,test_images,test_labels=np.load("dataset_digit.npy")

#    X_train=np.zeros((len(train_images),len(train_images[0])))
#    y_train=np.zeros(len(train_labels))
#    X_test=np.zeros((len(test_images),len(test_images[0])))
#    y_test=np.zeros(len(test_labels))
    
    X_train=[]
    y_train=[]
    X_test=[]
    y_test=[]
    
    
#    print("train_images:",train_images)
    
    for i in range(len(train_images)):
        
        if type(train_images[i][0])==type(1):
            if type(train_images[i])!=list:
                train_images[i]=train_images[i].tolist()
            if len(train_images[i])!=784:
                continue
#            print("train_images[i]:",train_images[i])
            X_train.append(train_images[i])
            y_train.append(int(train_labels[i]))
        else:
#            print("train_images[i]:",train_images[i][0])
            if type(train_images[i][0])!=list:
                train_images[i][0]=train_images[i][0].tolist()
            if len(train_images[i][0])!=784:
                continue
            X_train.append(train_images[i][0])
            y_train.append(int(train_labels[i]))

    for i in range(len(test_images)):
        if type(test_images[i][0])==type(1):
            X_test.append(test_images[i])
            y_test.append(int(test_labels[i]))
        else:
            X_test.append(test_images[i][0])
            y_test.append(int(test_labels[i]))
        
#    print("np.array(X_train)",np.array(X_train))
    df_train_X=DataFrame(np.array(X_train))
    df_train_Y=DataFrame(np.int64(y_train))
    
#    print("df_train_X",df_train_X)
    
    df_test_X=DataFrame(np.array(X_test))
    df_test_Y=DataFrame(np.int64(y_test))
    
#    print(df_train_X)
#    print(df_train_Y)

    # print(knn.predict(df_test_X))

#    svc = SVC()
#    svc.fit(df_train_X, df_train_Y)
    
    neigh = KNeighborsClassifier(n_neighbors=7)
#    neigh.fit(df_train_X, df_train_Y)
    neigh.fit(df_train_X,df_train_Y)

    joblib.dump(neigh,"neigh_model.m")

    Y_pred = neigh.predict(df_test_X)
#    print("X_train:",df_train_X)
#    print("Y_train:",df_train_Y)
#    print("len1,len2:",len(df_train_X[0]),len(df_train_Y[0]))
#    print("df_test_X",df_test_X.head(10))
#    print("df_train_X",df_train_X.head(10))
#    print("predict prob:",neigh.predict_proba(df_test_X)[0])
    print("neigh.predict(df_test_X):",Y_pred)
    print("real:",y_test)
    acc_svc = round(neigh.score(df_test_X, df_test_Y) * 100, 1)
    print(acc_svc)
if __name__=="__main__":
    main()
