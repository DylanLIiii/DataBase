# -*- coding: utf-8 -*-
"""
Created on Tue Jun 29 09:53:58 2021

@author: liuyu
"""

import pandas as pd

'''
按照一个评估指标选择top1-model，当回测期内评估指标相同时回溯上一个回测期
'''
def cal_signal(training_window,method,select_num=1):
    
    input_data = pd.read_excel('./input_data/50ETF-signalout.xlsx')
    signal_input = pd.read_excel('./input_data/signal_result-'+str(training_window)+'.xlsx')        
    
    tmp_signal_name = 'top' + str(select_num) + '-' + method + '-' + str(training_window)
    
    #按照当期method判断排名第一的模型
    signal_input['max_method'] = signal_input.groupby("start_date")[method].transform('max')
    #signal_input['max_win_rate_sp'] = signal_input.groupby("start_date")['win_rate_sp'].transform('max')
    #计算上期method
    signal_input.sort_values(by=['model','start_date'],inplace=True)
    signal_input['last_method'] = signal_input[method].shift(1)
    signal_input = signal_input[signal_input['start_date']!=signal_input['start_date'].iloc[0]] 
    #在sharpe_ratio_sp和win_rate_sp相同的时候比较上一期sharpe_ratio_sp    
    signal_input_filter = signal_input[signal_input[method]==signal_input['max_method']]
    signal_input_filter.sort_values(by='last_method',ascending=False,inplace=True)
    signal_input_filter = signal_input_filter.drop_duplicates(subset='start_date',keep='first')
    #将选出的top1 model错期一期作为下期信号
    signal_input_filter.sort_values(by='start_date',inplace=True)
    signal_input_filter['model_selected'] = signal_input_filter['model'].shift(1)
    
    signal_input_filter.to_excel('./input_data/signal_roll/'+tmp_signal_name+'.xlsx',index=False)
    
    input_data[tmp_signal_name] = 0
    for i in range(len(input_data)):
        tmp_trade_date = input_data['trade_date'].iloc[i]
        try:
            tmp_model = signal_input_filter[(signal_input_filter['start_date']<=tmp_trade_date)&(signal_input_filter['end_date']>=tmp_trade_date)]['model_selected'].iloc[0]
            input_data[tmp_signal_name].iloc[i] = input_data[tmp_model].iloc[i]
        except:
            continue
    
    input_data.to_excel('./input_data/50ETF-signalout.xlsx',index=False)
    result = tmp_signal_name + '信号处理完成'
    print(result)
    return(result)  


    
    
    
cal_signal(30,'50ETF-signalout.xlsx',select_num=1)