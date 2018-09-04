# -*- coding: utf-8 -*-
"""
Created on Tue Apr 17 15:32:31 2018

@author: XY100075
"""

import pandas as pd
import numpy as np
import copy
from matplotlib.gridspec import GridSpec
import matplotlib.pyplot as plt

def READ_DATA(filename):
#    filename = '/Users/gongwanting/Desktop/code/sample/sample'
    data_target=pd.read_excel(filename+'_target.xlsx',names=['名字','身份证号','审批日期','target'])
    data_target['审批日期']=pd.to_datetime(data_target['审批日期'])
    data1=pd.read_excel(filename+'_全景雷达.xlsx',sheetname='申请雷达回溯测试结果',skiprows=[0,1])
    data1['回溯时间']=pd.to_datetime(data1['回溯时间'])
    data=pd.merge(data_target,data1,how='left',left_on=['身份证号','审批日期'],right_on=['身份证','回溯时间'])
    data.drop(['姓名','身份证','回溯时间'],axis=1,inplace=True)
    data2=pd.read_excel(filename+'_全景雷达.xlsx',sheetname='行为雷达回溯测试结果',skiprows=[0,1])
    data2['回溯时间']=pd.to_datetime(data2['回溯时间'])
    data=pd.merge(data,data2,how='left',left_on=['身份证号','审批日期'],right_on=['身份证','回溯时间'])
    data.drop(['姓名','身份证','回溯时间'],axis=1,inplace=True)
    data3=pd.read_excel(filename+'_全景雷达.xlsx',sheetname='信用现状回溯测试结果',skiprows=[0,1])
    print(data3.columns)
    data3['回溯时间']=pd.to_datetime(data3['回溯时间'])
    data=pd.merge(data,data3,how='left',left_on=['身份证号','审批日期'],right_on=['身份证','回溯时间'])
    data.drop(['姓名','身份证','回溯时间'],axis=1,inplace=True)
    data4=pd.read_excel(filename+'_负面探针.xlsx',sheetname='负面洗白回溯测试结果',skiprows=[0,1,2])
    data4['探查结论'].replace({'空值未知':-1,'无法确认':0,'建议洗白':1},inplace=True)
    data4['探查明细'].replace({'-':-1,'逾期又还款':0,'正常履约':1},inplace=True)
    data4['最大履约金额'].replace({'-':np.nan,'>1000000':1000000-1000001},inplace=True)
    data4['最大履约金额']=data4['最大履约金额'].str.split('-',expand=True)[1]
    data4['回溯时间']=pd.to_datetime(data4['回溯时间'])
    data=pd.merge(data,data4,how='left',left_on=['身份证号','审批日期'],right_on=['身份证号','回溯时间'])
    data.drop(['姓名','回溯时间'],axis=1,inplace=True)
    data5=pd.read_excel(filename+'_负面探针.xlsx',sheetname='负面拉黑回溯测试结果',skiprows=[0,1,2])
    data5['探查结论'].replace({'空值未知':-1,'无法确认':0,'建议拉黑':1},inplace=True)
    data5['探查明细'].replace({'-':1,'逾期未还款':0},inplace=True)
    data5['最大逾期金额'].replace({'-':np.nan,'>1000000':1000000-1000001},inplace=True)
    data5['最大逾期金额']=data5['最大逾期金额'].str.split('-',expand=True)[1]
    data5['最长逾期天数'].replace({'-':-1,'1-15':15,'16-30':30,'31-60':60,'61-90':90,'91-120':120,'121-150':150,'151-180':180,'>180':181},inplace=True)
    data5['回溯时间']=pd.to_datetime(data5['回溯时间'])
    data=pd.merge(data,data5,how='left',left_on=['身份证号','审批日期'],right_on=['身份证号','回溯时间'])
    data.drop(['姓名','回溯时间'],axis=1,inplace=True)
    data6=pd.read_excel(filename+'_共债档案.xlsx',sheetname=1,skiprows=[0,1,2],usecols=[0,1,2,7,8,9,10])
    data6['共债订单金额1'].replace({'0':'0-0'},inplace=True)
    data6['共债订单金额1']=data6['共债订单金额1'].str.split('-',expand=True)[1]
    data6['回溯时间']=pd.to_datetime(data6['回溯时间'])
    data=pd.merge(data,data6,how='left',left_on=['身份证号','审批日期'],right_on=['身份证号','回溯时间']) 
    data.drop(['姓名','回溯时间'],axis=1,inplace=True)
    data.replace({'-':np.nan},inplace=True)
    data['最近查询时间']=(pd.to_datetime(data['审批日期'])-pd.to_datetime(data['最近查询时间'])).astype('timedelta64[D]')
    data['最近一次贷款时间']=(pd.to_datetime(data['审批日期'])-pd.to_datetime(data['最近一次贷款时间'])).astype('timedelta64[D]')
    data['最近履约时间']=(pd.to_datetime(data['审批日期'])-pd.to_datetime(data['最近履约时间'])).astype('timedelta64[D]')
    data['最近逾期时间']=(pd.to_datetime(data['审批日期'])-pd.to_datetime(data['最近逾期时间'])).astype('timedelta64[D]')
    data['共债统计时间范围1']=(pd.to_datetime(data['审批日期'])-pd.to_datetime(data['共债统计时间范围1'])).astype('timedelta64[M]')
    
    #小额现金分期
    data_newscore1=pd.read_excel('sample_小额现金分期.xlsx',sheetname ='信用雷达场景版_小额现金分期回溯测试结果',skiprows=[0,1],use_col=[0,1,2,3] )
    data_newscore1=data_newscore1.iloc[:,:4]
    data_newscore1.columns=['xingming','shenfenzheng','shijian','short']
    data_newscore1['shijian']=pd.to_datetime(data_newscore1['shijian'])
    data=pd.merge(data,data_newscore1,how='left',left_on=['身份证号','审批日期'],right_on=['shenfenzheng','shijian'])
    data.drop(['shenfenzheng','xingming','shijian'],axis=1,inplace=True)
    
    #传统小额贷款
    data_newscore2=pd.read_excel('sample__传统小额贷款（回溯）.xlsx',sheetname ='信用雷达场景版_传统小额贷款回溯测试结果',skiprows=[0,1],use_col=[0,1,2,3] )
    data_newscore2=data_newscore2.iloc[:,:4]
    data_newscore2.columns=['xingming','shenfenzheng','shijian','ultrashort']
    data_newscore2['shijian']=pd.to_datetime(data_newscore1['shijian'])
    data=pd.merge(data,data_newscore2,how='left',left_on=['身份证号','审批日期'],right_on=['shenfenzheng','shijian'])
    data.drop(['shenfenzheng','xingming','shijian'],axis=1,inplace=True)
    
    #中大额现金分期
    data_newscore3=pd.read_excel('sample_中大额现金分期.xlsx',sheetname ='信用雷达场景版_中大现金分期回溯测试结果',skiprows=[0,1],use_col=[0,1,2,3] )
    data_newscore3=data_newscore3.iloc[:,:4]
    data_newscore3.columns=['xingming','shenfenzheng','shijian','midlongscore']
    data_newscore3['shijian']=pd.to_datetime(data_newscore1['shijian'])
    data=pd.merge(data,data_newscore3,how='left',left_on=['身份证号','审批日期'],right_on=['shenfenzheng','shijian'])
    data.drop(['shenfenzheng','xingming','shijian'],axis=1,inplace=True)
    
    #消费分期
    data_newscore4=pd.read_excel('sample_消费分期（回溯）.xlsx',sheetname ='信用雷达场景版_消费分期回溯测试结果',skiprows=[0,1],use_col=[0,1,2,3] )
    data_newscore4=data_newscore4.iloc[:,:4]
    data_newscore4.columns=['xingming','shenfenzheng','shijian','xffqscore']
    data_newscore4['shijian']=pd.to_datetime(data_newscore1['shijian'])
    data=pd.merge(data,data_newscore4,how='left',left_on=['身份证号','审批日期'],right_on=['shenfenzheng','shijian'])
    data.drop(['shenfenzheng','xingming','shijian'],axis=1,inplace=True)
    
    #信用卡代偿
    data_newscore5=pd.read_excel('sample__信用卡代偿（回溯）.xlsx',sheetname ='信用雷达场景版_信用卡代偿回溯测试结果',skiprows=[0,1],use_col=[0,1,2,3] )
    data_newscore5=data_newscore5.iloc[:,:4]
    data_newscore5.columns=['xingming','shenfenzheng','shijian','xykscore']
    data_newscore5['shijian']=pd.to_datetime(data_newscore1['shijian'])
    data=pd.merge(data,data_newscore5,how='left',left_on=['身份证号','审批日期'],right_on=['shenfenzheng','shijian'])
    data.drop(['shenfenzheng','xingming','shijian'],axis=1,inplace=True)
    
    #添加晓玲新分数
    data_newscore6 = pd.read_csv('sample_newscore.csv')
    data_newscore6.columns = ['name','id_card_no','loan_day','newscore_target','newscore']
    data=pd.merge(data,data_newscore6,how='left',left_on=['身份证号','审批日期'],right_on=['id_card_no','loan_day'])
    data.drop(['name','id_card_no','loan_day','newscore_target'],axis=1,inplace = True)
    
    
    data.replace({np.nan:-1},inplace=True)
    cols=list(data);cols.insert(len(cols), cols.pop(cols.index('target')));data = data.loc[:, cols]
    data.iloc[:,3:]=data.iloc[:,3:].astype(int)
    return data


