import akshare as ak
import pandas as pd


def export_A_stocks(stock_info_list, date):
    stock_info_list.to_excel('01_股票列表' + str(date) + '.xlsx', sheet_name='A-stocks')


def judger_of_three_monthly_K(fir_open, fir_close, sec_open, sec_close, thr_open, thr_close):
    # 第一根k线 阳线
    judger_1 = fir_open < fir_close
    # 第二根k线 阴线
    judger_2 = sec_open > sec_close
    # 第三根k线 阳线
    judger_3 = thr_open < thr_close
    # 保持上升趋势
    judger_4 = fir_close < thr_close
    if (judger_1 and judger_2 and judger_3 and judger_4):
        return True
    return False


def selector_of_three_K_monthly(df, name, open_index, close_index):
    if len(df['date'].values) != 3:
        print(name + ' not 3')
        return False
    fir_open, fir_close = df.iloc[0, open_index], df.iloc[0, close_index]
    sec_open, sec_close = df.iloc[1, open_index], df.iloc[1, close_index]
    thr_open, thr_close = df.iloc[2, open_index], df.iloc[2, close_index]
    if judger_of_three_monthly_K(fir_open, fir_close, sec_open, sec_close, thr_open, thr_close):
        return True
    return False