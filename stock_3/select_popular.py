import akshare as ak
import pandas as pd


# 获取涨停板信息
def get_limit_up_stocks(trade_date):
    df = ak.stock_zt_pool_em(date=trade_date)
    return df

# 示例：获取2023年10月10日的涨停板信息
trade_date = '20250103'
limit_up_stocks = get_limit_up_stocks(trade_date)

# 打印涨停板信息
# print(limit_up_stocks)


limit_up_stocks_sorted = limit_up_stocks.sort_values(by='连板数', ascending=False)
# print("连板数倒排序：")
print(limit_up_stocks_sorted[['代码', '名称', '连板数', '所属行业']])

def get_industry_details(group):
    return group[['名称', '连板数']].to_dict(orient='records')


industry_details = limit_up_stocks.groupby('所属行业').apply(get_industry_details).reset_index()

industry_details.columns = ['所属行业', '股票详情']
print(industry_details)
industry_stats = limit_up_stocks.groupby('所属行业')['连板数'].count().reset_index()
industry_stats_sorted = industry_stats.sort_values(by='连板数', ascending=False)
print(industry_stats_sorted)