'''
datatest = data.iloc[:,3:-1]
bins =[];bins_count =[]

for i in datatest.columns:
    bins = pd.cut(datatest[i],10)
    bins.append([])
    bins_count = bins.value_counts()
    bins_count.append(bins_count)
    print("ok")
'''


def DATA_BIN(data,bin_num):
    bins=[];bins_count=[];flag=0
    for i in data.columns[:-1]:
        bins.append([]);bins_count.append([])
        data_hist=data[i].value_counts().sort_index()
        if data_hist.size<bin_num:
            for k in range(data_hist.size):
                bins[flag].append([])
                bins[flag][k].append(data_hist.index[k]);bins_count[flag].append(data_hist.iloc[k])
            flag+=1
            continue
        bin_count=int(data_hist.sum()/bin_num)
        bin_now=0;bin_count_now=0;bins[flag].append([])
        for j in range(data_hist.size):
            bins[flag][bin_now].append(data_hist.index[j])
            bin_count_now+=data_hist.iloc[j]
            if j<(data_hist.size-1):
                if (bin_count_now+data_hist.iloc[j+1])>bin_count:
                    bins_count[flag].append(bin_count_now)
                    bin_count_now=0
                    bin_now+=1
                    bins[flag].append([])
            else:
               bins_count[flag].append(bin_count_now)
        flag+=1
    return bins,bins_count

