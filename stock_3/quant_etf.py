# 参考资料
# https://zhuanlan.zhihu.com/p/855997776
import akshare as ak
import pandas as pd
import bt
import time
import matplotlib.pyplot as plt

# 获取A股场内ETF行情数据
etf_df = ak.fund_etf_fund_daily_em()
print(etf_df)

# 关键字过滤
# black_words = ['纳斯达克', '海外', '房', '国债']
black_words = []
black_words_list = []

# 类型过滤
black_etf_type = []
black_etf_type_list = []

# 起始日期过滤
black_start_date_list = []

debug_num = 200000
sleep_time = 0.1
start_date = '20230101'
end_date = '20251231'
check_date = '2023-01-03'
etf_dic = {}

for i in range(min(debug_num, len(etf_df['基金代码']))):
    etf, etf_name, etf_type = etf_df.iloc[i, 0], etf_df.iloc[i, 1], etf_df.iloc[i, 2]

    is_black_words, is_black_etf_type = 0, 0
    # 关键字过滤
    for i in black_words:
        if i in etf_name:
            is_black_words = 1
            black_words_list.append([etf, etf_name, etf_type])
    # 类型过滤
    for i in black_etf_type:
        if i in etf_type:
            is_black_etf_type = 1
            black_etf_type_list.append([etf, etf_name, etf_type])
    if is_black_words == 1 or is_black_etf_type == 1: continue

    try:
        df = ak.fund_etf_hist_em(symbol=etf, period="daily", start_date=start_date, end_date=end_date, adjust="qfq")
        df = df.rename(columns={'收盘': etf})[['日期', etf]]
        df['日期'] = df['日期'].astype('str')

        # 起始日期过滤
        if (check_date not in list(df['日期'])):
            black_start_date_list.append([etf, etf_name, etf_type])
            continue

        etf_dic[etf] = df
        time.sleep(sleep_time)
    except:
        print('**** has no etf: ', etf)

etf_dic_sort = sorted(etf_dic.items())
data_df = etf_dic_sort[0][1]
for i in range(1, len(etf_dic_sort)):
    data_df = data_df.merge(etf_dic_sort[i][1], on=['日期'])

data_df = data_df.rename(columns={'日期': 'date'})
data_df = data_df.set_index('date')
data_df.index = pd.to_datetime(data_df.index)
print(data_df)

print('*' * 30)
results_list = []
for i in range(22, 23):
    ROC = data_df.pct_change(i)
    print(ROC)
    st = bt.Strategy('大类资产轮动',
                     [bt.algos.SetStat(ROC), bt.algos.SelectN(2, sort_descending=True), bt.algos.WeighEqually(),
                      bt.algos.Rebalance()])
    stras = bt.Backtest(st, data_df)
    results = bt.run(stras)
    # results.plot()
    # plt.show()
    print(results.stats)
    print('cagr', results.stats.iloc[4, 0], 'max_drawdown', results.stats.iloc[5, 0])
    results_list.append([i, results.stats.iloc[4, 0], results.stats.iloc[5, 0]])

results_list.sort(key=lambda x: x[1], reverse=True)
for i in results_list:
    print(i)

print('*' * 30)
print('black_words_list: ', black_words_list)
print('black_etf_type_list: ', black_etf_type_list)
print('black_start_date_list: ', black_start_date_list)
