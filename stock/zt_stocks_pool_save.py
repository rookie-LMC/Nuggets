import pandas as pd
import numpy as np
import akshare as ak

# 处理时间
from dateutil.parser import parse
from datetime import datetime, timedelta

# trade_date = ak.tool_trade_date_hist_sina()
# print(trade_date)
# trade_date = trade_date['trade_date'].apply(lambda x: x.strftime('%Y%m%d'))
#
# today = datetime.now().strftime('%Y%m%d')
# trade_date = np.array(trade_date)
# n1 = np.argwhere(trade_date == str(today))[0][0] + 1
# yesterday = trade_date[n1 - 2]
# print(today, yesterday)

yesterday='20240515'
df = ak.stock_zt_pool_em(yesterday)
df.to_excel('./zt_stocks_pool/zt_pool_' + yesterday + '.xlsx', sheet_name='A-stocks')