def PSI(data_counts,bins,bins_count,data2):
    psi=[];data2_counts=data2.shape[0];bins_count2=copy.deepcopy(bins_count)
    flag=0
    for i in data2.columns[:-1]:
        psi0=0
        for j in range(len(bins[flag])):
            bins_rate=bins_count[flag][j]/data_counts
            bins_count2[flag][j]=data2.loc[(data2[i]>=bins[flag][j][0])&(data2[i]<=bins[flag][j][-1])].shape[0]
            bins_rate2=data2.loc[data2[i].isin(bins[flag][j])].shape[0]/data2_counts
            if bins_rate2==0:
                bins_rate2=1
            psi0+=(bins_rate-bins_rate2)*np.log(bins_rate/bins_rate2)
        psi.append(psi0)
        flag+=1
    return psi,bins_count2


def PSI_(data):
    cutoff=data['审批日期'].quantile(0.8)
    data_oot1=data[data['审批日期']<=cutoff]
    data_oot2=data[data['审批日期']>cutoff]
    bins,bins_count=DATA_BIN(data_oot1.iloc[:,3:],10)
    psi=[];data_oot1_counts=data_oot1.shape[0];data_oot2_counts=data_oot2.shape[0]
    flag=0
    for i in data_oot1.columns[3:-1]:
        psi0=0
        for j in range(len(bins[flag])):
            bins_rate=bins_count[flag][j]/data_oot1_counts
            bins_rate2=data_oot2.loc[data_oot2[i].isin(bins[flag][j])].shape[0]/data_oot2_counts
            if bins_rate2==0:
                bins_rate2=1
            psi0+=(bins_rate-bins_rate2)*np.log(bins_rate/bins_rate2)
        psi.append(psi0)
        flag+=1
    return psi


