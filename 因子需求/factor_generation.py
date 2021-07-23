# -*- coding: utf-8 -*-
"""
Created on Tue Jul 13 15:32:35 2021

@author: liuyu
"""

import pandas as pd

#生成预测目标信号，未来两日开盘价连续下跌！
def y_generation(df):
    
    df['50ETF-open-1'] = df['50ETF-open'].shift(-1)
    df['50ETF-open-2'] = df['50ETF-open'].shift(-2)
    df['y'] = df.apply(lambda X: 1 if (X['50ETF-open']>X['50ETF-open-1'])&(X['50ETF-open-1']>X['50ETF-open-2']) else 0,axis=1)
    
    return (list(df['y']))

#生成因子：开盘价跌破昨日N日均价一定thresh
def open_below_ma(df,var,n,thresh=0):
    
    df['ma'] = df[var+'-close'].rolling(n).mean().shift(1)
    df['x'] = df.apply(lambda X: 1 if (X[var+'-open']<X['ma']*(1-thresh)) else 0,axis=1)
    
    return (list(df['x']))

#生成因子：收盘价跌破昨日N日均价一定thresh
def close_below_ma(df,var,n,thresh=0):
    
    df['ma'] = df[var+'-close'].rolling(n).mean()
    df['x'] = df.apply(lambda X: 1 if (X[var+'-close']<X['ma']*(1-thresh)) else 0,axis=1).shift(1)
    
    return (list(df['x']))

#生成因子：跌破昨日布林带下界
def open_below_boll(df,var,n=20,thresh=0):

    df['ma'] = df[var+'-close'].rolling(n).mean().shift(1)
    df['std']= df[var+'-close'].rolling(n).std().shift(1)
    df['boll_lower'] = df['ma'] - 2*df['std']
    
    df['x'] = df.apply(lambda X: 1 if (X[var+'-open']<X['boll_lower']*(1-thresh)) else 0,axis=1)
    
    return (list(df['x']))       

#生成因子：跌破昨日布林带下界
def close_below_boll(df,var,n=20,thresh=0):

    df['ma'] = df[var+'-close'].rolling(n).mean().shift(1)
    df['std']= df[var+'-close'].rolling(n).std().shift(1)
    df['boll_lower'] = df['ma'] - 2*df['std']
    
    df['x'] = df.apply(lambda X: 1 if (X[var+'-close']<X['boll_lower']*(1-thresh)) else 0,axis=1)
    
    return (list(df['x'])) 

#生成因子：跌破昨日BBI下界
def open_below_bbi(df,thresh=0):

    df['ma_3'] = df['50ETF-close'].rolling(3).mean().shift(1)
    df['ma_6']= df['50ETF-close'].rolling(6).mean().shift(1)
    df['ma_12'] = df['50ETF-close'].rolling(12).mean().shift(1)
    df['ma_24']= df['50ETF-close'].rolling(24).mean().shift(1)
    
    df['bbi'] = (df['ma_3']+df['ma_6']+df['ma_12']+df['ma_24'])/4
    
    df['x'] = df.apply(lambda X: 1 if (X['50ETF-open']<X['bbi']*(1-thresh)) else 0,axis=1)
    
    return (list(df['x']))     

#生成因子：跌破昨日BBI下界
def close_below_bbi(df,thresh=0):

    df['ma_3'] = df['50ETF-close'].rolling(3).mean()
    df['ma_6']= df['50ETF-close'].rolling(6).mean()
    df['ma_12'] = df['50ETF-close'].rolling(12).mean()
    df['ma_24']= df['50ETF-close'].rolling(24).mean()
    
    df['bbi'] = (df['ma_3']+df['ma_6']+df['ma_12']+df['ma_24'])/4
    
    df['x'] = df.apply(lambda X: 1 if (X['50ETF-close']<X['bbi']*(1-thresh)) else 0,axis=1).shift(1)
    
    return (list(df['x']))   

#生成因子：连续下跌超N天
def close_dropdays(df,n):
    
    df['close_var'] = (df['50ETF-close'] - df['50ETF-close'].shift(1)).shift(1)
    df['is_drop'] = df.apply(lambda X: 1 if X['close_var']<0 else 0,axis=1)
    df['dropdays'] = df['is_drop'] * (df['is_drop'].groupby((df['is_drop'] != df['is_drop'].shift()).cumsum()).cumcount() + 1)
       
    df['x'] = df.apply(lambda X: 1 if (X['dropdays']>n) else 0,axis=1)
    
    return (list(df['x']))     

#生成因子：收盘价空头排列
def ma_sorting(df):

    df['ma_5'] = df['50ETF-close'].rolling(5).mean()
    df['ma_10']= df['50ETF-close'].rolling(10).mean()
    df['ma_20'] = df['50ETF-close'].rolling(20).mean()
    df['ma_30']= df['50ETF-close'].rolling(30).mean()
       
    df['x'] = df.apply(lambda X: 1 if ((X.ma_5<X.ma_10)&(X.ma_10<X.ma_20)&(X.ma_20<X.ma_30)) else 0,axis=1).shift(1)
    
    return (list(df['x']))    

