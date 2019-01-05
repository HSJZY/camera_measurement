import numpy as np
import pandas as pd
from pandas import DataFrame

# machine learning
from sklearn.neighbors import KNeighborsClassifier
from sklearn.externals import joblib

def main():
    images_data=np.load("./data/encoded_data_0_5.npy")
    images_label=np.load("./data/labels_0_5.npy")
    cut_num=2100
    train_images,train_labels,test_images,test_labels=images_data[:cut_num,:],images_label[:cut_num],images_data[cut_num:,:],images_label[cut_num:]

    df_train_X=DataFrame(np.array(train_images))
    df_train_Y=DataFrame(np.int64(train_labels))
    
#    print("df_train_X",df_train_X)
    
    df_test_X=DataFrame(np.array(test_images))
    df_test_Y=DataFrame(np.int64(test_labels))

    neigh = KNeighborsClassifier(n_neighbors=7)
#    neigh.fit(df_train_X, df_train_Y)
    neigh.fit(df_train_X,df_train_Y)

    joblib.dump(neigh,"en_neigh_model.m")

    Y_pred = neigh.predict(df_test_X)
#    print("X_train:",df_train_X)
#    print("Y_train:",df_train_Y)
#    print("len1,len2:",len(df_train_X[0]),len(df_train_Y[0]))
#    print("df_test_X",df_test_X.head(10))
#    print("df_train_X",df_train_X.head(10))
#    print("predict prob:",neigh.predict_proba(df_test_X)[0])
    print("neigh.predict(df_test_X):",Y_pred)
    print("real:",test_labels)
    acc_svc = round(neigh.score(df_test_X, df_test_Y) * 100, 1)
    print(acc_svc)
if __name__=="__main__":
    main()
