import time
import akshare as ak
from numpy import empty
import pandas as pd
import datetime as dt
from chinese_calendar import is_workday, is_holiday

from utils_stock import *

'''
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
print('**** 代码共计:', len(stocks_code))

'''
剔除黑名单
'''
stock_black_list = []
#### 剔除概念
concept_black_list = ['民爆概念', '云游戏']
concept_list = ak.stock_board_concept_name_em()
# 检查指定概念是否存在
for name in concept_black_list:
    if name not in concept_list['板块名称'].values:
        print(f"未找到概念名称'{name}'，请检查输入是否正确。")
        continue
    concept_stocks = ak.stock_board_concept_cons_em(name)
    print('**** 黑名单概念 ', name, ': ', len(concept_stocks['代码'].values))
    stock_black_list = list(set(stock_black_list) | set(concept_stocks['代码'].values))

#### 剔除概念
industry_black_list = ['游戏', '教育']
industry_list = ak.stock_board_industry_name_em()
# 检查指定行业是否存在
for name in industry_black_list:
    if name not in industry_list['板块名称'].values:
        print(f"未找到行业名称'{name}'，请检查输入是否正确。")
        continue
    industry_stock = ak.stock_board_industry_cons_em(name)
    print('**** 黑名单 ', name, ': ', len(industry_stock['代码'].values))
    stock_black_list = list(set(stock_black_list) | set(industry_stock['代码'].values))

stocks_code = [i for i in stocks_code if i[0] not in stock_black_list]
print('**** 黑名单行业 : ', len(stock_black_list), stock_black_list)

print('**** 剔除黑名单后 : ', len(stocks_code))

'''
个股日线、周线、月线
'''
print('*' * 50 + ' 加载数据')
print(stocks_code[:10])
stock_daily, stock_weekly, stock_monthly = {}, {}, {}
for i in range(min(len(stocks_code), 100)):
    print('**** load : ', stocks_code[i][0])
    stock_daily[stocks_code[i][0]] = ak.stock_zh_a_hist(stocks_code[i][0], adjust="qfq", period="daily")
    stock_weekly[stocks_code[i][0]] = ak.stock_zh_a_hist(stocks_code[i][0], adjust="qfq", period="weekly")
    stock_monthly[stocks_code[i][0]] = ak.stock_zh_a_hist(stocks_code[i][0], adjust="qfq", period="monthly")

'''
股价要在30元以下，流通股份要在30亿以下
'''


'''
月线三根
股票趋势波段分析
https://zhuanlan.zhihu.com/p/669747150
'''
print('*' * 50 + ' 月线三根筛选')
select_stock_three_K_monthly = []
target_start, target_end = '2024-02-01', '2024-04-30'
rename_columns = ['date', 'open', 'close', 'high', 'low', 'volume']
for i in range(min(len(stocks_code), 100)):
    stock_df_3_k_m = stock_monthly[stocks_code[i][0]].iloc[:, :6]
    stock_df_3_k_m.columns = rename_columns
    stock_df_3_k_m.index = pd.to_datetime(stock_df_3_k_m['date'])
    stock_df_3_k_m = stock_df_3_k_m[target_start: target_end]
    # print(stock_df_3_k_m)
    # print('*' * 20)

    if selector_of_three_K_monthly(stock_df_3_k_m, stocks_code[i][0], 1, 2):
        select_stock_three_K_monthly.append(stocks_code[i][0])
print(select_stock_three_K_monthly)

'''
当月 月K线涨幅限制
'''
# print('*' * 50 + ' 月K线涨幅限制')
# select_stock_K_monthly_limit = []
# target_start, target_end = '2024-05-01', '2024-05-31'


'''
过去65天出现过涨停
'''


'''
股票要在250日均线上运行。
'''