def DATA_IV(data,bins):
    goodt=data[data.iloc[:,-1]==0].shape[0];badt=data[data.iloc[:,-1]==1].shape[0]
    good_bad=[[[] for i in range(data.shape[1])],[[] for i in range(data.shape[1])]]
    woe=[[] for i in range(data.shape[1])];ivi=[[] for i in range(data.shape[1])];iv=[];eff_rate=[]
    flag=0
    for i in data.columns[:-1]:
        data_b=data[[i,'target']]
        for j in range(len(bins[flag])):
            data_bb=data_b.loc[data_b[i].isin(bins[flag][j])]
            gb0=data_bb.loc[data_b.iloc[:,-1].isin([0])].shape[0]
            gb1=data_bb.loc[data_b.iloc[:,-1].isin([1])].shape[0]
            good_bad[0][flag].append(copy.deepcopy(gb0))
            good_bad[1][flag].append(copy.deepcopy(gb1))
            if gb0==0:
                gb0=1 
            if gb1==0:
                gb1=1
            woe[flag].append(np.log((gb0/goodt)/(gb1/badt)))
            ivi[flag].append((gb0/goodt-gb1/badt)*woe[flag][j])
        iv.append(round(np.sum(ivi[flag]),4))
        eff_rate.append(round(data[data[i]>-1].shape[0]/data.shape[0],4))
        flag+=1
    return iv,good_bad,eff_rate

def WRITE_BIN_IV(filename,data,bins,good_bad,iv):
    counts=data.shape[0]
    with open(filename,'w') as f:
        for i in range(len(iv)):
            counts_eff=data.iloc[:,i][data.iloc[:,i]>-1].shape[0]
            f.write(data.columns[i]+'  '+str(round(counts_eff/counts*100,2))+'%  '+str(round(iv[i],4))+'\n')
            for j in range(len(bins[i])):
                f.write('['+str(bins[i][j][0])+','+str(bins[i][j][-1])+']  '+str(good_bad[0][i][j])+' '+str(good_bad[1][i][j])+'  '+str(round(good_bad[1][i][j]/(good_bad[0][i][j]+good_bad[1][i][j])*100,1))+'%  '+str(round((good_bad[0][i][j]+good_bad[1][i][j])/counts*100,1))+'%\n')
    f.close()

