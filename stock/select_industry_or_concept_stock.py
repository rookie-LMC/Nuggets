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
akshare API
https://akshare.akfamily.xyz/data/stock/stock.html

简单选股脚本
https://blog.csdn.net/qq_46363011/article/details/128764258
'''

'''
全局信息
'''
#### print设置
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

#### 全局变量
debug_num = 100000
sleep_time_circulating = 0.5
sleep_time_day_week_month_info = 0.5
action_date = dt.date.today()

#### 过滤
stock_black_list = []
words_black_list = ['st', 'ST', 'sT', 'St', '酒']
concept_select_list = []
industry_select_list = ['物流行业', '家电行业']
concept_stock_list = []
industry_stock_list = []

#### 召回
# 流通股本
circulating_stock_max = 100000000 * 30

'''
01 a股股票列表
'''
stock_list = ak.stock_zh_a_spot_em()
stock_symbol = stock_list['代码'].values
stock_name = stock_list['名称'].values
stocks_code = list(zip(stock_symbol, stock_name))
# export_A_stocks(stock_list, action_date)
print('**** 01 股票共计:', len(stocks_code))

'''
02 过滤 关键字
'''
for i in range(len(stocks_code)):
    tmp_symbol, tmp_name = stocks_code[i][0], stocks_code[i][1]
    for word in words_black_list:
        if word in tmp_name:
            stock_black_list.append(tmp_symbol)
            break
stock_black_list = list(set(stock_black_list))
print('**** 02 过滤 关键字 数量: ', len(stock_black_list))

'''
02 过滤 执行
'''
stocks_code = [i for i in stocks_code if i[0] not in stock_black_list]
print('**** 02 过滤后 个股数量 : ', len(stocks_code), ', 过滤数量: ', len(stock_black_list))

'''
03 召回 概念
'''
concept_list = ak.stock_board_concept_name_em()
# 检查概念是否存在
for name in concept_select_list:
    if name not in concept_list['板块名称'].values:
        print(f"未找到概念名称'{name}'，请检查输入是否正确。")
        continue
    concept_stocks = ak.stock_board_concept_cons_em(name)
    print('**** 03 召回 概念: ', name, ': ', len(concept_stocks['代码'].values))
    concept_stock_list = list(set(concept_stock_list) | set(concept_stocks['代码'].values))

'''
03 召回 行业
'''
industry_list = ak.stock_board_industry_name_em()
# 检查行业是否存在
for name in industry_select_list:
    if name not in industry_list['板块名称'].values:
        print(f"未找到行业名称'{name}'，请检查输入是否正确。")
        continue
    industry_stock = ak.stock_board_industry_cons_em(name)
    print('**** 03 召回 行业: ', name, ': ', len(industry_stock['代码'].values))
    industry_stock_list = list(set(industry_stock_list) | set(industry_stock['代码'].values))

stocks_code = [i for i in stocks_code if i[0] in concept_stock_list + industry_stock_list]
print('**** 03 召回 个股数量 : ', len(stocks_code), ', 过滤数量: ', len(stock_black_list))

'''
02 过滤 流通股份要在30亿以下
'''
select_stock_circulating_stock = []
for i in range(min(len(stocks_code), debug_num)):
    print('**** load stock_circulate : ', stocks_code[i][0])
    circulating_stock = ak.stock_individual_info_em(stocks_code[i][0]).iloc[7, 1]
    time.sleep(sleep_time_circulating)
    if (circulating_stock == '-'): continue
    try:
        if (circulating_stock <= circulating_stock_max):
            select_stock_circulating_stock.append(stocks_code[i][0])
    except:
        print('**** has no stock_circulate : ', stocks_code[i][0])

stocks_code = [i for i in stocks_code if i[0] in select_stock_circulating_stock]
print('**** 02 过滤 流通股份 个股数量 : ', len(stocks_code), ', 流通股份30亿以下数量: ',
      len(set(select_stock_circulating_stock)))

'''
03 召回
个股日线、周线、月线
'''
print('*' * 50 + ' 03 召回数据')
stock_daily, stock_weekly, stock_monthly = {}, {}, {}
for i in range(min(len(stocks_code), debug_num)):
    print('**** load K line : ', stocks_code[i][0])
    stock_daily[stocks_code[i][0]] = ak.stock_zh_a_hist(stocks_code[i][0], adjust="qfq", period="daily",
                                                        start_date='20220101')
    stock_weekly[stocks_code[i][0]] = ak.stock_zh_a_hist(stocks_code[i][0], adjust="qfq", period="weekly",
                                                         start_date='20220101')
    stock_monthly[stocks_code[i][0]] = ak.stock_zh_a_hist(stocks_code[i][0], adjust="qfq", period="monthly",
                                                          start_date='20220101')
    time.sleep(sleep_time_day_week_month_info)
print('*' * 50 + ' 03 召回数据完毕')

'''
04 策略 月线三根，阳-阴-阳，上升趋势
股票趋势波段分析
https://zhuanlan.zhihu.com/p/669747150
'''
print('*' * 50 + ' 04 策略 月线三根筛选')
select_stock_three_K_monthly = []
target_start, target_end = '2024-02-01', '2024-05-30'
rename_columns = ['date', 'open', 'close', 'high', 'low', 'volume']
for i in range(min(len(stocks_code), debug_num)):
    stock_df_3_k_m = stock_monthly[stocks_code[i][0]].iloc[:, :6]
    stock_df_3_k_m.columns = rename_columns
    stock_df_3_k_m.index = pd.to_datetime(stock_df_3_k_m['date'])
    stock_df_3_k_m = stock_df_3_k_m[target_start: target_end]
    # print(stock_df_3_k_m)
    # print('*' * 20)

    if selector_of_three_K_monthly(stock_df_3_k_m, stocks_code[i][0], 1, 2):
        select_stock_three_K_monthly.append(stocks_code[i][0])
stocks_code = [i for i in stocks_code if i[0] in select_stock_three_K_monthly]
print('**** 04 策略 月线三根 个股数量 : ', len(stocks_code))
print('*' * 50 + ' 04 策略 月线三根筛选完毕')

'''
04 策略 当月涨幅限制
'''
# print('*' * 50 + ' 月K线涨幅限制')
# select_stock_K_monthly_limit = []
# target_start, target_end = '2024-05-01', '2024-05-31'

'''
04 策略 股票要在250日均线上运行,且低于30。
'''
print('*' * 50 + ' 04 策略 250日均线+股价30')
select_mean_250_up_stock = []
rename_columns = ['date', 'open', 'close', 'high', 'low', 'volume']
mean_times = 250
close_max = 30
for i in range(min(len(stocks_code), debug_num)):
    df = stock_daily[stocks_code[i][0]].iloc[:, :6]
    df.columns = rename_columns
    df = df.iloc[-1 * mean_times:, :6]

    if (len(df['date'].values) < mean_times): continue

    df['date'] = pd.to_datetime(df['date'])
    df.set_index("date", inplace=True)
    df[str(mean_times)] = df.close.rolling(mean_times).mean()
    mean_250, close = df.iloc[-1, 5], df.iloc[-1, 1]
    if (mean_250 == '-' or close == '-'): continue

    try:
        # if (close >= mean_250 and close <= close_max):
        if (close >= mean_250):
            select_mean_250_up_stock.append(stocks_code[i][0])
    except:
        print('**** has no mean : ', stocks_code[i][0])

stocks_code = [i for i in stocks_code if i[0] in select_mean_250_up_stock]
print('**** 04 策略 250日均线+股价30 个股数量 : ', len(stocks_code))
print('*' * 50 + ' 04 策略 250日均线+股价30')

'''
04 策略 过去65天出现过涨停
akshare分析涨停板股票数据，只有20天数据，手动积累中
https://blog.csdn.net/qq_26742269/article/details/122824457
'''
print('*' * 50 + ' 04 策略 过去65天出现过涨停')
select_stock_65_zt = []
zt_days, zt_thres = 65, 9.9
for i in range(min(len(stocks_code), debug_num)):
    df = stock_daily[stocks_code[i][0]].iloc[-1 * zt_days:, -3]
    try:
        if (len(df) != zt_days): continue
        if (max(df) > zt_thres): select_stock_65_zt.append(stocks_code[i][0])
    except:
        print('**** has no zt : ', stocks_code[i][0])
stocks_code = [i for i in stocks_code if i[0] in select_stock_65_zt]
print('**** 04 策略 过去65天出现过涨停 个股数量 : ', len(stocks_code))
print('*' * 50 + ' 04 策略 过去65天出现过涨停 结束')

'''
筛选结果
'''
print('*' * 50 + ' 筛选结果')
for i in range(len(stocks_code)):
    print(stocks_code[i][0], stocks_code[i][1])

'''
保存结果
'''
# with open('./select_result/' + str(action_date), 'w') as f:
#     for i in range(len(stocks_code)):
#         f.write(export_select_stocks(stocks_code[i][0], stocks_code[i][1]) + '\n')
