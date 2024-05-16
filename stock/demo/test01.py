import pandas as pd
import numpy as np
import akshare as ak
pd.set_option('display.max_columns', 1000)
pd.set_option('display.width', 1000)
pd.set_option('display.max_colwidth', 1000)

rename_columns = ['date', 'open', 'close', 'high', 'low', 'volume']
df = ak.stock_zh_a_hist('300059', adjust="qfq", period="daily").iloc[:, :6]

df.columns = rename_columns
# print(df)
df = df.iloc[-250:, :6]

df['date'] = pd.to_datetime(df['date'])
df.set_index("date", inplace=True)
# df.drop(columns=['index'], inplace=True)
df['250'] = df.close.rolling(250).mean()
print(df)
mean_250 = df.iloc[-1, 5]
close = df.iloc[-1, 1]
print(mean_250,close)