import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt



input_data = pd.read_excel('/Users/dylan/DataBase/signal_process/50ETF-signalout copy.xlsx')
signal_input = pd.read_excel('/Users/dylan/DataBase/signal_process/signal_result-30 copy.xlsx')
# 加权选择
signal_input_quantile = signal_input[['annual_return_sp','win_rate_sp','pc_ratio_sp']].quantile([0.25,0.5,0.75])
for col_name in ['annual_return_sp','win_rate_sp','pc_ratio_sp']:
    def get_weight_group(x) :
        if x < signal_input_quantile[col_name].loc[0.25]: 
            return 1
        elif signal_input_quantile[col_name].loc[0.25] < x  and  x < signal_input_quantile[col_name].loc[0.5]: 
            return 2 
        elif signal_input_quantile[col_name].loc[0.5] < x and  x < signal_input_quantile[col_name].loc[0.75] : 
            return 3         
        else : 
            return 4 
    new_weighte_col_name = col_name + '_weight'
    signal_input[new_weighte_col_name] = signal_input[col_name].map(get_weight_group)

signal_input['Max_method'] = signal_input[['annual_return_sp_weight','win_rate_sp_weight','pc_ratio_sp_weight']].sum(axis = 1)

signal_input['Max_method'].sort_values(ascending = False)

# 选择当期最大
signal_input['Max_method'] = signal_