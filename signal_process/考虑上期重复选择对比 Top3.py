import pandas as pd
input_data = pd.read_excel(
    '/Users/dylan/Desktop/signal_process/input_data/50ETF-signalout.xlsx')
signal_input = pd.read_excel('/Users/dylan/Desktop/signal_process/input_data/signal_result-30.xlsx')
# 按照当期method保留至少前三的模型
signal_input['max_method'] = signal_input.groupby("start_date")["annual_return_op"].transform('max')  # [method] 表示对method column进行max操作
signal_input_fliter1 = signal_input.nlargest(3, 'max_method', keep="all")
# signal_input['max_win_rate_sp']'] = signal_input.groupby("start_date")['win_rate_sp'].transform('max')
# 本期相同则计算对应上期method
if len(signal_input['max_method']) > 3:
    signal_input_fliter1.sort_values(by=['model', 'start_date'],inplace=True)
    signal_input_fliter1['last_method'] = signal_input_fliter1["annual_return_op"].shift(1)  # 错期过,现在对应
    signal_output = signal_input_fliter1.nlargest(3,'last_method', keep="first")
else:
    signal_output = signal_input_fliter1.sort_values(by="start_date")
# 对选择的三个模型进行Voting
# 
signal_output.to_excel("/Users/dylan/DataBase/1.xlsx",index="False",sheet_name = "Sheet1")