def PRODUCT_SELECT(product_list,iv):
    cn=[['申请准入分','申请准入置信度','查询机构数','查询消费金融类机构数','查询网络贷款类机构数','总查询次数','最近查询时间','近1个月总查询笔数','近3个月总查询笔数','近6个月总查询笔数']
       ,['贷款行为分','贷款行为置信度', '贷款放款总订单数', '贷款已结清订单数', '贷款逾期订单数（M0+）', '贷款机构数', '消费金融类机构数','网络贷款类机构数_x','近1个月贷款笔数','近3个月贷款笔数','近6个月贷款笔数','历史贷款机构成功扣款笔数','历史贷款机构失败扣款笔数','近1个月贷款机构成功扣款笔数','近1个月贷款机构失败扣款笔数','信用贷款时长','最近一次贷款放款时间']
       ,['网贷建议授信额度','网贷额度置信度','网络贷款类机构数_y','网络贷款类产品数','网络贷款机构最大授信额度','网络贷款机构平均授信额度','消金建议授信额度','消金额度置信度','消金贷款类机构数','消金贷款类产品数','消金贷款类机构最大授信额度','消金贷款类机构平均授信额度']
       ,['探查结论_x','探查明细_x','最大履约金额','最近履约时间','履约笔数','当前逾期机构数_x','当前履约机构数_x','异常还款机构数_x','睡眠机构数_x']
       ,['探查结论_y','探查明细_y','最大逾期金额','最长逾期天数','最近逾期时间','当前逾期机构数_y','当前履约机构数_y','异常还款机构数_y','睡眠机构数_y']]
    cn_no=[iv[:10],iv[10:27],iv[27:39],iv[39:48],iv[48:]]
    column_select=[];iv_select=[]
    for i in product_list:
        column_select+=cn[i-1]
        iv_select+=cn_no[i-1]
    column_select.append('target')
    return column_select,iv_select
        

def DATA_COMBINE(data,iv,miniv,miss_rate,corr_score):
    text={'cname':list(data.columns[:-1]),'iv':iv}
    iv_sort=pd.DataFrame(text).sort_values(['iv'],ascending=False)
    iv_sort.drop(iv_sort[iv_sort['iv']<miniv].index,axis=0,inplace=True)
    combination=[];
    flag=0
    for i in range(iv_sort.shape[0]-1):
        if (data[data[iv_sort.iloc[i,0]]>-1].shape[0]/data.shape[0])>=miss_rate:
            for j in range(i+1,iv_sort.shape[0]):
                if (data[data[iv_sort.iloc[j,0]]>-1].shape[0]/data.shape[0])>=miss_rate:
                    if abs(data[[iv_sort.iloc[i,0],iv_sort.iloc[j,0]]].corr().iloc[0,1])<corr_score:
                        combination.append(iv_sort.iloc[i,0])
                        combination.append(iv_sort.iloc[j,0])
                        flag+=1
                        print(flag)
            '''
                    if flag==3:
                        break
            if flag==3:
                break
            '''
    return combination

