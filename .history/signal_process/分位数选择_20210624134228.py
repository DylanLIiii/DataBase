import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt



input_data = pd.read_excel('/Users/dylan/DataBase/signal_process/50ETF-signalout copy.xlsx')
signal_output = pd.read_excel('/Users/dylan/DataBase/signal_process/signal_result-30 copy.xlsx')

signal_output_quantile = signal_output[['annual_return_sp','win_rate_sp','pc_ratio_sp']].quantile([0.25,0.5,0.75])


signal_output_weight = signal_output_quantile[['annual_return_sp','win_rate_sp','pc_ratio_sp']].loc[0.5].loc['annual_return_sp'] < signal_output['annual_return_sp']
signal_output['signal_output_weight'] = signal_output_weight.replace({True : 1, False : 0})

# 选择函数
def get_weight_group(x) :
    if x < signal_output_quantile[methods]
# 权重函数

def method_weight_func(method) : 
    methods = pd.Series[method]
    
    def get_weight_group(x) :
    if x < signal_output_quantile[methods].loc[0.25].loc[methods.iloc[1]]: 
        return 1
    elif signal_output_quantile[methods].loc[0.25].loc[methods.iloc[1]] < x < signal_output_quantile[methods].loc[0.5]: 
        return 2 
    elif signal_output_quantile[methods].loc[0.5].loc[emthods.iloc[1]] < x < 
        return 3         
    
    for i in range(1,len(methods)):
        signal_output_weight1 = (signal_output_quantile[methods].loc[0.5].loc[methods.iloc[i]] < signal_output[methods.iloc[1]]) & (signal_output_quantile[methods].loc[0.75].loc[methods.iloc[i]] < signal_output[methods.iloc[1]])
        signal_output_weight1.replace({True : 1, False : 0})
        signal_output_weight2 = (signal_output_quantile[methods].loc[0.75].loc[methods.iloc[i]] < signal_output[methods.iloc[1]])
        signal_output_weight2.replace({True : 2, False : 0})
        signal_output_weight = signal_output_weight2 + signal_output_weight1
        signal_output[str(method.loc[i]) + '_weight'] = signal_output_weight1 + signal_output_weight2
    signal_output['Max_method'] = signal_output[method + '_weight'].sum(axis=1)

    signal_output.sort_values(by = 'Max_weight' ,axis = 0 , ascending = False, inplace = True)

#