
import pandas as pd 
import re 

def get_statement(trade_date):
    
    import pandas as pd 
    import re 
    
    # 数据处理
    factor_signals = pd.read_csv(r'/Users/dylan/Github repo/DataBase/因子需求/factor_date.csv')
    model_signals = pd.read_excel(r'/Users/dylan/Github repo/DataBase/因子需求/50ETF.xlsx')
    
    factor_signals.set_index('trade_date',inplace = True)
    model_signals.set_index('trade_date',inplace = True)
    
    # 选取相同时间索引长度的因子信号和模型信号拼接
    signals_input = (factor_signals.loc[list(model_simple.index)]
                        if  len(factor_signals.index) >= len(model_signals.index)
                            else model_signals.loc[list(factor_signals.index]
        
    
    
    
    