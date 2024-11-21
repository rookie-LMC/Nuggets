'''
akshare API
https://akshare.akfamily.xyz/data/stock/stock.html

简单选股脚本
https://blog.csdn.net/qq_46363011/article/details/128764258
'''

import time
import akshare as ak
import numpy as np
from numpy import empty
import pandas as pd
import datetime as dt

# 处理时间
from dateutil.parser import parse
from datetime import datetime, timedelta
from chinese_calendar import is_workday, is_holiday

from utils_stock import *

'''
全局参数
'''
debug_num = 2000000000
sleep_time_day_week_month_info = 0.3
# action_date = dt.date.today()
action_date = '2024-11-04'
start_date = '20230101'
mean_times_1 = 19
mean_times_2 = 5
'''
01 港股通成份股
'''
stock_list = ak.stock_hk_ggt_components_em()
stock_symbol = stock_list['代码'].values
stock_name = stock_list['名称'].values
stocks_code = list(zip(stock_symbol, stock_name))
# export_A_stocks(stock_list, action_date)
print('**** 01 股票共计:', len(stocks_code))
# print(stocks_code)


'''
03 召回
个股日线、周线、月线
'''
print('*' * 50 + ' 03 召回数据')
stock_daily, stock_weekly, stock_monthly = {}, {}, {}
for i in range(min(len(stocks_code), debug_num)):
    try:
        # print('**** load K line : ', stocks_code[i][0])

        stock_daily[stocks_code[i][0]], stock_weekly[stocks_code[i][0]], stock_monthly[stocks_code[i][0]] = load_stocks(
            action_date, stocks_code[i][0], field='hk')

        # print(stock_daily[stocks_code[i][0]][['日期', '收盘', '成交量']])
        # print(stock_weekly[stocks_code[i][0]][['日期', '收盘', '成交量']])
        # print(stock_monthly[stocks_code[i][0]][['日期', '收盘', '成交量']])
    except:
        print('**** has no day week month K line: ', stocks_code[i][0])
print('*' * 50 + ' 03 召回数据完毕')

for i in range(min(len(stocks_code), debug_num)):
    try:
        stock_data = stock_daily[stocks_code[i][0]][['日期', '收盘', '成交量']]

        df_1 = stock_data.iloc[-1 * mean_times_1:, :6]
        mean_times_max_val_1 = df_1['收盘'].max()
        mean_times_turnover_1 = df_1['成交量'].mean()

        df_2 = stock_data.iloc[-1 * mean_times_2:, :6]
        mean_times_max_val_2 = df_2['收盘'].max()
        mean_times_turnover_2 = df_2['成交量'].mean()

        last_val = stock_data.iloc[-1, 1]
        last_turnover = stock_data.iloc[-1, 2]

        # c_val_1 = last_val / mean_times_max_val_1 > 0.9
        # c_val_2 = last_val / mean_times_max_val_1 < 1.1
        # c_val_3 = last_val / mean_times_max_val_2 > 0.9
        # c_val_4 = last_val / mean_times_max_val_2 < 1.1

        c_turnover_1 = last_turnover / mean_times_turnover_1 > 1.3
        c_turnover_2 = last_turnover / mean_times_turnover_2 > 0.0

        # is_target = c_val_1 and c_val_2 and c_val_3 and c_val_4 and c_turnover_1 and c_turnover_2
        is_target = c_turnover_1 and c_turnover_2
        if (is_target):
            print("股票筛选: ", stocks_code[i][0], stocks_code[i][1])
    except:
        print('**** has no stock data K line: ', stocks_code[i][0])
