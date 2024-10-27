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

a = ak.stock_zh_a_hist_min_em(symbol='300286', start_date="2024-06-01 09:32:00", period='60')
zs = ak.stock_zh_index_hist_csindex(symbol='399106', start_date="20240526", end_date="22220525")
print(zs)
