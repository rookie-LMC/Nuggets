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

debug_num = 200000000000
# action_date = dt.date.today()
action_date = '2024-12-16'
save_file = 'stock_HK_2024_12_16'
stocks_code = [('00293', '国泰航空'), ('01478', '丘钛科技'), ('01896', '猫眼娱乐')]

stock_daily, stock_weekly, stock_monthly = {}, {}, {}
for i in range(min(len(stocks_code), debug_num)):
    try:
        # print('**** load K line : ', stocks_code[i][0])
        stock_daily[stocks_code[i][0]], stock_weekly[stocks_code[i][0]], stock_monthly[stocks_code[i][0]] = \
            load_stocks(save_file, action_date, stocks_code[i][0])

        # print(stock_daily[stocks_code[i][0]][['日期', '收盘', '成交量']])
        # print(stock_weekly[stocks_code[i][0]][['日期', '收盘', '成交量']])
        # print(stock_monthly[stocks_code[i][0]][['日期', '收盘', '成交量']])
    except:
        print('**** has no day week month K line: ', stocks_code[i][0])
print('*' * 50 + ' 03 召回数据完毕')

win_rate_list = []
for i in range(min(len(stocks_code), debug_num)):
    stock_data = stock_daily[stocks_code[i][0]][['日期', '涨跌幅']]
    print(stocks_code[i][0], stocks_code[i][1], stock_data.iloc[-1, 1])
    win_rate_list.append(stock_data.iloc[-1, 1])

print('*' * 20 + ' 胜率情况')
win_num = len([1 for i in win_rate_list if i > 0])
print(win_num, len(win_rate_list), win_num / len(win_rate_list))
