
import pandas as pd 
import re 

def get_statement(trade_date):
    
    factor_signals = pd.read_csv(r'/Users/dylan/Github repo/DataBase/因子需求/factor_date.csv')
    model_signals = pd.read_excel(r'/Users/dylan/Github repo/DataBase/因子需求/50ETF.xlsx')
    factor_signals.set_index(by'trade_date')
    model_signals.set_index()
    # 选取相同时间索引长度的因子信号和模型信号拼接
    
        
    
    
    
    