def DENY_RULE(data,combination,lift_rate):
    posi=['贷款逾期订单数（M0+）','近1个月贷款笔数','近3个月贷款笔数','近6个月贷款笔数','历史贷款机构失败扣款笔数','近1个月贷款机构失败扣款笔数','最近一次贷款时间','最近履约时间','当前逾期机构数_x','异常还款机构数_x','探查结论_y','探查明细_y','最大逾期金额','最长逾期天数','当前逾期机构数_y','异常还款机构数_y']
    sample_count=data.shape[0]
    overdue_count=data[data['target']==1].shape[0]
    print(overdue_count/sample_count)
    deny_rule=[[[0,0,0,round(overdue_count/sample_count,4)]]]
    combination_set=list(set(combination))
    combination_set.append('target')
    bins100,bins100_count=DATA_BIN(data[combination_set],100)
    po=[]
    for i in range(int(len(combination)/2)):
        print(i+1)
        data_dr=data[[combination[i*2],combination[i*2+1],'target']]
        r=combination_set.index(combination[i*2])
        c=combination_set.index(combination[i*2+1])
        rnum=len(bins100[r])
        cnum=len(bins100[c])
        pass_overdue=np.zeros((2,rnum,cnum))
        pass_overdue_uniq=np.ones((rnum,cnum))
        for j in range(rnum):
            if combination[i*2] in posi:
                data_dr0=data_dr[(data_dr.iloc[:,0]>=bins100[r][j][-1])]
            else:
                data_dr0=data_dr[(data_dr.iloc[:,0]<=bins100[r][j][-1])]
            for k in range(cnum):
                if combination[i*2+1] in posi:
                    data_dr1=data_dr0[(data_dr.iloc[:,1]>=bins100[c][k][-1])]
                else:
                    data_dr1=data_dr0[(data_dr.iloc[:,1]<=bins100[c][k][-1])]
                sample_dr=data_dr1.shape[0]
                pass_overdue[0,j,k]=sample_dr/sample_count
                if sample_count!=sample_dr:
                    pass_overdue[1,j,k]=(overdue_count-data_dr1[data['target'].isin([1])].shape[0])/(sample_count-sample_dr)
        pass_overdue_uniq[1:]=pass_overdue[0,1:]-pass_overdue[0,:-1]
        pass_overdue[0][pass_overdue_uniq==0]=2
        pass_overdue[1][pass_overdue_uniq==0]=2
        pass_overdue_uniq[:]=1
        pass_overdue_uniq[:,1:]=pass_overdue[0,:,1:]-pass_overdue[0,:,:-1]
        pass_overdue[0][pass_overdue_uniq==0]=2
        pass_overdue[1][pass_overdue_uniq==0]=2
        pass_overdue_uniq[:]=1
        po_copy=copy.deepcopy(pass_overdue)
        po.append(po_copy)
        for n in lift_rate:
            deny_rule0=[]
            pass_overdue[0][pass_overdue[1]>n]=2
            deny_rule_index=np.where(pass_overdue[0]==np.min(pass_overdue[0]))
            for m in range(len(deny_rule_index[0])):
                deny_rule0.append([bins100[r][deny_rule_index[0][m]][-1],bins100[c][deny_rule_index[1][m]][-1],1-round(pass_overdue[0,deny_rule_index[0][m],deny_rule_index[1][m]],4),round(pass_overdue[1,deny_rule_index[0][m],deny_rule_index[1][m]],4)])
            deny_rule.append(deny_rule0)
    return deny_rule,po

def DENY_RULE_CONFIRM(combination,deny_rule,data):
    posi=['贷款逾期订单数（M0+）','近1个月贷款笔数','近3个月贷款笔数','近6个月贷款笔数','历史贷款机构失败扣款笔数','近1个月贷款机构失败扣款笔数','最近一次贷款时间','最近履约时间','当前逾期机构数_x','异常还款机构数_x','探查结论_y','探查明细_y','最大逾期金额','最长逾期天数','当前逾期机构数_y','异常还款机构数_y']
    sample_count=data.shape[0]
    overdue_count=data[data['target']==1].shape[0]
    pass_overdue=[[[1,round(overdue_count/sample_count,4)]]]
    for i in range(int(len(combination)/2)):
        data_dr=data[[combination[i*2],combination[i*2+1],'target']]
        for j in range(i*3+1,i*3+4):
            po=[]
            for k in range(len(deny_rule[j])):
                po0=[]
                if combination[i*2] in posi:
                    data_dr0=data_dr[(data_dr.iloc[:,0]>=deny_rule[j][k][0])]
                else:
                    data_dr0=data_dr[(data_dr.iloc[:,0]<=deny_rule[j][k][0])]
                if combination[i*2+1] in posi:
                    data_dr1=data_dr0[(data_dr.iloc[:,1]>=deny_rule[j][k][1])]
                else:
                    data_dr1=data_dr0[(data_dr.iloc[:,1]<=deny_rule[j][k][1])]
                sample_dr=data_dr1.shape[0]
                po0.append(round((sample_count-sample_dr)/sample_count,4))
                if sample_count!=sample_dr:
                    po0.append(round((overdue_count-data_dr1[data['target'].isin([1])].shape[0])/(sample_count-sample_dr),4))
                else:
                    po0.append(0)
                po.append(po0)
            pass_overdue.append(po)
    return pass_overdue

