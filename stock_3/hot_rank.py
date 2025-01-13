import akshare as ak

# stock_hot_rank_em_df = ak.stock_hot_follow_xq()
# print(stock_hot_rank_em_df)
# # print(len(stock_hot_rank_em_df[stock_hot_rank_em_df['涨跌幅']>2.0]))
#
# stock_hk_hot_rank_detail_em_df = ak.stock_hk_hot_rank_detail_em(symbol="301027")
# print(stock_hk_hot_rank_detail_em_df)
#
# # stock_hk_hot_rank_em_df = ak.stock_hk_hot_rank_em()
# # print(stock_hk_hot_rank_em_df)


import akshare as ak

# 获取 A 股实时数据
stock_list = ak.stock_info_a_code_name()

# 显示前几行数据
print(stock_list)






