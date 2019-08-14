#大致认为从50变化到250

import cv2
import matplotlib.pyplot as plt
import numpy as np 
import random
import os 

imgs = os.listdir('data')
imgs = [i for i in imgs if (('.jpg' in i) and ('train' not in  i))]
posimg = ['./data/'+i for i in imgs if '_1' in i]
negimg = ['./data/'+i for i in imgs if '_0' in i]
win_size = (32,32)
block_size = (16,16)
block_stride = (8,8)
cell_size = (8,8)
num_bins = 9
img_avg = 120
hog = cv2.HOGDescriptor(win_size,block_size,block_stride,cell_size,num_bins)

random.seed(42)

def gethog(imgs):
    X = []
    for filename in random.sample(imgs,len(imgs)):
        img = cv2.imread(filename)
        if img is None:
            print('Could not find image %s'%filename)
            continue
        X.append(hog.compute(img,(120,120)))
    return X
    #opencv需要特征矩阵包含32位浮点数，而且目标标签是32位的整数。

X_pos = gethog(posimg)
X_pos = np.array(X_pos,dtype = np.float32)
y_pos = np.ones(X_pos.shape[0],dtype = np.int32)

X_neg = gethog(negimg)
X_neg = np.array(X_neg,dtype = np.float32)
y_neg = -np.ones(X_neg.shape[0],dtype = np.int32)

#合并 数据集
X = np.concatenate((X_pos,X_neg))
y = np.concatenate((y_pos,y_neg))
from sklearn import model_selection as ms
X_train,X_test,y_train,y_test = ms.train_test_split(X,y,test_size = 0.2,random_state = 42)
#实现支持向量机
def train_svm(X_train,y_train):
    svm = cv2.ml.SVM_create()
    svm.setKernel(cv2.ml.SVM_LINEAR)
    svm.train(X_train,cv2.ml.ROW_SAMPLE,y_train)
    return svm

def score_svm(svm,X,y):
    from sklearn import metrics
    _,y_pred = svm.predict(X)
    return metrics.accuracy_score(y,y_pred)

svm = train_svm(X_train,y_train)
sc = score_svm(svm,X_train,y_train)
sc = score_svm(svm,X_test,y_test)

#模型自举，其实相当于当时那个超新星的说的用于反复训练的方法
score_train = []
score_test = []
while True:
    svm = train_svm(X_train,y_train)
    score_train.append(score_svm(svm,X_train,y_train))
    score_test.append(score_svm(svm,X_test,y_test))
    #找到假正图片，当然，没有则结束
    _,y_pred = svm.predict(X_test)
    
    false_pos = np.logical_and((y_test.ravel()==-1),(y_pred.ravel()==1))
    false_neg = np.logical_and((y_test.ravel()== 1),(y_pred.ravel()==-1))
    if not (np.any(false_pos) or np.any(false_neg)):#非空返回True，空返回False，None返回None
        print('no more false positives:done ')
        break
    X_train = np.concatenate((X_train,X_test[false_pos,:]),axis = 0)
    X_train = np.concatenate((X_train,X_test[false_neg,:]),axis = 0)
    y_train = np.concatenate((y_train,y_test[false_pos]),axis = 0)
    y_train = np.concatenate((y_train,y_test[false_neg]),axis = 0)

print(score_train)
print(score_test)


img_test = cv2.imread('./rawdata/train_0.jpg')
#检测函数
rho,rho_1,rho_2 = svm.getDecisionFunction(0)
sv = svm.getSupportVectors()
hog.setSVMDetector(np.append(sv.ravel(),rho))
print('已设置完svm')
found_raw = hog.detectMultiScale(img_test,scale = 1.1)
print('已完成检测')
