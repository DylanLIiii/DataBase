import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt
from interval import interval, inf, imath



input_data = pd.read_excel('/Users/dylan/DataBase/signal_process/50ETF-signalout copy.xlsx')
signal_output = pd.read_excel('/Users/dylan/DataBase/signal_process/signal_result-30 copy.xlsx')

signal_output_quantile = signal_output[['annual_return_sp','win_rate_sp','pc_ratio_sp']].quantile([0.25,0.5,0.75])


signal_output_weight1 = signal_output_quantile[['annual_return_sp','win_rate_sp','pc_ratio_sp']].loc[0.5].loc['annual_return_sp'] < signal_output['annual_return_sp']
signal_output['annual_return_sp_weight'] = signal_output_weight1.replace({True : 1, False : 0})

signal_output_weight2 = signal_output_quantile[['annual_return_sp','win_rate_sp','pc_ratio_sp']].loc[0.5].loc['win_rate_sp'] < signal_output['win_rate_sp']
signal_output['win_rate_sp_weight'] = signal_output_weight2.replace({True : 1, False : 0})

signal_output_weight3 = signal_output_quantile[['annual_return_sp','win_rate_sp','pc_ratio_sp']].loc[0.5].loc['pc_ratio_sp'] < signal_output['pc_ratio_sp'] 
signal_output['pc_ratio_sp_weight'] = signal_output_weight3.replace({True : 1, False : 0})


signal_output['Max_weight'] = signal_output[['annual_return_sp_weight','win_rate_sp_weight','pc_ratio_sp_weight']].sum(axis = 1)

signal_output.sort_values(by = 'Max_weight' ,axis = 0 , ascending = False, inplace = True) # 注意

# 选出Top1 

signal_output

 
