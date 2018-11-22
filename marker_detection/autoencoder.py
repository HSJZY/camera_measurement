#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Oct 21 22:14:53 2018

@author: jiang

Know more, visit my Python tutorial page: https://morvanzhou.github.io/tutorials/
My Youtube Channel: https://www.youtube.com/user/MorvanZhou
Dependencies:
tensorflow: 1.1.0
matplotlib
numpy
"""
import tensorflow as tf
from tensorflow.examples.tutorials.mnist import input_data
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D
from matplotlib import cm
import numpy as np
import os

tf.set_random_seed(1)

# Hyper Parameters
BATCH_SIZE = 64
LR = 0.0005         # learning rate
N_TEST_IMG = 4
LOAD=True

# tf placeholder
tf_x = tf.placeholder(tf.float32, [None, 28*28])    # value in the range of (0, 1)
# encoder
en0 = tf.layers.dense(tf_x, 128, tf.nn.tanh)
en1 = tf.layers.dense(en0, 64, tf.nn.tanh)
encoded = tf.layers.dense(en1, 16, tf.nn.sigmoid)
# decoder
de1 = tf.layers.dense(encoded, 64, tf.nn.tanh)
de2 = tf.layers.dense(de1, 128, tf.nn.tanh)
decoded = tf.layers.dense(de2, 28*28, tf.nn.sigmoid)
#optimizer
loss = tf.losses.mean_squared_error(labels=tf_x, predictions=decoded)
train = tf.train.AdamOptimizer(LR).minimize(loss)

# tf saver
sess = tf.Session()
saver = tf.train.Saver()
path='./marker_detection/autoencoder_model'
if LOAD:
    saver.restore(sess, tf.train.latest_checkpoint(path))
else:
    sess.run(tf.global_variables_initializer())




def train_model():
    # initialize figure
    f, a = plt.subplots(3, N_TEST_IMG, figsize=(4, 2))
    plt.ion()   # continuously plot
    # original data (first row) for viewing
    imgs_dataset=np.load("./data/data_1_5.npy")
#    labels=np.load("./data/labels_1_5.npy")
    #generate view_data
    #---------------------------生成１－４的观测数据------------------------------------------
    #is_finding=1
    #finding_iter_i=0
    #while(is_finding!=N_TEST_IMG+1):
    #    if labels[finding_iter_i]==is_finding:
    #        plt.imshow(np.reshape(imgs_dataset[finding_iter_i],(28,28)),cmap = 'binary')
    #        plt.show()
    #        _ok=int(input())
    #        if _ok==0:
    #            finding_iter_i+=1
    #            continue
    #        print("testing...")
    #        view_data.append(imgs_dataset[finding_iter_i])
    #        is_finding+=1
    #    finding_iter_i+=1
    #np.save("./generate_model/view_data",view_data)
    #-----------------------------------------------------------------------------------------
    view_data=np.load("../generate_model/view_data.npy")
    for i in range(N_TEST_IMG):
        a[0][i].imshow(np.reshape(view_data[i], (28, 28)), cmap='gray')
        a[0][i].set_xticks(()); a[0][i].set_yticks(())
    
    saved_train_loss=[]
    data_size=len(imgs_dataset)
    for step in range(15000):
        #grap one batch from data
        batch_i=step*BATCH_SIZE%data_size
        batch_i_1=(step+1)*BATCH_SIZE%data_size
        if batch_i>batch_i_1:
            continue
        #print("batch_i:",batch_i,"batch_i_1",batch_i_1)
        b_x = imgs_dataset[batch_i:batch_i_1]
        
        np.reshape(b_x,(BATCH_SIZE,28*28))
        #print("b_x:",b_x.shape,type(b_x))
        _, encoded_, decoded_, loss_ = sess.run([train, encoded, decoded, loss], {tf_x: b_x})
        saved_train_loss.append(loss_)
        if step % 100 == 0:     # plotting
            print('train loss: %.4f' % loss_)
            # plotting decoded image (second row)
            encoded_data = sess.run(encoded, {tf_x: view_data})
            decoded_data = sess.run(decoded, {tf_x: view_data})
            for i in range(N_TEST_IMG):
                a[1][i].clear()
                a[1][i].imshow(np.reshape(encoded_data[i], (4, 4)), cmap='gray')
                a[1][i].set_xticks(()); a[1][i].set_yticks(())
                
                a[2][i].clear()
                a[2][i].imshow(np.reshape(decoded_data[i], (28, 28)), cmap='gray')
                a[2][i].set_xticks(()); a[2][i].set_yticks(())
            plt.draw(); plt.pause(0.01)
    ckpt_path = os.path.join('./model', 'DDPG.ckpt')
    save_path = saver.save(sess, ckpt_path, write_meta_graph=False)
    print("\nSave Model %s\n" % save_path)
    np.save("../generate_model/saved_loss",saved_train_loss)
    print("train loss saved")
    plt.ioff()
def eval_model(img_input):
    img_input=np.reshape(img_input,(-1,784))
    encoded_data = sess.run(encoded, {tf_x: img_input})
    print("encoded_data:",encoded_data[0])
    return encoded_data
    #decoded_data = sess.run(decoded, {tf_x: encoded_data})
def generate_encoded_data():
    imgs=np.load('./data/data_0_5.npy')
    encoded_data=[]
    for i in range(len(imgs)):
        cur_img=imgs[i].reshape((-1,28*28))
        encoded_img=sess.run(encoded,{tf_x:cur_img})
        encoded_data.append(encoded_img[0])
    np.save('./data/encoded_data_0_5',encoded_data)
    
if __name__=='__main__':
    if LOAD:
        generate_encoded_data()
        #eval_model()
    else:
        train_model()
