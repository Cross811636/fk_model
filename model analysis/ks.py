# -*- coding: utf-8 -*-
"""
Created on Tue Jul 17 10:39:20 2018

@author: XY100075
"""

import pandas as pd 
import numpy as np
import matplotlib.pyplot as plt

data=pd.read_csv('cdq_yqreal_sample_qbdj1_20180719_ultrashort_ks.csv',header=None,names=['id_card_no','name','loan_day','ultra_short','target'])
score_quan=data[['ultra_short','target']].quantile(np.linspace(0,1,51)[1:-1])
#score_quan.columns=['id_card_no','name','loan_day','ultra_short','target']


good0=data[data['target']==0].shape[0]
bad0=data[data['target']==1].shape[0]
good=[]
bad=[]

for i in ['ultra_short']:
    good1=[];bad1=[]
    for j in range(score_quan.shape[0]):
        good1.append(data[(data[i]<=score_quan[i].iloc[j])&(data['target']==0)].shape[0]/good0)
        bad1.append(data[(data[i]<=score_quan[i].iloc[j])&(data['target']==1)].shape[0]/bad0)

    good.append(good1)
    bad.append(bad1)
    plt.figure()
    plt.plot(list(score_quan.index),good1)
    plt.plot(list(score_quan.index),bad1)
    plt.text(0.2,0.8,max(abs(np.array(good1)-np.array(bad1))))
    plt.ylabel('percentage')
    plt.xlabel('quantile')
    plt.savefig(i[2:]) 
    plt.close()
