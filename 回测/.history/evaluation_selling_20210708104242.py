# -*- coding: utf-8 -*-
"""
Created on Thu May  6 14:22:23 2021

@author: liuyu
"""

import pandas as pd
import os

'''
最大回撤、年化收益、夏普比率
'''
def maxdrawdown(df):
    #df = pd.read_excel('./result/test_pool_2_result.xlsx',index=False)
    mdd_benchmark = ((df['benchmark_value'].cummax()-df['benchmark_value'])/df['benchmark_value'].cummax()).max()
    mdd_portfolio = ((df['portfolio_value'].cummax()-df['portfolio_value'])/df['portfolio_value'].cummax()).max()
    #mdd_portfolio_1 = ((df['portfolio_value_1'].cummax()-df['portfolio_value_1'])/df['portfolio_value_1'].cummax()).max()
    return([round(mdd_benchmark*100,2),round(mdd_portfolio*100,2)])

def annual_return(df,total_cap=100):
    
    tr_benchmark = df['benchmark_value'].iloc[-1]/total_cap 
    tr_portfolio = df['portfolio_value'].iloc[-1]/total_cap 
    #tr_portfolio_1 = df['portfolio_value_1'].iloc[-1]/total_cap 
    #计算年化收益率
    y = int(df['trade_date'].iloc[-1][:4])-int(df['trade_date'].iloc[0][:4])+1
    ar_benchmark = ((tr_benchmark **(1/y))-1)*100
    ar_portfolio = ((tr_portfolio **(1/y))-1)*100
    #ar_portfolio_1 = ((tr_portfolio_1 **(1/y))-1)*100
    return([round(ar_benchmark,2),round(ar_portfolio,2)])
    
def sharpe_ratio(df):
    
    tr_benchmark = (df['benchmark_value']-df['benchmark_value'].shift(1))/df['benchmark_value'].shift(1)
    tr_portfolio = (df['portfolio_value']-df['portfolio_value'].shift(1))/df['portfolio_value'].shift(1)
    #tr_portfolio_1 = (df['portfolio_value_1']-df['portfolio_value_1'].shift(1))/df['portfolio_value_1'].shift(1)
    #y = int(df['trade_date'].iloc[-1][:4])-int(df['trade_date'].iloc[0][:4])+1
    sharpe_ratio_benchmark = (tr_benchmark.mean() - (1.025**(1/365)-1))/tr_benchmark.std()*(250**(1/2))
    if tr_portfolio.std() != 0:        
        sharpe_ratio_portfolio = (tr_portfolio.mean() - (1.025**(1/365)-1))/tr_portfolio.std()*(250**(1/2))
    else:
        sharpe_ratio_portfolio = 0
    #sharpe_ratio_portfolio_1 = (tr_portfolio_1.mean() - (1.025**(1/365)-1))/tr_portfolio_1.std()*(250**(1/2))

    return([round(sharpe_ratio_benchmark,2),round(sharpe_ratio_portfolio,2)])

    
def win_rate_sp(df):
    signal = df.columns[2]
    selling_days = len(df[df[signal]!=0])
    df['benchmark_var'] = df['50ETF'] - df['50ETF'].shift(1)
    
    tmp_df = df[(df[signal]!=0)&(df['benchmark_var']<0)]
    
    if selling_days==0:
        win_rate_sp = 0
    else:
        win_rate_sp = len(tmp_df) / selling_days
    
    sell_times = len(df['sell_point'].dropna())/(len(df)/250)
        
    #sell_times = sum(df['sell_point'].dropna())/(len(df)/250)
    if len(df['sell_point'].dropna()) ==0:
        avg_holding_period = 0
    else:
        avg_holding_period = selling_days / len(df['sell_point'].dropna())
    
    #benchmark_win_rate = selling_days/len(df)
    
    return([round(sell_times,2),round(avg_holding_period,2),round(win_rate_sp,2)])

