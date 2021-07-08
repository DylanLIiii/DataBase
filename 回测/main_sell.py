# -*- coding: utf-8 -*-
"""
Created on Thu May  6 14:23:59 2021

@author: liuyu
"""

import pandas as pd

import back_test_selling
#import cal_benchmark_policy
import evaluation_selling

import sys
import os
work_dir = os.getcwd()
sys.path.append(work_dir + '/conf/')
# import config


'''
主函数入口，输入文件名，选合约方式、卖出方式、是否择时、起止日期，生成合约持仓序列和净值序列，并计算年化收益、最大回撤与夏普比率
test_pool: 文件名 形如XXXX_pool
select_policy: 1为选虚值合约，2为选实值合约
sell_policy: 1为持有至到期，2为根据信号卖出
timing: True为启动择时，择时信号为50ETF文件对应列名，False为不启动择时
'''
def main(selling_ratio,start_date,end_date,timing):
   
    #根据输入参数生成策略名

    test_pool_name = str(selling_ratio*100)+'%比例减仓策略_'+timing+'_'+start_date[:10]+'_'+end_date[:10]
                      
    print('=========执行策略文件：'+test_pool_name+'=========')

    print('=========开始进行净值回测=========')

    try:
        portfolio_result = pd.read_excel('./result/'+test_pool_name+'_result.xlsx')
    except:
        portfolio_result = back_test_selling.back_test_selling(test_pool_name,selling_ratio,start_date,end_date,timing)
        
        df = pd.DataFrame()
        #df['target'] = ['benchmark',test_pool]
        df['maxdrawdown'] = evaluation_selling.maxdrawdown(portfolio_result) 
        df['annual_return'] = evaluation_selling.annual_return(portfolio_result)
        df['sharpe_ratio'] = evaluation_selling.sharpe_ratio(portfolio_result)
        result = df
    
    else:
        result = '=========暂无支持的合约策略========='
    
    #cal_benchmark_policy.get_benchmark_portfolio('计算空仓策略')
    
    print(result)
    return(result)

 
if __name__=='__main__':

    
    tmp_start_date = '2018-06-01'
    
    tmp_end_date =   '2021-05-25'
    
    tmp_selling_ratio = 1
    
   
    #main(tmp_select_policy,tmp_sell_policy,tmp_option_ratio,tmp_start_date,tmp_end_date,tmp_timing,tmp_bid)    
    
    #for tmp_timing in ['lr',"svm", "xgb", "gbdt", "rfc", "dtc", "knnc", "bagc", "etc", "adac"]:
    #for tmp_timing in ['昨日收盘价-未来10日均价下跌','昨日收盘价-未来15日均价下跌','未来两日开盘价持续下跌','布林带-空头']:
    input_data = pd.read_excel('./input_data/50ETF.xlsx')
    for tmp_timing in input_data.columns[2:]:
        main(tmp_selling_ratio,tmp_start_date,tmp_end_date,tmp_timing)
    

    
    
    
    
    
    
    
    