import time
import pandas as pd
import akshare as ak

#### 过滤
stock_black_list = []
words_black_list = ['st', 'ST', 'sT', 'St', '酒']
concept_black_list = []
# industry_black_list = ['房地产服务', '房地产开发', '酿酒行业', '食品饮料', '教育']
industry_black_list = []

debug_num = 100000
sleep_time_day_week_month_info = 0.25

'''
01 a股股票列表
'''
stock_list = ak.stock_zh_a_spot_em()
stock_symbol = stock_list['代码'].values
stock_name = stock_list['名称'].values
stocks_code = list(zip(stock_symbol, stock_name))
# export_A_stocks(stock_list, action_date)
print('**** 01 股票共计:', len(stocks_code))

'''
02 过滤 关键字
'''
for i in range(len(stocks_code)):
    tmp_symbol, tmp_name = stocks_code[i][0], stocks_code[i][1]
    for word in words_black_list:
        if word in tmp_name:
            stock_black_list.append(tmp_symbol)
            break
stock_black_list = list(set(stock_black_list))
print('**** 02 过滤 关键字 数量: ', len(stock_black_list))

'''
02 过滤 概念
'''
concept_list = ak.stock_board_concept_name_em()
# 检查概念是否存在
for name in concept_black_list:
    if name not in concept_list['板块名称'].values:
        print(f"未找到概念名称'{name}'，请检查输入是否正确。")
        continue
    concept_stocks = ak.stock_board_concept_cons_em(name)
    print('**** 02 过滤 概念: ', name, ': ', len(concept_stocks['代码'].values))
    stock_black_list = list(set(stock_black_list) | set(concept_stocks['代码'].values))

'''
02 过滤 行业
'''
industry_list = ak.stock_board_industry_name_em()
# 检查行业是否存在
for name in industry_black_list:
    if name not in industry_list['板块名称'].values:
        print(f"未找到行业名称'{name}'，请检查输入是否正确。")
        continue
    industry_stock = ak.stock_board_industry_cons_em(name)
    print('**** 02 过滤 行业: ', name, ': ', len(industry_stock['代码'].values))
    stock_black_list = list(set(stock_black_list) | set(industry_stock['代码'].values))

'''
02 过滤 执行
'''
stocks_code = [i for i in stocks_code if i[0] not in stock_black_list]
print('**** 02 过滤后 个股数量 : ', len(stocks_code), ', 过滤数量: ', len(stock_black_list))

print(stocks_code)
for
# save_date = ''
# df.to_excel('./save_stock/zt_pool_' + save_date + '.xlsx', sheet_name='A-stocks')

'''
03 召回
个股日线、周线、月线
'''
print('*' * 50 + ' 03 召回数据')
stock_daily, stock_weekly, stock_monthly = {}, {}, {}
for i in range(min(len(stocks_code), debug_num)):
    try:
        print('**** load K line : ', stocks_code[i][0])
        stock_daily[stocks_code[i][0]] = ak.stock_zh_a_hist(stocks_code[i][0], adjust="qfq", period="daily",
                                                            start_date='20220101')
        stock_weekly[stocks_code[i][0]] = ak.stock_zh_a_hist(stocks_code[i][0], adjust="qfq", period="weekly",
                                                             start_date='20220101')
        stock_monthly[stocks_code[i][0]] = ak.stock_zh_a_hist(stocks_code[i][0], adjust="qfq", period="monthly",
                                                              start_date='20220101')
        time.sleep(sleep_time_day_week_month_info)
    except:
        print('**** has no day week month K line: ', stocks_code[i][0])
print('*' * 50 + ' 03 召回数据完毕')