#生成因子：麦克指标弱支撑
def mike_ws(df,n=12):

    df['typ'] = ((df['50ETF-close']+df['50ETF-high']+df['50ETF-low'])/3).shift(1)
    df['mike_ws'] = 2 * df['typ'] - df['50ETF-close'].shift(1).rolling(n).max()
      
    df['x'] = df.apply(lambda X: 1 if (X['50ETF-open']<X['mike_ws']) else 0,axis=1)
    
    return (list(df['x']))   

#生成因子：出现N日极大值M日窗口
def window_max(df,var,n,m):

    df['n_max'] = df[var+'-close'].rolling(n).max()
      
    df['is_n_max'] = df.apply(lambda X: 1 if (X['n_max'] == X[var+'-close']) else 0,axis=1)
    df['n_max_m_window'] = df['is_n_max'].rolling(m).sum()
    
    df['x'] = df.apply(lambda X: 1 if ( X.n_max_m_window>0) else 0, axis=1).shift(1)
    
    return (list(df['x']))  

def factor_generation(df,date):
    #添加当天数据行
    df = df.append({'trade_date':date},ignore_index=True)
    
    df['Y'] = y_generation(df)
    df['前日收盘价跌破过去5日均价'] = close_below_ma(df,'50ETF',5)
    df['前日收盘价跌破过去15日均价'] = close_below_ma(df,'50ETF',15)
    df['前日收盘价跌破过去30日均价'] = close_below_ma(df,'50ETF',30)
    df['前日收盘价跌破过去5日均价3%'] = close_below_ma(df,'50ETF',5,0.03)
    df['前日收盘价跌破过去15日均价3%'] = close_below_ma(df,'50ETF',15,0.03)
    df['前日收盘价跌破过去30日均价3%'] = close_below_ma(df,'50ETF',30,0.03)
    df['前日收盘价-昨日布林带下界'] = close_below_boll(df,'50ETF')
    df['前日收盘价-昨日BBI'] = close_below_bbi(df)
    df['前日收盘价-昨日BBI大于3%'] = close_below_bbi(df,0.03)
    df['连跌天数大于3日'] = close_dropdays(df,3)
    df['连跌天数大于2日'] = close_dropdays(df,2)
    df['前日收盘价均线空头排列'] = ma_sorting(df)
    df['麦克指标弱支撑'] = mike_ws(df)
    df['SPX收盘跌破5日均价'] = close_below_ma(df,'SPX',5)
    df['SPX收盘跌破5日均价3%'] = close_below_ma(df,'SPX',5,0.03)
    df['SPX收盘跌破15日均价'] = close_below_ma(df,'SPX',15)
    df['SPX收盘跌破15日均价3%'] = close_below_ma(df,'SPX',15,0.03)   
    df['SPX收盘价-布林带下界'] = close_below_boll(df,'SPX')    
    df['VIX出现30日区间极大值'] = window_max(df,'VIX',30,1)
    df['VIX出现45日区间极大值'] = window_max(df,'VIX',45,1)    
    df['VIX30日区间极大值5日窗口'] = window_max(df,'VIX',30,5)
    df['VIX45日区间极大值5日窗口'] = window_max(df,'VIX',45,5)   
    df['VIX30日区间极大值10日窗口'] = window_max(df,'VIX',30,10)
    df['VIX45日区间极大值10日窗口'] = window_max(df,'VIX',45,10)   
    
    #df.dropna(how='any',inplace=True)
    #切片长度？
    df = df.tail(150)
    
    df.to_excel('./input_data/factor_data.xlsx',index=False)
    
    columns = ['trade_date','Y',
               '前日收盘价跌破过去5日均价',
               '前日收盘价跌破过去15日均价',
               '前日收盘价跌破过去30日均价',
               '前日收盘价跌破过去5日均价3%',
               '前日收盘价跌破过去15日均价3%',
               '前日收盘价跌破过去30日均价3%',
               '前日收盘价-昨日布林带下界',
               '前日收盘价-昨日BBI',
               '前日收盘价-昨日BBI大于3%',
               '连跌天数大于3日',
               '连跌天数大于2日',
               '前日收盘价均线空头排列',
               '麦克指标弱支撑',
               'SPX收盘跌破5日均价',
               'SPX收盘跌破5日均价3%',
               'SPX收盘跌破15日均价',
               'SPX收盘跌破15日均价3%',
               'SPX收盘价-布林带下界',
               'VIX出现30日区间极大值',
               'VIX出现45日区间极大值',
               'VIX30日区间极大值5日窗口',
               'VIX30日区间极大值10日窗口',
               'VIX45日区间极大值5日窗口',
               'VIX45日区间极大值10日窗口']
    '''
               '北向资金净流出天数大于3日',
               '北向资金净流出天数大于2日',
               '前一日认沽认购比例大于0.9',
               '前一日认沽认购比例大于1',
               '前一日认沽认购比例大于1.1']

    '''
    model_data = df[columns]
    model_data['sec_code'] = '510050.XSHG'
    model_data.to_csv('./input_data/model_input.csv',encoding='utf_8_sig',index=False)
        
    result = '因子处理完成'
    print('========'+result+'========')
    return(result)
    
    
if __name__ == '__main__':       

    input_data = pd.read_excel('./input_data/input_data.xlsx')
    factor_generation(input_data,date)











