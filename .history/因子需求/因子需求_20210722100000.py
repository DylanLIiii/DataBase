
import pandas as pd 
import re 

def get_statement(trade_date):
    factor_signals = pd.read_csv(r'/Users/dylan/Github repo/DataBase/因子需求/factor_data.xlsx')
    model_signals = pd.read_excel(r'')
    factor_signal = factor_signals.set_index('trade_date').loc[trade_date,:]
    
    factor_signal[factor_signal == 1]
    
    