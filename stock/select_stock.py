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
#### print设置
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

#### 时间和日期
start = time.perf_counter()
action_date = dt.date.today()

#### 获取a股列表
stock_list = ak.stock_zh_a_spot_em()
# print(stock_list)
stock_symbol = stock_list['代码'].values
stock_name = stock_list['名称'].values
stocks_code = list(zip(stock_symbol, stock_name))
# export_A_stocks(stock_list, action_date)
print('**** 股票共计:', len(stocks_code))

#### 个股黑名单
stock_black_list = []

'''
关键字个股
'''
words_black_list = ['st', 'ST', 'sT', 'St']
for i in range(len(stocks_code)):
    tmp_symbol, tmp_name = stocks_code[i][0], stocks_code[i][1]
    for word in words_black_list:
        if word in tmp_name:
            stock_black_list.append(tmp_symbol)
            break
print('**** 剔除关键字数量: ', len(set(stock_black_list)))

'''
概念黑名单
'''
#### 剔除概念
concept_black_list = []
concept_list = ak.stock_board_concept_name_em()
# 检查指定概念是否存在
for name in concept_black_list:
    if name not in concept_list['板块名称'].values:
        print(f"未找到概念名称'{name}'，请检查输入是否正确。")
        continue
    concept_stocks = ak.stock_board_concept_cons_em(name)
    print('**** 黑名单概念 ', name, ': ', len(concept_stocks['代码'].values))
    stock_black_list = list(set(stock_black_list) | set(concept_stocks['代码'].values))

'''
行业黑名单
'''
industry_black_list = ['房地产服务', '房地产开发']
industry_list = ak.stock_board_industry_name_em()
# 检查指定行业是否存在
for name in industry_black_list:
    if name not in industry_list['板块名称'].values:
        print(f"未找到行业名称'{name}'，请检查输入是否正确。")
        continue
    industry_stock = ak.stock_board_industry_cons_em(name)
    print('**** 黑名单行业 ', name, ': ', len(industry_stock['代码'].values))
    stock_black_list = list(set(stock_black_list) | set(industry_stock['代码'].values))

'''
剔除
'''
stocks_code = [i for i in stocks_code if i[0] not in stock_black_list]
print('**** 黑名单行业后 : ', len(stocks_code), len(set(stock_black_list)))

'''
股价要在30元以下，流通股份要在30亿以下
'''
select_stock_circulating_stock = []
circulating_stock_max = 100000000 * 30
for i in range(min(len(stocks_code), 1)):
    circulating_stock = ak.stock_individual_info_em(stocks_code[i][0]).iloc[7, 1]
    if (circulating_stock <= circulating_stock_max):
        select_stock_circulating_stock.append(stocks_code[i][0])

'''
过去65天出现过涨停
akshare分析涨停板股票数据
https://blog.csdn.net/qq_26742269/article/details/122824457
'''
## 积累数据中

'''
个股日线、周线、月线
'''
print('*' * 50 + ' 加载数据')
print(stocks_code[:10])
stock_daily, stock_weekly, stock_monthly = {}, {}, {}
for i in range(min(len(stocks_code), 1)):
    print('**** load : ', stocks_code[i][0])
    stock_daily[stocks_code[i][0]] = ak.stock_zh_a_hist(stocks_code[i][0], adjust="qfq", period="daily")
    stock_weekly[stocks_code[i][0]] = ak.stock_zh_a_hist(stocks_code[i][0], adjust="qfq", period="weekly")
    stock_monthly[stocks_code[i][0]] = ak.stock_zh_a_hist(stocks_code[i][0], adjust="qfq", period="monthly")

'''
月线三根
股票趋势波段分析
https://zhuanlan.zhihu.com/p/669747150
'''
# print('*' * 50 + ' 月线三根筛选')
# select_stock_three_K_monthly = []
# target_start, target_end = '2024-02-01', '2024-04-30'
# rename_columns = ['date', 'open', 'close', 'high', 'low', 'volume']
# for i in range(min(len(stocks_code), 100)):
#     stock_df_3_k_m = stock_monthly[stocks_code[i][0]].iloc[:, :6]
#     stock_df_3_k_m.columns = rename_columns
#     stock_df_3_k_m.index = pd.to_datetime(stock_df_3_k_m['date'])
#     stock_df_3_k_m = stock_df_3_k_m[target_start: target_end]
#     # print(stock_df_3_k_m)
#     # print('*' * 20)
#
#     if selector_of_three_K_monthly(stock_df_3_k_m, stocks_code[i][0], 1, 2):
#         select_stock_three_K_monthly.append(stocks_code[i][0])
# print(select_stock_three_K_monthly)

'''
当月 月K线涨幅限制
'''
# print('*' * 50 + ' 月K线涨幅限制')
# select_stock_K_monthly_limit = []
# target_start, target_end = '2024-05-01', '2024-05-31'


'''
股票要在250日均线上运行。
'''
select_mean_250_up_stock = []
rename_columns = ['date', 'open', 'close', 'high', 'low', 'volume']
mean_times = 250
for i in range(min(len(stocks_code), 1)):
    df = stock_daily[stocks_code[i][0]].iloc[:, :6]
    df.columns = rename_columns
    df = df.iloc[-1 * mean_times:, :6]
    if (len(df['date'].values) < mean_times): continue

    df['date'] = pd.to_datetime(df['date'])
    df.set_index("date", inplace=True)
    df[str(mean_times)] = df.close.rolling(mean_times).mean()
    mean_250 = df.iloc[-1, 5]
    close = df.iloc[-1, 1]
    if (close >= mean_250):
        select_mean_250_up_stock.append(stocks_code[i][0])
