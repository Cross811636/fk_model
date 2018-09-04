# -*- coding: utf-8 -*-
"""
Created on Thu Apr 19 09:33:57 2018

@author: XY100075
"""

import pandas as pd
import numpy as np

def MODEL_EVALUATION(data):
    data_hist=[];p_rate=[];pv_plus=[];TPR=[];FPR=[]#;lift=[];nTNR=[]
    flag=0
    for i in data.columns[:-1]:
        data0=data[[i,'target']][data[i]>-1]
        data_hist.append(data0[i].value_counts().sort_index())
        #data_hist是将data0的每一列非重复元素进行计数并进行排序
        p_count=[];pv_plus0=[];fx0=[];gx0=[];KS0=[]#;lift0=[];nTNR0=[]
        
        for j in range(data_hist[flag].shape[0]):
            P=data0[data0['target'].isin([0])].shape[0]
            N=data0[data0['target'].isin([1])].shape[0]
            data01=data0[data0[i]>=data_hist[flag].index[j]]
            data02=data01[data01['target'].isin([1])]
            TP=data01[data01['target'].isin([0])].shape[0]
            FP=data02.shape[0]
            TN=data02[data02[i]<data_hist[flag].index[j]].shape[0]
            #FN=data.loc[(data[i]>-1)&(data[i]<data_hist[flag].index[j])&(data['target'].isin([0]))].shape[0]
            p_count0=data01.shape[0]
            '''
            g1=FN/P;b1=TN/N;g2=TP/P;b2=FPm/N
            if b1==0:
                b1+=1
            if b2==0:
                b2+=1
            if g1==0:
                g1+=1
            if g2==0:
                g2+=1
            iv_value=(g1-b1)*np.log(g1/b1)+(g2-b2)*np.log(g2/b2)
            if 0>iv_value or iv_value>1:
                iv_value=0
            iv0.append(iv_value)
            '''
            pv_plus0.append(TP/p_count0)
            fx0.append(TP/P)
            gx0.append(FP/N)
            #lift0.append(pv_plus0[j]/(P/data0.shape[0]))
            #nTNR0.append(1-(TN/N))
            p_count.append(p_count0/data0.shape[0])
        p_rate.append(p_count)
        pv_plus.append(pv_plus0)
        TPR.append(fx0)
        FPR.append(gx0)
        #lift.append(lift0)
        #nTNR.append(nTNR0)
        flag+=1
    return p_rate,pv_plus,TPR,FPR

def WRITE_GAIN_KS(filename,p_rate,pv_plus,TPR,FPR):
    #输入文件名，p_rate，pv_plus，TPR，FPR等参数
    with open(filename,'w') as f:
        #使用whith open打开文件
        for i in range(len(p_rate)):
            #便利每一个P_rate
            f.write(str(p_rate[i])+'\n')
            #写入对应的参数
            f.write(str(pv_plus[i])+'\n')
            f.write(str(TPR[i])+'\n')
            f.write(str(FPR[i])+'\n')
    f.close()
'''
for i in range(len(p_rate)):
    fig=plt.figure()
    plt.plot([0,1],[0,1],c='blue',label='random')
    plt.plot(nTNR[i],TPR[i],c='red',label='model')
    plt.xlabel('Sensitivity')
    plt.ylabel('Specificity')
    plt.legend(loc='lower right')
    plt.savefig('D:/kaka/model/ROC/'+data.columns[i]+'_ROC.JPG')
    plt.close()
'''