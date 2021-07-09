# -*- coding: utf-8 -*-
"""
Created on Thu May  6 14:23:59 2021

@author: liuyu
"""

import pandas as pd

import back_test_selling
#import cal_benchmark_policy
import evaluation_selling

'''
import sys
import os
work_dir = os.getcwd()
sys.path.append(work_dir + '/conf/')
import config
'''

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
        portfolio_result = back_test_selling.back_test_selling(test_pool_name,selling_ratio,start_date,end_date,timing)
        
        df = pd.DataFrame()
        #df['target'] = ['benchmark',test_pool]
        df['maxdrawdown'] = evaluation_selling.maxdrawdown(portfolio_result) 
        df['annual_return'] = evaluation_selling.annual_return(portfolio_result)
        df['sharpe_ratio'] = evaluation_selling.sharpe_ratio(portfolio_result)
        df['bid_rate'] = [0,evaluation_selling.win_rate_sp(portfolio_result)[0]]
        df['hold_period'] = [0,evaluation_selling.win_rate_sp(portfolio_result)[1]]
        df['win_rate'] = [0,evaluation_selling.win_rate_sp(portfolio_result)[2]]
        df['pc_ratio'] = evaluation_selling.pc_ratio(portfolio_result)
        
        result = df
    
    except:
        result = '=========暂无支持的合约策略========='
    
    print(result)
    return(result)

def signal_roll(training_window,sleep_window,selling_ratio,start_date,end_date):
    
    input_data = pd.read_excel('./input_data/50ETF.xlsx')
    trade_date_list = list(input_data['trade_date'].apply(lambda X: str(X)[:10]))
    
    tmp_start_date = start_date
    out_data = pd.DataFrame()
    
    while tmp_start_date <= trade_date_list[-sleep_window]:
    
        tmp_data = input_data[input_data['trade_date']>=tmp_start_date].iloc[:training_window]
        tmp_end_date = str(tmp_data['trade_date'].iloc[-1])[:10]
        
        for tmp_timing in tmp_data.columns[2:]:
            
            try:
                result_df = main(selling_ratio,tmp_start_date,tmp_end_date,tmp_timing)
                #print(result_df)
                #tmp_maxdrawdown_op = result_df['maxdrawdown'].iloc[1]
                tmp_annual_return_sp = result_df['annual_return'].iloc[1]
                tmp_sharpe_ratio_sp = result_df['sharpe_ratio'].iloc[1]
                tmp_win_rate_sp = result_df['win_rate'].iloc[1]
                tmp_pc_ratio_sp = result_df['pc_ratio'].iloc[1]
                
                tmp_dict = {'start_date':tmp_start_date,'end_date':tmp_end_date,'model':tmp_timing,'annual_return_sp':tmp_annual_return_sp,'sharpe_ratio_sp':tmp_sharpe_ratio_sp,'win_rate_sp':tmp_win_rate_sp,'pc_ratio_sp':tmp_pc_ratio_sp}
            except:
                continue
            
            out_data = out_data.append(tmp_dict,ignore_index=True)
              
        try:
            tmp_start_date = [n for n in trade_date_list if n >= tmp_start_date][sleep_window]

        except:
            break
    out_data = out_data[['start_date','end_date','model','annual_return_sp','sharpe_ratio_sp','win_rate_sp','pc_ratio_sp']]
    out_data.to_excel('./input_data/signal_result-'+str(training_window)+'_'+str(sleep_window)+'.xlsx',index=False)    

def benchmark_roll(training_window,sleep_window,selling_ratio,start_date,end_date):

    input_data = pd.read_excel('./input_data/50ETF.xlsx')
    trade_date_list = list(input_data['trade_date'].apply(lambda X: str(X)[:10]))
    
    tmp_start_date = start_date
    out_data = pd.DataFrame()
    
    while tmp_start_date <= trade_date_list[-sleep_window]:
    
        tmp_data = input_data[input_data['trade_date']>=tmp_start_date].iloc[:training_window]
        tmp_end_date = str(tmp_data['trade_date'].iloc[-1])[:10]
        
        tmp_timing = tmp_data.columns[2]
        try:
            result_df = main(selling_ratio,tmp_start_date,tmp_end_date,tmp_timing)
            #print(result_df)
            #tmp_maxdrawdown_op = result_df['maxdrawdown'].iloc[1]
            tmp_annual_return_sp = result_df['annual_return'].iloc[0]
            tmp_sharpe_ratio_sp = result_df['sharpe_ratio'].iloc[0]
            tmp_win_rate_sp = 0
            tmp_pc_ratio_sp = result_df['pc_ratio'].iloc[0]
            
            tmp_dict = {'start_date':tmp_start_date,'end_date':tmp_end_date,'model':'benchmark','annual_return':tmp_annual_return_sp,'sharpe_ratio':tmp_sharpe_ratio_sp,'win_rate':tmp_win_rate_sp,'pc_ratio':tmp_pc_ratio_sp}
        except:
            continue
          
        out_data = out_data.append(tmp_dict,ignore_index=True)
          
        try:
            tmp_start_date = [n for n in trade_date_list if n >= tmp_start_date][sleep_window]
    
        except:
            break
    out_data = out_data[['start_date','end_date','model','annual_return','sharpe_ratio','win_rate','pc_ratio']]
    out_data.to_excel('./input_data/output_result-'+str(training_window)+'_'+str(sleep_window)+'.xlsx',index=False)        

if __name__=='__main__':
    
    
    start_date = '2018-05-01'
    
    end_date =   '2021-06-30'
    
    tmp_selling_ratio = 1
    
    #tmp_timing =     'T10-adj2'
    
    training_window = 30
    
    sleep_window = 5
    
    signal_roll(training_window,sleep_window,tmp_selling_ratio,start_date,end_date)
    #benchmark_roll(training_window,sleep_window,tmp_selling_ratio,start_date,end_date)
 
    
    
    
    
    