#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Aug 12 22:22:59 2018

@author: gongwanting
"""
import pandas as pd
import numpy as np 
import matplotlib.pyplot as plt

datapath='/Users/gongwanting/Desktop/'
original_data=pd.read_excel(datapath+'奇子创投.xlsx',names=['姓名','身份证号码','申请时间','电话','Y'])
short_v1=pd.read_excel(datapath+'奇子创投测试结果.xlsx',sheetname='信用雷达场景版_小额现金分期测试结果',skiprows=2)
short_v1std=short_v1.iloc[:,0:3]
original_short1=pd.merge(original_data,short_v1std,how='left',left_on=['身份证号码','姓名'],right_on=['身份证号','姓名'])
original_short1['小额现金分期场景行为分'].fillna(0,inplace=True)
#分数分布对比图
original_short1['小额现金分期场景行为分'].hist(bins=50)

#计算KS
score_quan=original_short1[['小额现金分期场景行为分','Y']].quantile(np.linspace(0,1,20)[1:-1])
good0=original_short1[original_short1['Y']==0].shape[0]
bad0=original_short1[original_short1['Y']==1].shape[0]
print ('总的逾期人数为:%s, 总的正常还款人数为：%s' % ([bad0][0],[good0][0]))
good=[]
bad=[]


#针对每个分计算good_rate，bad_rate，good_cnt，bad_cnt，cum_good_cnt，cum_bad
 #将分数保存为分组模式
bins=list(np.arange(300,1000,20))
bins.append(-1)
bins.append(0)
bins.sort()
original_short1['bins']=pd.cut(original_short1['小额现金分期场景行为分'],bins)
grouped=original_short1['小额现金分期场景行为分'].groupby([original_short1['bins'],original_short1['Y']]).count().unstack()
grouped[1].fillna(1,inplace=True)
sum_good_cnt=grouped[0].sum()
sum_bad_cnt=int(grouped[1].sum())
grouped['pct_total']=grouped[0]+grouped[1]
grouped['total_rate']=grouped['pct_total']/(sum_good_cnt+sum_bad_cnt)
grouped['total_rate'].plot()
#好坏比
grouped['good_rate']=grouped[0]/sum_good_cnt
grouped['bad_rate']=grouped[1]/sum_bad_cnt
#odds
grouped['odds']=grouped['good_rate']/grouped['bad_rate']
#woe
grouped['woe']=np.log(grouped['bad_rate']/grouped['good_rate'])
#IV
grouped['iv']=sum((grouped['bad_rate']-grouped['good_rate'])*grouped['woe'])-sum((grouped['bad_rate'][-3:]-grouped['good_rate'][-3:])*grouped['woe'][-3:])
#好坏累积比
grouped['cum_good_rate']=grouped[0].cumsum()/sum_good_cnt
grouped['cum_bad_rate']=grouped[1].cumsum()/sum_bad_cnt
#KS 
grouped['ks']=max(grouped['cum_bad_rate']-grouped['cum_good_rate'])
grouped.to_csv(datapath+'analysis_template1.csv')


for i in ['小额现金分期场景行为分']:
    good1=[];bad1=[] 
    for j in range(score_quan.shape[0]):         
        good1.append(original_short1[(original_short1[i]<=score_quan[i].iloc[j])&(original_short1['Y']==0)].shape[0]/good0)
        bad1.append(original_short1[(original_short1[i]<=score_quan[i].iloc[j])&(original_short1['Y']==1)].shape[0]/bad0)
    good.append(good1)
    bad.append(bad1)
    bad_good=abs(np.array(bad1)-np.array(good1))
    #对分数十分位点的确定，索引对应对应的十分位分数
    quan_index=list(score_quan.index)
    ks_point=max(bad_good)
    ks_point_index=quan_index[np.where(bad_good==ks_point)[0][0]]
    
    plt.figure()
    plt.xlim([0,1])
    plt.ylim([0,1])
    plt.subplot(211)
    plt.plot(list(score_quan.index),good1,label='good')
    plt.plot(list(score_quan.index),bad1,label='bad')
    plt.plot(quan_index,bad_good,label='bad-good')
    #可视化KS点距x轴的距离
    plt.plot([ks_point_index,ks_point_index],[0,ks_point],'-.',c='grey')
    #画出KS点
    plt.scatter(ks_point_index,ks_point)
    plt.text(0.4,0.3,'KS: %s'%round(ks_point,3))
    plt.legend(loc='best')
    plt.title('KS Curve of short')
    plt.ylabel('percentage')
    plt.xlabel('quantile')   
    plt.subplot(212)
    plt.plot(quan_index, bad_good,'r-', lw=2)
    plt.savefig(datapath+'小额现金分期场景行为分KS图1.png') 
    plt.show()
    plt.close()
    
#绘制两个分数KS曲线图的对比，画在一张图的两个部分
        
#绘制ROC曲线
def score_roc(df, score_name, tag_name):
    from sklearn.metrics import roc_curve, auc
    df.loc[df[tag_name]==1, 'label'] = 0
    df.loc[df.label!=0, 'label'] = 1
    df[score_name] = (df[score_name]-300)/700
    false_positive_rate, true_positive_rate, thresholds = roc_curve(df.label, df[score_name])
    roc_auc = auc(false_positive_rate, true_positive_rate)
    plt.title(' Receiver Operating Characteristic')
    plt.plot(false_positive_rate, true_positive_rate, 'b', label='AUC = %0.2f'% roc_auc)
    plt.legend(loc='lower right')
    plt.plot([0,1],[0,1],'r--')
    plt.xlim([-0.1,1.2])
    plt.ylim([-0.1,1.2])
    plt.ylabel('True Positive Rate')
    plt.xlabel('False Positive Rate')
    plt.show() 
score_roc(original_short1,'小额现金分期场景行为分','Y')   












