'''
东方财富网-行情中心-涨停板行情-涨停股池
https://quote.eastmoney.com/ztb/detail#type=ztgc

东方财富网-行情中心-涨停板行情-强势股池
https://quote.eastmoney.com/ztb/detail#type=qsgc
'''

import akshare as ak
import datetime as dt

trade_date = '20250108'
df_zt = ak.stock_zt_pool_em(date=trade_date)
df_strong = ak.stock_zt_pool_strong_em(date=trade_date)

print(df_zt[['代码', '名称', '涨跌幅', '流通市值', '炸板次数', '涨停统计', '连板数', '所属行业']])


# print(df_strong)


def get_stocks_code(df, code_col=0, name_col=1):
    stocks_code = []
    rows, cols = df_zt.shape
    for row in range(rows):
        stocks_code.append([df.iloc[row, code_col], df.iloc[row, name_col]])
    return stocks_code


def get_industry_and_concept_of_stocks(stocks_code, debug_num=20000):
    industry_list = ak.stock_board_industry_name_em()
    concept_list = ak.stock_board_concept_name_em()
    stocks_code_industry_concept = {}

    for i in range(min(len(stocks_code), debug_num)):
        st_code, st_name = stocks_code[i][0], stocks_code[i][1]
        stocks_code_industry_concept[st_code] = [[], [], st_name]

    for name in list(industry_list['板块名称']):
        industry_stock = ak.stock_board_industry_cons_em(name)
        for i in range(min(len(stocks_code), debug_num)):
            st_code, st_name = stocks_code[i][0], stocks_code[i][1]
            if st_code in list(industry_stock['代码']):
                stocks_code_industry_concept[st_code][0].append(name)

    for name in list(concept_list['板块名称']):
        concept_stocks = ak.stock_board_concept_cons_em(name)
        for i in range(min(len(stocks_code), debug_num)):
            st_code, st_name = stocks_code[i][0], stocks_code[i][1]
            if st_code in list(concept_stocks['代码']):
                stocks_code_industry_concept[st_code][1].append(name)

    return stocks_code_industry_concept

# def group_and_sort(target):
#     info_dic = {}
#     for key, val in info_dic.items():
#         for



stocks_code_industry_concept = get_industry_and_concept_of_stocks()
print(stocks_code_industry_concept)

stocks_code_industry_concept = get_industry_and_concept_of_stocks(get_stocks_code(df_strong))
print(stocks_code_industry_concept)
