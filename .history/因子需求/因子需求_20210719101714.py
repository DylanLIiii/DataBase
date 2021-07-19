
import pandas as pd 

def get_statement(trade_date):
    factors = pd.read_excel(r'/Users/dylan/Github repo/DataBase/因子需求/因子表.xlsx')
    factor_signals = pd.read_excel(r'/Users/dylan/Github repo/DataBase/因子需求/factor_data.xlsx')
    
    factorfactor_signals.set_index('trade_date').loc[trade_date,:]
    