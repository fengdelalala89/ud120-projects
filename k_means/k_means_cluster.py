#!/usr/bin/python 
# -*- coding: utf-8 -*-
""" 
    Skeleton code for k-means clustering mini-project.
"""




import pickle
import numpy
import matplotlib.pyplot as plt
import sys
sys.path.append("../tools/")
from feature_format import featureFormat, targetFeatureSplit



# 画出散点图
##enumerate(sequence, [start=0])：python的内置 函数。用于将一个可遍历的数据对象(如列表、元组或字符串)组合为一个索引序列，同时列出数据和数据下标
def Draw(pred, features, poi, mark_poi=False, name="image.png", f1_name="feature 1", f2_name="feature 2"):
    """ some plotting code designed to help you visualize your clusters """

    ### plot each cluster with a different color--add more colors for
    ### drawing more than five clusters
    colors = ["b", "c", "k", "m", "g"]
    for ii, pp in enumerate(pred):
        plt.scatter(features[ii][0], features[ii][1], color = colors[pred[ii]])

    ### if you like, place red stars over points that are POIs (just for funsies)
    if mark_poi:
        for ii, pp in enumerate(pred):
            if poi[ii]:
                plt.scatter(features[ii][0], features[ii][1], color="r", marker="*")
    plt.xlabel(f1_name)
    plt.ylabel(f2_name)
    plt.savefig(name)
    plt.show()


#pickle.load(file)：反序列化对象。将文件中的数据解析为一个Python对象。
### load in the dict of dicts containing all the data on each person in the dataset
data_dict = pickle.load( open("../final_project/final_project_dataset.pkl", "r") )
### there's an outlier--remove it! 
data_dict.pop("TOTAL", 0)  #删除离群值


### the input features we want to use 
### can be any key in the person-level dictionary (salary, director_fees, etc.) 
feature_1 = "salary"
feature_2 = "exercised_stock_options"
#feature_3 = "total_payments"
poi  = "poi"
features_list = [poi, feature_1, feature_2 ]
data = featureFormat(data_dict, features_list )
poi, finance_features = targetFeatureSplit( data )


### in the "clustering with 3 features" part of the mini-project,
### you'll want to change this line to 
### for f1, f2, _ in finance_features:
### (as it's currently written, the line below assumes 2 features)
#for f1, f2,f3 in finance_features:
for f1, f2 in finance_features:
    plt.scatter( f1, f2 )   #scatter在这里针对的应该是两个变量
plt.show()

##特征缩放
from sklearn.preprocessing import MinMaxScaler
def scaler(feature_train):
    MMS = MinMaxScaler()
    a = MMS.fit_transform(feature_train)
    return a


### cluster here; create predictions of the cluster labels
### for the data and store them to a list called pred
##聚类
from sklearn.cluster import KMeans
#pred = KMeans(n_clusters=2 ).fit_predict(finance_features)  #部署聚类：创建拟合器 然后fit 然后predict
kmeans = KMeans(n_clusters=2).fit(scaler(finance_features))
pred = kmeans.labels_
#print (type(pred),pred)


### rename the "name" parameter when you change the number of features
### so that the figure gets saved to a different file
try:
    Draw(pred, finance_features, poi, mark_poi=False, name="clusters.pdf", f1_name=feature_1, f2_name=feature_2)
except NameError:
    print "no predictions object named pred found, no clusters to plot"


import numpy as np
##计算薪酬范围
# array1 = numpy.array(finance_features)
# m_f1 = max(array1[:,0])
# print("max salary:",m_f1)
# #for f1,f2,f3 in array1:
# for f1,f2 in array1:
#     if f1 > 0:
#         m_f1 = min(f1, m_f1)
# print("min salary:",m_f1)

salarylist=[]
for item in data_dict:
    stock = data_dict[item]['salary']
    if stock != 'NaN':
        salarylist.append(stock)
salarylist = np.array(salarylist)
print "max:",np.max(salarylist)
print "min:",np.min(salarylist)





##计算股权范围
# array2 = numpy.array(finance_features)
# m_f2 = max(array2[:,1])
# print("max exercised_stock_options:" , m_f2)
# #for f1,f2,f3 in array2:
# for f1,f2 in array2:
#     if f2>0:
#         m_f2 = min(f2, m_f2)
# print("min exercised_stock_options:" , m_f2)


stocklist=[]
for item in data_dict:
    stock = data_dict[item]['exercised_stock_options']
    if stock != 'NaN':
        stocklist.append(stock)
stocklist = np.array(stocklist)
print "max:",np.max(stocklist)
print "min:",np.min(stocklist)


#计算重缩放特征
#公式 x' = (x- min)/(max-min)
#计算原值为 200,000 的“salary”特征在尺度变换后的值会是什么，
# 以及原值为 100 万美元的“exercised_stock_options”特征在尺度变换后的值会是什么？
print "计算重缩放特征"
print "salary:",(200000-min(salarylist))*1.0/(max(salarylist)-min(salarylist))
print "exercised_stock_options:", (1000000-min(stocklist))*1.0/(max(stocklist)-min(stocklist))




# from sklearn.preprocessing import MinMaxScaler
# import numpy
# #这里numpy数组中的是特征，因为此处特征只有一个，所以看起来是这样的
# #因为这里应该作为一个浮点数进行运算，所以数字后面要加.
# # weights = numpy.array([[115.],[140.],[175.]])
# # scaler = MinMaxScaler()
# # rescaled_weight = scaler.fit_transform(weights)
# # print rescaled_weight