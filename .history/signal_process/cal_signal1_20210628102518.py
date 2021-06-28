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

# 至少选择当期Top3
signal_input.sort_values(by = 'Max_method', ascending = False ).groupby('start_date').head(3)



"""  #当期相同则计算上期method
if len(signal_input_filter['Max_method']) > 3:       
    signal_input_filter.sort_values(by=['model','start_date'],inplace=True) 
    signal_input_filter['Last_method'] = signal_input_filter['Max_method'].shift(1) 
    signal_output = signal_input_filter.nlargest(3,'Last_method',keep="first")
else:
    signal_output = signal_input_filter.sort_values(by="start_date").shift(1)

    signal_input_filter.sort_values(by='start_date',inplace=True)
    signal_input_filter['model_selected'] = signal_input_filter['model'].shift(1)
    
    signal_input_filter.to_excel('/Users/dylan/DataBase/signal_process/1.xlsx',index=False) """
# 选出当期Top3

signal_input_filter = signal_input.groupby(by = 'start_date').apply(lambda x : x.nlargest(3, 'Max_method', keep = 'all'))


""" # 权重相同则比较上一期
for i in ['start_date']:
    if len(signal_input) """
    for col_name in
def get_weight_group(x) :
    if x < signal_output_quantile[col_name].loc[0.25]: 
        return 1
    elif signal_ouput_quantile[col_name].loc[0.25] < x  and  x < signal_input_quantile[col_name].loc[0.5]: 
        return 2 
    elif signal_output_quantile[col_name].loc[0.5] < x and  x < signal_input_quantile[col_name].loc[0.75] : 
        return 3         
    else : 
        return 4 
signal_output = pd.DataFrame()
for i in signal_input_filter['start_date'].drop_duplicates(): 
    column = signal_input_filter.loc[(i)].sample(1)
    signal_output = signal_output.append(column)

signal_output['model_selected'] = signal_output['model'].shift(1)
signal_output.
### 得到信号
df = signal_output[['annual_return_sp','win_rate_sp','pc_ratio_sp']]
s = signal_output.[[]]

# signal_output
signal_output.to_excel('/Users/dylan/DataBase/signal_process/1.xlsx')



