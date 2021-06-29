import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def cal_signal(methods,try_window,select_number) :
    """This is a function

    Args:
        methods ([string]): A list
        try_window ([integer]): the number of try_window
        select_number ([intrger]): the number of model_select

    Returns:
        [excel doc]: Excel doc contains model_selected for next window
    """    
    input_data = pd.read_excel(r'D:\Github repo\DataBase\signal_process\50-ETF-signalout.xlsx')
    signal_input = pd.read_excel(r'\Github repo\DataBase\signal_process\signal_result-'+ str(try_window) +' copy.xlsx') 
    input_data.dropna(axis = 1, inplace= True)
    # 加权处理，取四分位数进行分权
    signal_input_quantile = signal_input[methods].quantile([0.25,0.5,0.75])
    for col_name in methods:
        def get_weight_group(x) :
            # 加权处理函数
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
    signal_input['Max_method'] = signal_input[methods].sum(axis = 1)
    signal_input['Max_method'].sort_values(ascending = False)
    # 选出当期Top
    signal_input_filter = signal_input.groupby(by = 'start_date').apply(lambda x : x.nlargest(3, 'Max_method', keep = 'first'))
    # 在Top中进行随机选择
    signal_output = pd.DataFrame()
    for i in signal_input_filter['start_date'].drop_duplicates(): 
        column = signal_input_filter.loc[(i)].sample(select_number)
        signal_output = signal_output.append(column)
        signal_output['model_selected'] = signal_output['model'].shift(1)
        
    signal_output.to_excel(r'D:\Github repo\DataBase\signal_process\signal_output.xlsx')
        
    