def PLOT_PASS_OVERDUE_HIST(filename,pass_overdue):
    plt.figure(figsize=(15,5))
    plt.subplots_adjust(left=0.1,right=0.95,bottom=0.15,top=0.95)
    gs=GridSpec(1,17)
    a=pass_overdue[0][0].flatten();a1=pass_overdue[0][1].flatten();a2=list(np.where(a==2)[0]);a2.reverse();a=list(a);a1=list(a1)
    for i in a2:
        del a[i];del a1[i]    
    ax1=plt.subplot(gs[:,:5])
    ax1.hist2d(a,a1,bins=20,cmap='rainbow',vmax=1)
    a=pass_overdue[1][0].flatten();a1=pass_overdue[1][1].flatten();a2=list(np.where(a==2)[0]);a2.reverse();a=list(a);a1=list(a1)
    for i in a2:
        del a[i];del a1[i]
    ax2=plt.subplot(gs[:,6:11])
    ax2.hist2d(a,a1,bins=20,cmap='rainbow',vmax=1)
    a=pass_overdue[2][0].flatten();a1=pass_overdue[2][1].flatten();a2=list(np.where(a==2)[0]);a2.reverse();a=list(a);a1=list(a1)
    for i in a2:
        del a[i];del a1[i]
    ax3=plt.subplot(gs[:,12:])
    ax3.hist2d(a,a1,bins=20,cmap='rainbow',vmax=1)
    plt.savefig(filename)
    plt.close()

def WRITE_REPORT(filename,data,eff_rate,iv,combination,deny_rule):
    combination_reshape=[' ']
    for k in range(len(combination)):
        if k%2==0:
            combination_reshape.append(combination[k]+'+'+combination[k+1])
            combination_reshape.append(combination[k]+'+'+combination[k+1])
            combination_reshape.append(combination[k]+'+'+combination[k+1])
    combination_set=list(set(combination))
    combination_set.append('target')
    iv_eff={'eff_rate':eff_rate,'iv':iv}
    writer=pd.ExcelWriter(filename)
    pd.DataFrame(iv_eff,index=data.columns[:-1]).to_excel(writer,'指标')
    data[list(set(combination))].corr().to_excel(writer,'相关性')
    pd.DataFrame(deny_rule,index=combination_reshape).to_excel(writer,'策略制定')
    writer.save()

def DATA_GAIN_KS(data):
    p_rate=[];pv_plus=[];TPR=[];FPR=[];KS=[]#;lift=[];nTNR=[]
    for i in data.columns[:-1]:
        data0=data[[i,'target']][data[i]>-1]
        data_hist=data0[i].value_counts().sort_index()
        p_count=[];pv_plus0=[];ks0=[]#;lift0=[];nTNR0=[]
        for j in range(data_hist.shape[0]):
            P=data0[data0['target'].isin([0])].shape[0]
            N=data0[data0['target'].isin([1])].shape[0]
            data01=data0[data0[i]>=data_hist.index[j]]
            data02=data01[data01['target'].isin([1])]
            TP=data01[data01['target'].isin([0])].shape[0]
            FP=data02.shape[0]
            TN=data02[data02[i]<data_hist.index[j]].shape[0]
            #FN=data.loc[(data[i]>-1)&(data[i]<data_hist.index[j])&(data['target'].isin([0]))].shape[0]
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
            if P==0:
                P+=1
            if N==0:
                N+=1
            pv_plus0.append(TP/p_count0)
            ks0.append(round(abs(TP/P-FP/N),4))
            #lift0.append(pv_plus0[j]/(P/data0.shape[0]))
            #nTNR0.append(1-(TN/N))
            p_count.append(p_count0/data0.shape[0])
        p_rate.append(p_count)
        pv_plus.append(pv_plus0)
        #TPR.append(fx0)
        #FPR.append(gx0)
        KS.append(ks0)
        #lift.append(lift0)
        #nTNR.append(nTNR0)
    return p_rate,pv_plus,KS

def WRITE_GAIN_KS(filename,p_rate,pv_plus,KS):
    with open(filename,'w') as f:
        for i in range(len(p_rate)):
            f.write(str(p_rate[i])+'\n')
            f.write(str(pv_plus[i])+'\n')
            f.write(str(KS[i])+'\n')
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