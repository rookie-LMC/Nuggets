import akshare as ak
import pandas as pd


def get_stocks_code(df, code_col=1, name_col=2):
    stocks_code = []
    rows, cols = df.shape
    for row in range(rows):
        stocks_code.append([df.iloc[row, code_col], df.iloc[row, name_col]])
    return stocks_code


def get_industry_and_concept_of_stocks(stocks_code, debug_num=20000):
    industry_list = ak.stock_board_industry_name_em()
    concept_list = ak.stock_board_concept_name_em()
    stocks_code_industry_concept = {}
    print(industry_list)
    print(concept_list)
    for i in range(min(len(stocks_code), debug_num)):
        st_code, st_name = stocks_code[i][0], stocks_code[i][1]
        stocks_code_industry_concept[st_code] = [[], [], st_name]

    for name in list(industry_list['板块名称']):
        print(name)
        industry_stock = ak.stock_board_industry_cons_em(name)
        for i in range(min(len(stocks_code), debug_num)):
            st_code, st_name = stocks_code[i][0], stocks_code[i][1]
            if st_code in list(industry_stock['代码']):
                stocks_code_industry_concept[st_code][0].append(name)

    for name in list(concept_list['板块名称']):
        print(name)
        concept_stocks = ak.stock_board_concept_cons_em(name)
        for i in range(min(len(stocks_code), debug_num)):
            st_code, st_name = stocks_code[i][0], stocks_code[i][1]
            if st_code in list(concept_stocks['代码']):
                stocks_code_industry_concept[st_code][1].append(name)

    return stocks_code_industry_concept


def group_and_sort(target):
    industry_dic, concept_dic = {}, {}
    for key, val in target.items():
        industry, concept = val[0], val[1]
        for i in industry:
            industry_dic[i] = industry_dic.get(i, 0) + 1
        for i in concept:
            concept_dic[i] = concept_dic.get(i, 0) + 1
    return industry_dic, concept_dic


def export_zt(save_file, trade_date, df_dic):
    file_path = './' + save_file + '/' + str(trade_date) + '.xlsx'
    print(file_path)

    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        for zt, df in df_dic.items():
            df.to_excel(writer, sheet_name=zt)


# stock_daily.to_excel(writer, sheet_name='daily')
# stock_weekly.to_excel(writer, sheet_name='weekly')
# stock_monthly.to_excel(writer, sheet_name='monthly')
