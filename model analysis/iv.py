# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 15:32:31 2018

@author: XY100075
"""

import pandas as pd
import numpy as np

def DATA_BIN_SCREEN(data,bin_num):
    data_hist=[];bins=[];flag=0
    for i in data.columns[:-1]:
        bins.append([])
        data_hist.append(data[i][data[i]>-1].value_counts().sort_index())
        if data_hist[flag].size<bin_num:
            for k in range(data_hist[flag].size):
                bins[flag].append([])
                bins[flag][k].append(data_hist[flag].index[k])
            print(i)
            print(data_hist[flag])
            flag+=1
            continue
        bin_count=int(data_hist[flag].sum()/bin_num)
        print(i)
        bin_now=0;bin_count_now=0;bins[flag].append([])
        for j in range(data_hist[flag].size):
            bins[flag][bin_now].append(data_hist[flag].index[j])
            bin_count_now+=data_hist[flag].iloc[j]
            if j<(data_hist[flag].size-1):
                if (bin_count_now+data_hist[flag].iloc[j+1])>bin_count:
                    print('[',bins[flag][bin_now][0],',',bins[flag][bin_now][-1],'] ',bin_count_now)
                    bin_count_now=0
                    bin_now+=1
                    bins[flag].append([])
            else:
               print('[',bins[flag][bin_now][0],',',bins[flag][bin_now][-1],'] ',bin_count_now)
        flag+=1
    return data_hist,bins

def DATA_BIN_LOG(data,bin_num):
    data_hist=[];bins=[];bins_count=[];flag=0
    for i in data.columns[:-1]:
        bins.append([]);bins_count.append([])
        data_hist.append(data[i][data[i]>-1].value_counts().sort_index())
        if data_hist[flag].size<bin_num:
            for k in range(data_hist[flag].size):
                bins[flag].append([])
                bins[flag][k].append(data_hist[flag].index[k]);bins_count[flag].append(data_hist[flag].iloc[k])
            flag+=1
            continue
        bin_count=int(data_hist[flag].sum()/bin_num)
        bin_now=0;bin_count_now=0;bins[flag].append([])
        for j in range(data_hist[flag].size):
            bins[flag][bin_now].append(data_hist[flag].index[j])
            bin_count_now+=data_hist[flag].iloc[j]
            if j<(data_hist[flag].size-1):
                if (bin_count_now+data_hist[flag].iloc[j+1])>bin_count:
                    bins_count[flag].append(bin_count_now)
                    bin_count_now=0
                    bin_now+=1
                    bins[flag].append([])
            else:
               bins_count[flag].append(bin_count_now)
        flag+=1
    return data_hist,bins,bins_count

def DATA_IV(data,bins):
    good_bad=[[[] for i in range(data.shape[1])],[[] for i in range(data.shape[1])]]
    woe=[[] for i in range(data.shape[1])]
    ivi=[[] for i in range(data.shape[1])]
    iv=[]
    flag=0
    for i in data.columns[:-1]:
        goodt=data[(data[i]>-1)&(data.iloc[:,-1]==0)].shape[0]
        badt=data[(data[i]>-1)&(data.iloc[:,-1]==1)].shape[0]
        for j in range(len(bins[flag])):
            good_bad[0][flag].append(data.loc[data[i].isin(bins[flag][j])&data.iloc[:,-1].isin([0])].shape[0])
            good_bad[1][flag].append(data.loc[data[i].isin(bins[flag][j])&data.iloc[:,-1].isin([1])].shape[0])
            if good_bad[0][flag][j]==0:
                good_bad[0][flag][j]+=1 
            if good_bad[1][flag][j]==0:
                good_bad[1][flag][j]+=1
            woe[flag].append(np.log((good_bad[0][flag][j]/goodt)/(good_bad[1][flag][j]/badt)))
            ivi[flag].append((good_bad[0][flag][j]/goodt-good_bad[1][flag][j]/badt)*woe[flag][j])
        iv.append(np.sum(ivi[flag]))
        flag+=1
    return iv,good_bad

def WRITE_BIN_IV(filename,data,bins,good_bad,bins_count,iv):
    counts=data.shape[0]
    with open(filename,'w') as f:
        for i in range(len(iv)):
            counts_eff=data.iloc[:,i][data.iloc[:,i]>-1].shape[0]
            f.write(data.columns[i]+'  '+str(round(counts_eff/counts*100,2))+'%  '+str(round(iv[i],4))+'\n')
            for j in range(len(bins[i])):
                f.write('['+str(bins[i][j][0])+','+str(bins[i][j][-1])+']  '+str(good_bad[0][i][j])+' '+str(good_bad[1][i][j])+' ' +str(bins_count[i][j])+'  '+str(round(bins_count[i][j]/counts_eff*100,2))+'%\n')
    f.close()
    
def DATA_COMBINE_PASS_OVERDUE(data,data_corr,data_hist,iv,iv_score,corr_score):
    iv_high=np.where(np.array(iv)>iv_score)[0]
    print('高iv字段:')
    for i in range(len(iv_high)):
        print(data.columns[iv_high[i]],iv[iv_high[i]])
    po=[];combination_no=[];
    for i in range(len(iv_high)-1):
        for j in range(i+1,len(iv_high)):
            print(data.columns[iv_high[i]],data.columns[iv_high[j]],'变量相关性:',data_corr.iloc[iv_high[i],iv_high[j]])
            if abs(data_corr.iloc[iv_high[i],iv_high[j]])<corr_score:
                print('选择组合')
                combination_no.append([iv_high[i],iv_high[j]])
                pass_overdue=np.zeros((2,len(data_hist[iv_high[i]]),len(data_hist[iv_high[j]])))
                target1count=data[data['target'].isin([1])].shape[0]
                for k in range(pass_overdue.shape[1]):
                    for l in range(pass_overdue.shape[2]):
                        pass_overdue[0,k,l]=data.loc[(data.iloc[:,iv_high[i]]<data_hist[iv_high[i]].index[k])&(data.iloc[:,iv_high[j]]<data_hist[iv_high[j]].index[l])].shape[0]/data.shape[0]
                        pass_overdue[1,k,l]=data.loc[(data.iloc[:,iv_high[i]]<data_hist[iv_high[i]].index[k])&(data.iloc[:,iv_high[j]]<data_hist[iv_high[j]].index[l])&data['target'].isin([1])].shape[0]/target1count
                po.append(pass_overdue)
            else:
                print('不选择组合')
    return combination_no,po

def DATA_COMBINE(data,data_corr,iv,iv_score,corr_score):
    iv_high=np.where(np.array(iv)>iv_score)[0]
    print('高iv字段:')
    for i in range(len(iv_high)):
        print(data.columns[iv_high[i]],iv[iv_high[i]])
    combination_no=[];
    for i in range(len(iv_high)-1):
        for j in range(i+1,len(iv_high)):
            print(data.columns[iv_high[i]],data.columns[iv_high[j]],'变量相关性:',data_corr.iloc[iv_high[i],iv_high[j]])
            if abs(data_corr.iloc[iv_high[i],iv_high[j]])<corr_score:
                print('选择组合')
                combination_no.append([iv_high[i],iv_high[j]])
            else:
                print('不选择组合')
    return combination_no

def DATA_DENY_RULE(data,iv,corr_score):
    iv_sort=pd.Series(data.columns[:-1],index=iv).sort_index(ascending=False)
    combination=[];
    flag=0
    for i in range(iv_sort.shape[0]-1):
        if (data[data[iv_sort.iloc[i]]>-1].shape[0]/data.shape[0])>0.4:
            for j in range(i+1,iv_sort.shape[0]):
                if (data[data[iv_sort.iloc[j]]>-1].shape[0]/data.shape[0])>0.4:
                    if abs(data[[iv_sort.iloc[i],iv_sort.iloc[j]]].corr().iloc[0,1])<corr_score:
                        combination.append(iv_sort.iloc[i])
                        combination.append(iv_sort.iloc[j])
                        flag+=1
                    if flag==3:
                        break
            if flag==3:
                break
    return combination

def PASS_OVERDUE(data,combination,pass_lift):
    po=[];deny_rule=[]
    sample_count=data.shape[0]
    overdue_count=data[data['target']==1].shape[0]
    for i in range(3):
        data_dr_hist=[];deny_rule0=[]
        data_dr=data[[combination[i*2],combination[i*2+1],'target']]
        data_dr_hist.append(data_dr[combination[i*2]].value_counts().sort_index())
        data_dr_hist.append(data_dr[combination[i*2+1]].value_counts().sort_index())
        rnum=len(data_dr_hist[0])
        cnum=len(data_dr_hist[1])
        pass_overdue=np.zeros((2,rnum,cnum))
        pass_overdue_uniq=np.ones((rnum,cnum))
        for j in range(rnum):
            for k in range(cnum):
                data_dr0=data_dr[(data_dr.iloc[:,0]<=data_dr_hist[0].index[j])&(data_dr.iloc[:,1]<=data_dr_hist[1].index[k])]
                sample_dr=data_dr0.shape[0]
                pass_overdue[0,j,k]=sample_dr/sample_count
                if sample_count!=sample_dr:
                    pass_overdue[1,j,k]=(overdue_count-data_dr0.loc[data['target'].isin([1])].shape[0])/(sample_count-sample_dr)
        for i in range(2):
            pass_overdue_uniq[1:]=pass_overdue[i,1:]-pass_overdue[i,:-1]
            pass_overdue[i][pass_overdue_uniq==0]=1
            pass_overdue_uniq[:]=1
            pass_overdue_uniq[:,1:]=pass_overdue[i,:,1:]-pass_overdue[i,:,:-1]
            pass_overdue[i][pass_overdue_uniq==0]=1
            pass_overdue_uniq[:]=1
        po.append(pass_overdue)
        deny_rule_index=np.where(pass_overdue[0]==np.min(pass_overdue[0][pass_overdue[1]<=0.0828]))#pass_lift*overdue_count/sample_count
        for l in range(len(deny_rule_index[0])):
            deny_rule0.append([data_dr_hist[0].index[deny_rule_index[0][l]],data_dr_hist[1].index[deny_rule_index[1][l]],pass_overdue[0,deny_rule_index[0][l],deny_rule_index[1][l]],pass_overdue[1,deny_rule_index[0][l],deny_rule_index[1][l]]])
        deny_rule.append(deny_rule0)
    return po,deny_rule,deny_rule_index
        