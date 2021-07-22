
import pandas as pd 
import re 

def get_statement(trade_date):
    
    factor_signals = pd.read_csv(r'/Users/dylan/Github repo/DataBase/因子需求/factor_date.csv')
    model_signals = pd.read_excel(r'/Users/dylan/Github repo/DataBase/因子需求/50ETF.xlsx')
    
    # 选取相同时间索引长度的
    if len(factor_signals.index) > len(model_signals) : 
        
    
    factor_signal[factor_signal == 1]
    
    