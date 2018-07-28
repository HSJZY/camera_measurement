import os
import tensorflow as tf
import urllib.request
import numpy as np
import cv2
import matplotlib.pyplot as plt
from numpy import rot90

def shuffle_data(dataset):
    images=dataset[0]
    labels=dataset[1]
    index=[i for i in range(len(images))]
    np.random.shuffle(index)
#     print("index:",index)
    random_images=[]
    random_labels=[]
    for i in range(len(images)):
        random_images.append(images[index[i]])
        random_labels.append(labels[index[i]])
    #print("random_labels:",random_labels)
    random_dataset=np.array([random_images,random_labels])
    return random_dataset
def rotate_90_img(img,row_size):
    img_matrix=np.array(img).reshape(row_size,row_size).tolist()
    rotated_img=rot90(img_matrix).reshape(-1,row_size*row_size)[0]
    return rotated_img

def main():
    LOGDIR='./tmp/'
#    GIST_URL = 'https://gist.githubusercontent.com/dandelionmane/4f02ab8f1451e276fea1f165a20336f1/raw/dfb8ee95b010480d56a73f324aca480b3820c180/'
#    mnist=tf.contrib.learn.datasets.mnist.read_data_sets(train_dir=LOGDIR+'data',one_hot=True)

    train_images=[]
    train_labels=[]
#    for index,image in enumerate(mnist.train.images):
#        label=np.argmax(mnist.train.labels[index])
#        if label<=5 and label>=1:
#            image[image>0.01]=1
#            image[image<=0.01]=0
#            rotated_img=image
#            for i in range(4):
#                if i==0:
#                    rotated_img=image
#                else:
#                    rotated_img=rotate_90_img(rotated_img,28)
#                train_images.append(rotated_img)
#                train_labels.append(label)
#        else:
#            image[image>0.01]=1
#            image[image<=0.1]=0
#            rotated_img=image
#            for i in range(4):
#                if i==0:
#                    rotated_img=image
#                else:
#                    rotated_img=rotate_90_img(rotated_img,28)
#                train_images.append(image)
#                train_labels.append(0)
#    train_data=(train_images,train_labels)
#    train_data=shuffle_data(train_data)
#    print("len(train_data) before:",len(train_data[0]))
#    train_images=train_data[0][:1].tolist()
#    train_labels=train_data[1][:1].tolist()
#    train_data=(train_images,train_labels)
#    print("len(train_data) after:",len(train_data[0]))

    negative_dataset=np.load("negative_samples.npy")
    labeled_dataset=np.load("labeled_data_after.npy")
    
    # print(negative_dataset)
    for i in range(200):
        print("(negative_dataset[0][i][0]).reshape(1,-1).tolist():",(negative_dataset[0][i][0]).reshape(1,-1).tolist()[0])
        train_images.append((np.int16(negative_dataset[0][i][0]).reshape(1,-1)).tolist()[0])
        train_labels.append(negative_dataset[1][i])
    for i in range(len(labeled_dataset[0])):
        train_images.append(labeled_dataset[0][i])
        train_labels.append(labeled_dataset[1][i])
    # train_images=np.array(train_images)
    train_labels=np.array(train_labels)

    #生成one-hot编码
    # n_class = train_labels.max() + 1
    # n_sample = train_labels.shape[0]
    # print("n_class and n_sample",n_class,n_sample,train_labels)
    # train_labels_onehot = np.zeros((n_sample, n_class)).tolist()
    # for i in range(len(train_labels_onehot)):
    #     train_labels_onehot[i][train_labels[i]]=1

    train_data=(train_images,train_labels)
    train_data=shuffle_data(train_data)
    print("len(train_data):",len(train_data))

    test_images=train_data[0][:1550]
    test_labels=train_data[1][:1550]
    train_images=train_data[0][1550:]
    train_labels=train_data[1][1550:]

    dataset_digit=np.array([train_images,train_labels,test_images,test_labels])
    np.save("dataset_digit",dataset_digit)
    print("len(dataset_digit[0])",len(dataset_digit[0]))
if __name__=="__main__":
    main()
