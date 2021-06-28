import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt



input_data = pd.read_excel('/Users/dylan/DataBase/signal_process/50ETF-signalout copy.xlsx')
signal_output = pd.read_excel('/Users/dylan/DataBase/signal_process/signal_result-30 copy.xlsx')

signal_output_quantile = signal_output[[['annual_return_sp','win_rate_sp','pc_ratio_sp']].quantile([0.25,0.5,0.75])


if signal_output_quantile[[['annual_return_sp','win_rate_sp','pc_ratio_sp']].loc[0.5] < signal_output[['annual_return_sp','win_rate_sp','pc_ratio_sp']] and signal_output[['annual_return_sp','win_rate_sp','pc_ratio_sp']] < signal_output_quantile[['annual_return_sp','win_rate_sp','pc_ratio_sp']].loc[0.75] :
    print
elif signal_output_quantile[['annual_return_sp','win_rate_sp','pc_ratio_sp']].loc[0.75] < signal_output[['annual_return_sp','win_rate_sp','pc_ratio_sp']] : 
    return 2
else :
    return 1


