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

debug_num = 20000000000000000
# action_date = dt.date.today()
action_date = '2025-01-13'
save_file = 'stock_A_2025_01_13'
stocks_code =[('603269', '海鸥股份'), ('688426', '康为世纪'), ('002851', '麦格米特'), ('300684', '中石科技'), ('603893', '瑞芯微'), ('605333', '沪光股份'), ('603016', '新宏泰'), ('605318', '法狮龙')]


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
stocks_code_industry_concept = {}
for i in range(min(len(stocks_code), debug_num)):
    stock_data = stock_daily[stocks_code[i][0]][['日期', '涨跌幅']]
    win_rate_list.append(stock_data.iloc[-1, 1])
    stocks_code_industry_concept[stocks_code[i][0]] = [[], [], stock_data.iloc[-1, 1], stocks_code[i][1]]

industry_list = ak.stock_board_industry_name_em()
concept_list = ak.stock_board_concept_name_em()

for name in list(industry_list['板块名称']):
    industry_stock = ak.stock_board_industry_cons_em(name)
    for i in range(min(len(stocks_code), debug_num)):
        if stocks_code[i][0] in list(industry_stock['代码']):
            stocks_code_industry_concept[stocks_code[i][0]][0].append(name)

for name in list(concept_list['板块名称']):
    concept_stocks = ak.stock_board_concept_cons_em(name)
    for i in range(min(len(stocks_code), debug_num)):
        if stocks_code[i][0] in list(concept_stocks['代码']):
            stocks_code_industry_concept[stocks_code[i][0]][1].append(name)

print('*' * 20 + ' 明细情况')
print('*' * 20 + ' 分析日期: ', action_date, ', 读取文件夹', save_file)

# for i in range(min(len(stocks_code), debug_num)):
#     print(stocks_code[i][0], stocks_code[i][1],
#           ' , 涨跌幅:', stocks_code_industry_concept[stocks_code[i][0]][2],
#           ' , 行业:', stocks_code_industry_concept[stocks_code[i][0]][0],
#           ' , 概念:', stocks_code_industry_concept[stocks_code[i][0]][1])

stocks_code_sorted = dict(sorted(stocks_code_industry_concept.items(),
                                 key=lambda item: item[1][2],
                                 reverse=True))
for key, val in stocks_code_sorted.items():
    print(key, val[3], ' ,涨跌幅:', val[2], ' ,行业:', val[0], ' ,概念:', val[1])

print('*' * 20 + ' 胜率情况')
win_num = len([1 for i in win_rate_list if i > 0])
print(win_num, len(win_rate_list), win_num / len(win_rate_list))