def pc_ratio(df):
    
    df['benchmark_var'] = df['benchmark_value']-df['benchmark_value'].shift(1)
    df['portfolio_var'] = df['portfolio_value']-df['portfolio_value'].shift(1)
    #df['portfolio_1_var'] = df['portfolio_value_1']-df['portfolio_value_1'].shift(1)
    
    pc_ratio_benchmark = (df[df['benchmark_var']>0]['benchmark_var'].mean())/abs((df[df['benchmark_var']<0]['benchmark_var'].mean()))
    pc_ratio_portfolio = (df[df['portfolio_var']>0]['portfolio_var'].mean())/abs((df[df['portfolio_var']<0]['portfolio_var'].mean()))
    #pc_ratio_portfolio_1 = (df[df['portfolio_1_var']>0]['portfolio_1_var'].mean())/abs((df[df['portfolio_1_var']<0]['portfolio_1_var'].mean()))
    
    return([round(pc_ratio_benchmark,2),round(pc_ratio_portfolio,2)])
    
    
def evaluation(result_path):
    
    path = './result/'
    evaluation_result = pd.DataFrame()
    portfolio_result  = pd.DataFrame()
    for root, dirs, files in os.walk(path):  
        for file in files:
            df = pd.read_excel('./result/'+file
                               )
            portfolio_name = file.split('.xlsx')[0]
            
            ratio_policy  = portfolio_name.split('_')[0].split('比例')[0]            
            timing_policy = portfolio_name.split('策略_')[1].split('_20')[0]     
            #start_date    = portfolio_name.split('_')[4]
            #end_date      = portfolio_name.split('_')[5]            
            tmp_dict = {'减仓比例': ratio_policy,
                        '信号指标':timing_policy,
                        '最大回撤-空仓策略':maxdrawdown(df)[1],
                        '年化收益率-空仓策略':annual_return(df)[1],
                        '年化夏普率-空仓策略':sharpe_ratio(df)[1],
                        '年均空仓次数':win_rate_sp(df)[0],
                        '平均空仓时间':win_rate_sp(df)[1],
                        '空仓策略胜率':win_rate_sp(df)[2],
                        '空仓策略盈亏比':pc_ratio(df)[1]}

            tmp_df = df[['trade_date','portfolio_value']]
            tmp_df.columns = ['trade_date',portfolio_name]
            evaluation_result = evaluation_result.append(tmp_dict,ignore_index=True)
            #evaluation_result = evaluation_result.append(tmp_dict_1,ignore_index=True)
            
            if portfolio_result.empty:
                portfolio_result = tmp_df
            else:
                portfolio_result = pd.merge(portfolio_result,tmp_df,on='trade_date')
            
    tmp_dict_1 ={'减仓比例':'benchmark',
                '信号指标':'benchmark',
                '最大回撤-空仓策略':maxdrawdown(df)[0],
                '年化收益率-空仓策略':annual_return(df)[0],
                '年化夏普率-空仓策略':sharpe_ratio(df)[0],
                '年均空仓次数':0,
                '平均空仓时间':0,
                '空仓策略胜率':0,
                '空仓策略盈亏比':pc_ratio(df)[0]}

    evaluation_result = evaluation_result.append(tmp_dict_1,ignore_index=True)
    tmp_df = df[['trade_date','benchmark_value']]
    portfolio_result = pd.merge(portfolio_result,tmp_df,on='trade_date')
    portfolio_result.to_excel('./evaluation/portfolio_result.xlsx',index=False)
    #evaluation_result = evaluation_result.append(tmp_dict,ignore_index=True)
    evaluation_result = evaluation_result[['减仓比例','信号指标','最大回撤-空仓策略','年化收益率-空仓策略','年化夏普率-空仓策略','年均空仓次数','平均空仓时间','空仓策略胜率','空仓策略盈亏比']]
    evaluation_result.to_excel('./evaluation/evaluation_result.xlsx',index=False)
    
    return(result_path)
    
    
if __name__=='__main__':


    evaluation('策略回测统计')
    
    