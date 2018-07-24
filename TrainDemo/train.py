# -*- coding: utf-8 -*-
"""
Created on Wed Jul 18 17:37:13 2018

@author: mayn
"""

import numpy as np
import tensorflow as tf
import os

# sigmoid function
def nonlin(x,deriv=False):
    if(deriv==True):
        return x*(1-x)
    return 1/(1+np.exp(-x))

'''
# input dataset
X = np.array([[0,0,-1],
              [0,0,1],
              [0, 1, -1],
              [0, 1, 0], 
              [0, 1, 1],
              [0, 3, -1], 
              [0, 3, 0], 
              [0, 3, 1], 
              [0, 2, -1], 
              [0, 2, 1],
              [0, 2, 0]])
# output dataset 
Y = np.array([[1, 3, 2, 2, 2, 2, 2, 2, 1, 3, 1]]).T

'''

def train_one_door_one_window():
    '''
        输入： 门位置，窗位置，门在墙上的相对位置; 
               (1) 位置表示墙的编号:门所在的墙为0号墙，顺时针旋转共4面墙
               (2) 门在墙上相对位置：0表示在墙的正中央，左为正，右为负
        输出： 床头所靠的墙
    '''
    X = [ [0, 0,-1],
          [0, 0, 0],
          [0, 0, 1],
          [0, 1,-1],
          [0, 1, 0], 
          [0, 1, 1],
          [0, 3,-1], 
          [0, 3, 0], 
          [0, 3, 1], 
          [0, 2,-1], 
          [0, 2, 1],
          [0, 2, 0],
          [0, 0, -0.8],
          [0, 0, -0.9],
          [0, 0, -0.7],
          [0, 0, -0.6]]
    '''
    Y = [[1], [2], [3], [2], [2], [2], [2], [2], [2], [1], [3], [1],
         [1], [1], [1], [1]]'''
    
    Y = [[2], [2], [2], [2], [2], [2], [2], [2], [2], [2], [2], [2],
         [2], [2], [2], [2]]
    
    tf_x = tf.placeholder(tf.float32, [None,3])     # input x
    tf_y = tf.placeholder(tf.float32, [None,1])     # input y
    
    # neural network layers
    l1 = tf.layers.dense(tf_x, 15, tf.nn.relu)          # hidden layer
    output = tf.layers.dense(l1, 1)                     # output layer
    
    loss = tf.losses.mean_squared_error(tf_y, output)   # compute cost
    optimizer = tf.train.GradientDescentOptimizer(learning_rate=0.1)
    train_op = optimizer.minimize(loss)
    
    sess = tf.Session()                                 # control training and others
    sess.run(tf.global_variables_initializer())         # initialize var in graph
    
    for step in range(150):
        # train and net output
        _, l, pred = sess.run([train_op, loss, output], {tf_x: X, tf_y: Y})
        if step % 10 == 0:
            print('loss is: ' + str(l))
            # print('prediction is:' + str(pred))
            
    x_pred = [[0, 0,-1],
              [0, 0, 1],
              [0, 1,-1],
              [0, 1, 0], 
              [0, 1, 1],
              [0, 3,-1], 
              [0, 3, 0], 
              [0, 3, 1], 
              [0, 2,-1], 
              [0, 2, 1],
              [0, 2, 0],
              [0, 0, -0.9],
              [0, 0, -0.4],
              [0, 0, -0.5]]
    
    
    output_pred = sess.run(output,{tf_x:x_pred})
    print('input is:' + str(x_pred[0][:]))
    print('output is:' + str(output_pred[0][0]))
    print('input is:' + str(x_pred))
    print('output is:' + str(output_pred))
    weights1 = tf.get_default_graph().get_tensor_by_name(os.path.split(l1.name)[0] + '/kernel:0')
    weights2 = tf.get_default_graph().get_tensor_by_name(os.path.split(output.name)[0] + '/kernel:0')
    #print(sess.run(weights1), sess.run(weights2))
    a = sess.run(weights1)
    a1 = a[2] * (-1.0)
    b = sess.run(weights2)
    for i in range(len(a1)):
        if a1[i] < 0:
            a1[i] = 0
    b1 = []
    for i in range(len(b)):
        r = a1[i] + b[i]
        b1.append(r)
    print(b1, sum(b1))
    
train_one_door_one_window()