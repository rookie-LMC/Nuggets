import time
import akshare as ak
import numpy as np
from numpy import empty
import pandas as pd
import datetime as dt

#### print设置
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

df = ak.stock_zh_a_hist('300093', adjust="qfq", period="daily").iloc[-65:, -3]
print(max(df))