import pandas as pd
import numpy as np
import akshare as ak

# 处理时间
from dateutil.parser import parse
from datetime import datetime, timedelta

select_65_zt_stock = []
trade_date = ak.tool_trade_date_hist_sina()
# print(trade_date)
trade_date = trade_date['trade_date'].apply(lambda x: x.strftime('%Y%m%d'))
d1 = datetime.now().strftime('%Y%m%d')
trade_date = np.array(trade_date)
print(trade_date)
n1 = np.argwhere(trade_date == str(d1))[0][0] + 1
print(n1)
# 获取最近6年的交易日行情
dates = trade_date[n1 - 65:n1]
print(dates)

print(ak.stock_zt_pool_em('20240422'))
# for date in dates:
#     try:
#         zt_pool = ak.stock_zt_pool_em(date)
#         select_65_zt_stock.extend(zt_pool['代码'].values)
#     except:
#         print("dates error: ",date)

select_65_zt_stock = list(set(select_65_zt_stock))
print(select_65_zt_stock)
