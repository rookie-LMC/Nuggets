import time
import akshare as ak
import numpy as np
from numpy import empty
import pandas as pd
import datetime as dt

# 处理时间
from dateutil.parser import parse
from datetime import datetime, timedelta
from chinese_calendar import is_workday, is_holiday

from utils_stock import *

debug_num = 20000000000000000
# action_date = dt.date.today()
action_date = '2024-12-16'
save_file = 'stock_A_2024_12_16'
stocks_code = [('300465', '高伟达'), ('601969', '海南矿业'), ('300509', '新美星'), ('300382', '斯莱克'),
               ('002568', '百润股份'), ('002068', '黑猫股份'), ('002646', '天佑德酒'), ('605319', '无锡振华'),
               ('603181', '皇马科技'), ('000534', '万泽股份'), ('002182', '宝武镁业'), ('002108', '沧州明珠'),
               ('002081', '金 螳 螂'), ('001278', '一彬科技'), ('603076', '乐惠国际'), ('603686', '福龙马'),
               ('600668', '尖峰集团'), ('002716', '湖南白银'), ('605180', '华生科技'), ('605133', '嵘泰股份'),
               ('603488', '展鹏科技'), ('000627', '天茂集团'), ('600714', '金瑞矿业'), ('688683', '莱尔科技'),
               ('002191', '劲嘉股份'), ('300906', '日月明'), ('605050', '福然德'), ('605378', '野马电池'),
               ('605208', '永茂泰'), ('002104', '恒宝股份'), ('603908', '牧高笛'), ('002585', '双星新材'),
               ('603538', '美诺华'), ('002350', '北京科锐'), ('000688', '国城矿业'), ('000570', '苏常柴Ａ'),
               ('300024', '机器人'), ('002817', '黄山胶囊'), ('603085', '天成自控'), ('300365', '恒华科技'),
               ('603901', '永创智能'), ('603681', '永冠新材'), ('300098', '高新兴'), ('603344', '星德胜'),
               ('600560', '金自天正'), ('000042', '中洲控股'), ('000637', '茂化实华'), ('300507', '苏奥传感'),
               ('300611', '美力科技'), ('603909', '建发合诚'), ('002982', '湘佳股份'), ('600682', '南京新百'),
               ('002829', '星网宇达'), ('600722', '金牛化工'), ('000523', '红棉股份'), ('601956', '东贝集团'),
               ('301081', '严牌股份'), ('002303', '美盈森'), ('603096', '新经典'), ('603506', '南都物业'),
               ('002584', '西陇科学'), ('688288', '鸿泉物联'), ('600397', '安源煤业'), ('002314', '南山控股'),
               ('300289', '利德曼'), ('300335', '迪森股份'), ('300543', '朗科智能'), ('600833', '第一医药'),
               ('002121', '科陆电子'), ('600293', '三峡新材'), ('002800', '天顺股份'), ('300494', '盛天网络'),
               ('688327', '云从科技-UW'), ('603725', '天安新材'), ('002296', '辉煌科技'), ('300582', '英飞特'),
               ('301027', '华蓝集团'), ('603256', '宏和科技'), ('002437', '誉衡药业'), ('300756', '金马游乐'),
               ('002576', '通达动力'), ('002774', '快意电梯'), ('002329', '皇氏集团'), ('300995', '奇德新材'),
               ('300288', '朗玛信息'), ('002921', '联诚精密'), ('002687', '乔治白'), ('603176', '汇通集团'),
               ('002264', '新 华 都'), ('001319', '铭科精技'), ('300586', '美联新材'), ('603030', '全筑股份'),
               ('300603', '立昂技术'), ('300736', '百邦科技'), ('603458', '勘设股份'), ('600386', '北巴传媒'),
               ('002798', '帝欧家居'), ('002177', '御银股份'), ('002811', '郑中设计'), ('688620', '安凯微'),
               ('300113', '顺网科技'), ('002652', '扬子新材'), ('300329', '海伦钢琴'), ('300074', '华平股份'),
               ('002501', '利源股份'), ('688365', '光云科技'), ('300153', '科泰电源'), ('600630', '龙头股份'),
               ('002820', '桂发祥'), ('002103', '广博股份'), ('002659', '凯文教育'), ('603839', '安正时尚'),
               ('603326', '我乐家居'), ('301231', '荣信文化')]

stock_daily, stock_weekly, stock_monthly = {}, {}, {}
for i in range(min(len(stocks_code), debug_num)):
    try:
        # print('**** load K line : ', stocks_code[i][0])
        stock_daily[stocks_code[i][0]], stock_weekly[stocks_code[i][0]], stock_monthly[stocks_code[i][0]] = \
            load_stocks(save_file, action_date, stocks_code[i][0])

        # print(stock_daily[stocks_code[i][0]][['日期', '收盘', '成交量']])
        # print(stock_weekly[stocks_code[i][0]][['日期', '收盘', '成交量']])
        # print(stock_monthly[stocks_code[i][0]][['日期', '收盘', '成交量']])
    except:
        print('**** has no day week month K line: ', stocks_code[i][0])
print('*' * 50 + ' 03 召回数据完毕')

win_rate_list = []
stocks_code_industry_concept = {}
for i in range(min(len(stocks_code), debug_num)):
    stock_data = stock_daily[stocks_code[i][0]][['日期', '涨跌幅']]
    win_rate_list.append(stock_data.iloc[-1, 1])
    stocks_code_industry_concept[stocks_code[i][0]] = [[], [], stock_data.iloc[-1, 1]]

industry_list = ak.stock_board_industry_name_em()
concept_list = ak.stock_board_concept_name_em()

for name in list(industry_list['板块名称']):
    industry_stock = ak.stock_board_industry_cons_em(name)
    for i in range(min(len(stocks_code), debug_num)):
        if stocks_code[i][0] in list(industry_stock['代码']):
            stocks_code_industry_concept[stocks_code[i][0]][0].append(name)

for name in list(concept_list['板块名称']):
    concept_stocks = ak.stock_board_concept_cons_em(name)
    for i in range(min(len(stocks_code), debug_num)):
        if stocks_code[i][0] in list(concept_stocks['代码']):
            stocks_code_industry_concept[stocks_code[i][0]][1].append(name)

print('*' * 20 + ' 明细情况')
print('*' * 20 + ' 分析日期: ', action_date, ', 读取文件夹', save_file)
for i in range(min(len(stocks_code), debug_num)):
    print(stocks_code[i][0], stocks_code[i][1],
          ' , 涨跌幅: ', stocks_code_industry_concept[stocks_code[i][0]][2],
          ' , 行业: ', stocks_code_industry_concept[stocks_code[i][0]][0],
          ' , 概念: ', stocks_code_industry_concept[stocks_code[i][0]][1])

print('*' * 20 + ' 胜率情况')
win_num = len([1 for i in win_rate_list if i > 0])
print(win_num, len(win_rate_list), win_num / len(win_rate_list))
