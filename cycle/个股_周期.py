'''
"""
Date: 2024/4/25 20:00
Desc: 首页-行情中心-涨停板行情-涨停股池
https://quote.eastmoney.com/ztb/detail#type=ztgc

涨停板行情专题为您展示了 6 个股票池，分别为：
1. 涨停股池：包含当日当前涨停的所有A股股票(不含未中断连续一字涨停板的新股)；
2. 昨日涨停股池：包含上一交易日收盘时涨停的所有A股股票(不含未中断连续一字涨停板的新股)；
3. 强势股池：包含创下60日新高或近期多次涨停的A股股票；
4. 次新股池：包含上市一年以内且中断了连续一字涨停板的A股股票；
5. 炸板股池：包含当日触及过涨停板且当前未封板的A股股票；
6. 跌停股池：包含当日当前跌停的所有A股股票。
注：涨停板行情专题统计不包含ST股票及科创板股票。

daily_limit_up_market
'''

import akshare as ak
import datetime as dt
from utils_cycle import *

trade_date = '20250110'

# 东方财富网-行情中心-涨停板行情-涨停股池
df_zt = ak.stock_zt_pool_em(date=trade_date)
# 东方财富网-行情中心-涨停板行情-昨日涨停股池
df_zt_pvs = ak.stock_zt_pool_previous_em(date=trade_date)
# 东方财富网-行情中心-涨停板行情-强势股池
df_zt_strong = ak.stock_zt_pool_strong_em(date=trade_date)
# 东方财富网-行情中心-涨停板行情-次新股池
df_zt_sn = ak.stock_zt_pool_sub_new_em(date=trade_date)
# 东方财富网-行情中心-涨停板行情-炸板股池
df_zt_zbgc = ak.stock_zt_pool_zbgc_em(date=trade_date)
# 东方财富网-行情中心-涨停板行情-跌停股池
df_zt_dtgc = ak.stock_zt_pool_dtgc_em(date=trade_date)

# 序号-代码-名称
# print(df_zt)
df_market = df_zt_strong
stock_zt_list = get_stocks_code(df_market)
print(stock_zt_list)
stocks_code_industry_concept = get_industry_and_concept_of_stocks(stock_zt_list)

industry_dic, concept_dic = group_and_sort(stocks_code_industry_concept)
print('* ' * 10, trade_date, '* ' * 10)
print(sorted(industry_dic.items(), key=lambda x: x[1], reverse=True))
print('* ' * 10, trade_date, '* ' * 10)
print(sorted(concept_dic.items(), key=lambda x: x[1], reverse=True))
