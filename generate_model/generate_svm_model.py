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

    X_train=np.zeros((len(train_images),len(train_images[0])))
    y_train=np.zeros(len(train_labels))
    X_test=np.zeros((len(test_images),len(test_images[0])))
    y_test=np.zeros(len(test_labels))
    for i in range(len(train_images)):
#        print("train_images[i]:",train_images[i])
        X_train[i]=train_images[i]
        y_train[i]=train_labels[i]

    for i in range(len(test_images)):
        X_test[i]=test_images[i]
        y_test[i]=test_labels[i]

    df_train_X=DataFrame(X_train)
    df_train_Y=DataFrame(y_train)
    df_test_X=DataFrame(X_test)
    df_test_Y=DataFrame(y_test)

    # print(knn.predict(df_test_X))

#    svc = SVC()
#    svc.fit(df_train_X, df_train_Y)
    
    neigh = KNeighborsClassifier(n_neighbors=10)
    neigh.fit(df_train_X, df_train_Y)

    joblib.dump(neigh,"neigh_model.m")

    # Y_pred = svc.predict(df_test_X)
    acc_svc = round(neigh.score(df_test_X, df_test_Y) * 100, 2)
    print(acc_svc)
if __name__=="__main__":
    main()
