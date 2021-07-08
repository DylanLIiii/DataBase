# -*- coding: utf-8 -*-
"""
Created on Thu May  6 14:10:28 2021

@author: liuyu
"""

import pandas as pd
import numpy as np
#import os
#import pgsql_utils
'''
from WindPy import *
w.start()
w.isconnected()
'''

'''
回测效果
参数 option_ratio = '等量对冲' 等量对冲：每买1份标的就买1份合约
     option_ratio = 0,3%,10%,50%,100% 将当前净值的XX%用于买合约
手续费50ETF按万分之一点五；期权合约按照7元一张；卖期权保证金按照买入日维持保证金的2倍；无风险利率为2%
'''  

def back_test_selling(test_pool_name,selling_ratio,start_date,end_date,signal,total_cap=100):
        
    benchmark_file = pd.read_excel('./input_data/50ETF.xlsx',index=False)
    benchmark_file = benchmark_file[['trade_date','50ETF',signal]]
    benchmark_file['trade_date'] = benchmark_file['trade_date'].astype("str").str[0:10] 
       
    price_data = benchmark_file[(benchmark_file['trade_date']>=start_date)&(benchmark_file['trade_date']<=end_date)]
    price_data = price_data.sort_values(by='trade_date')
    price_data['benchmark_share'] = total_cap*(1-1.5/10000)/float(price_data['50ETF'].iloc[0])
    price_data['benchmark_value'] = price_data['benchmark_share'] * price_data['50ETF']
    price_data['50ETF_share'],price_data['portfolio_value'] = [0,0] 
    price_data['sell_point'],price_data['buy_point'] = [None,None]
 
    #滚动回测按信号执行空仓策略
    for i in range(0,len(price_data)):
        #第一个交易日
        if i==0:
            #如果出现信号，则按照selling_ratio减仓
            if price_data[signal].iloc[i] != 0:
                #合约价值永远分为两部分，一部分由标的浮动价值构成，另一部分是撤出的资金
                tmp_50etf_share = (1-selling_ratio) * price_data['benchmark_share'].iloc[i]
                tmp_cash = selling_ratio * total_cap
                price_data['50ETF_share'].iloc[i] = tmp_50etf_share
                price_data['portfolio_value'].iloc[i] = tmp_50etf_share * float(price_data['50ETF'].iloc[i]) + tmp_cash   
                #price_data['sell_point'].iloc[i] = 1
            else:               
                tmp_50etf_share = price_data['benchmark_share'].iloc[i]
                tmp_cash = 0
                price_data['50ETF_share'].iloc[i] = tmp_50etf_share
                price_data['portfolio_value'].iloc[i] = tmp_50etf_share * float(price_data['50ETF'].iloc[i]) + tmp_cash  
                price_data['buy_point'].iloc[i] = price_data['portfolio_value'].iloc[i]                 
        #如果空头信号不发生变化
        elif price_data[signal].iloc[i] == price_data[signal].iloc[i-1]:

            price_data['50ETF_share'].iloc[i] = tmp_50etf_share
            price_data['portfolio_value'].iloc[i] = tmp_50etf_share * float(price_data['50ETF'].iloc[i]) + tmp_cash 

        #如果空头信号发生变化
        else:
            #如果变为空头信号
            if price_data[signal].iloc[i] != 0:
                tmp_cash = tmp_50etf_share * (float(price_data['50ETF'].iloc[i])) * selling_ratio / (1+1.5/10000)
                tmp_50etf_share = tmp_50etf_share * (1-selling_ratio)
                price_data['50ETF_share'].iloc[i] = tmp_50etf_share
                price_data['portfolio_value'].iloc[i] = tmp_50etf_share * float(price_data['50ETF'].iloc[i]) + tmp_cash                               
                price_data['sell_point'].iloc[i] = price_data['portfolio_value'].iloc[i]
            else:
                tmp_50etf_share = tmp_50etf_share + tmp_cash / ((float(price_data['50ETF'].iloc[i]))*(1+1.5/10000))
                tmp_cash = 0
                price_data['50ETF_share'].iloc[i] = tmp_50etf_share
                price_data['portfolio_value'].iloc[i] = tmp_50etf_share * float(price_data['50ETF'].iloc[i]) + tmp_cash            
                price_data['buy_point'].iloc[i] = price_data['portfolio_value'].iloc[i]
    
    price_data.to_excel('./result/'+test_pool_name+'_result.xlsx',index=False)
    return(price_data)        
    