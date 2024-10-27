import akshare as ak
import pandas as pd


def export_A_stocks(stock_daily, stock_weekly, stock_monthly, action_date, stock_code):
    file_path = './stock_info' + '/' + str(action_date) + '-' + str(stock_code) + '.xlsx'
    print(file_path)
    # stock_date.to_excel(file_path, sheet_name=sheet_name)

    with pd.ExcelWriter(file_path, engine='openpyxl') as writer:
        stock_daily.to_excel(writer, sheet_name='daily')
        stock_weekly.to_excel(writer, sheet_name='weekly')
        stock_monthly.to_excel(writer, sheet_name='monthly')



        # export_A_stocks(stock_daily[stocks_code[i][0]], stock_weekly[stocks_code[i][0]],
        #                 stock_monthly[stocks_code[i][0]],
        #                 action_date, stocks_code[i][0])