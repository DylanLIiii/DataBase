import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt



input_data = pd.read_excel('/Users/dylan/DataBase/signal_process/50ETF-signalout copy.xlsx')
signal_output = pd.read_excel('/Users/dylan/DataBase/signal_process/signal_result-30 copy.xlsx')

signal_output_quantile = signal_output[['annual_return_sp','win_rate_sp','pc_ratio_sp']].quantile([0.25,0.5,0.75])

def get_weight_group(x) :
    if x < signal_output_quantile[methods].loc[0.25].loc[methods.iloc[i]]: 
        return 1
    elif signal_output_quantile[methods].loc[0.25].loc[methods.iloc[i]] < x < signal_output_quantile[methods].loc[0.5].loc[methods.iloc[1]]: 
        return 2 
    elif signal_output_quantile[methods].loc[0.5].loc[methods.iloc[i]] < x < signal_output_quantile[methods].loc[0.75].loc[methods.iloc[1]] : 
        return 3         
    else : 
        return 4
    signal_output['Max_weight'] = signal_output[methods].iloc[:,0].map(get_weight_group).sum(axis = 1)