import pandas as pd


def cal_signal(training_window,method,select_num=3):
    
    input_data = pd.read_excel('./input_data/50ETF-signalout.xlsx')
    signal_input = pd.read_excel('./input_data/signal_result-'+str(training_window)+'.xlsx')        
    
    tmp_signal_name = 'top' + str(select_num) + '-' + method + '-' + str(training_window)
    
    #按照当期method保留至少前三的模型
    signal_input['Max_method'] = signal_input.groupby("start_date")[method].transform('max') # [method] 表示对method column进行max操作
    signal_input_fliter1 = signal_input.nlargest(3,'Max_method',keep = "all")
    #signal_input['max_win_rate_sp']'] = signal_input.groupby("start_date")['win_rate_sp'].transform('max')
    #本期相同则计算对应上期method
    if len(signal_input['Max_method']) > 3:       
        signal_input_fliter1.sort_values(by=['model','start_date'],inplace=True) 
        signal_input_fliter1['Last_emthod'] = signal_input_fliter1[method].shift(1) # 错期过,现在对应
        signal_input_fliter1.nlargest(3,'Last_emthod',keep="first")
        signal_output = signal_input_fliter1.sort_values(by="start_date").shift(1)
    else:
        signal_output = signal_input_fliter1.sort_values(by="start_date").shift(1)
    # 对选出的Top3进行Voting

    signal_input_filter.sort_values(by='start_date',inplace=True)
    signal_input_filter['model_selected'] = signal_input_filter['model'].shift(1)
    
    signal_input_filter.to_excel('./input_data/signal_roll/'+tmp_signal_name+'.xlsx',index=False)
    
    input_data[tmp_signal_name] = 0
    for i in range(len(input_data)):
        tmp_trade_date = input_data['trade_date'].iloc[i]
        try:
            tmp_model = signal_input_filter[(signal_input_filter['start_date']<=tmp_trade_date)&(signal_input_filter['end_date']>=tmp_trade_date)]['model_selected'].iloc[0]
            input_data[tmp_signal_name].iloc[i] = input_data[tmp_model].iloc[i]
        except:
            continue
    
    input_data.to_excel('./input_data/50ETF-signalout.xlsx',index=False)
    result = tmp_signal_name + '信号处理完成'
    print(result)
    return(result)  
