# 参考资料
# https://zhuanlan.zhihu.com/p/855997776
import akshare as ak
import pandas as pd
import bt
import matplotlib.pyplot as plt

start_date = '20230101'
end_date = '20251231'
etf_510300 = ak.fund_etf_hist_em(symbol="510300", period="daily", start_date=start_date, end_date=end_date,
                                 adjust="qfq")
etf_159915 = ak.fund_etf_hist_em(symbol="159915", period="daily", start_date=start_date, end_date=end_date,
                                 adjust="qfq")
etf_513100 = ak.fund_etf_hist_em(symbol="513100", period="daily", start_date=start_date, end_date=end_date,
                                 adjust="qfq")
etf_518880 = ak.fund_etf_hist_em(symbol="518880", period="daily", start_date=start_date, end_date=end_date,
                                 adjust="qfq")
st_601857 = ak.stock_zh_a_hist(symbol="601857", period="daily", start_date=start_date, end_date=end_date,
                               adjust="qfq")

etf_510300 = etf_510300.rename(columns={'收盘': '510300'})[['日期', '510300']]
etf_159915 = etf_159915.rename(columns={'收盘': '159915'})[['日期', '159915']]
etf_513100 = etf_513100.rename(columns={'收盘': '513100'})[['日期', '513100']]
etf_518880 = etf_518880.rename(columns={'收盘': '518880'})[['日期', '518880']]
st_601857 = st_601857.rename(columns={'收盘': '601857'})[['日期', '601857']]

st_601857['日期'] = st_601857['日期'].astype('str')

data_df = etf_510300.merge(
    etf_159915, on=['日期']).merge(
    etf_513100, on=['日期']).merge(
    etf_518880, on=['日期']).merge(
    st_601857, on=['日期'])

data_df = data_df.rename(columns={'日期': 'date'})
data_df = data_df.set_index('date')
data_df.index = pd.to_datetime(data_df.index)
print(data_df)

print('*' * 30)
results_list = []
for i in range(22, 23):
    ROC = data_df.pct_change(i)
    st = bt.Strategy('大类资产轮动',[bt.algos.SetStat(ROC),bt.algos.SelectN(2, sort_descending=True),bt.algos.WeighEqually(),bt.algos.Rebalance()])
    stras = bt.Backtest(st, data_df)
    results = bt.run(stras)
    results.plot()
    plt.show()
    print(results.stats)
    print('cagr', results.stats.iloc[4, 0], 'max_drawdown', results.stats.iloc[5, 0])
    results_list.append([i, results.stats.iloc[4, 0], results.stats.iloc[5, 0]])

results_list.sort(key=lambda x: x[1], reverse=True)
for i in results_list:
    print(i)