'''
东方财富网-行情中心-涨停板行情-涨停股池
https://quote.eastmoney.com/ztb/detail#type=ztgc

东方财富网-行情中心-涨停板行情-强势股池
https://quote.eastmoney.com/ztb/detail#type=qsgc
'''

import akshare as ak
import datetime as dt

trade_date = '20250110'
df_zt = ak.stock_zt_pool_em(date=trade_date)
df_strong = ak.stock_zt_pool_strong_em(date=trade_date)

# 序号-代码-名称
print(df_zt)


def get_stocks_code(df, code_col=1, name_col=2):
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


def group_and_sort(target):
    industry_dic, concept_dic = {}, {}
    for key, val in target.items():
        industry, concept = val[0], val[1]
        for i in industry:
            industry_dic[i] = industry_dic.get(i, 0) + 1
        for i in concept:
            concept_dic[i] = concept_dic.get(i, 0) + 1
    return industry_dic, concept_dic


# stock_zt_list = get_stocks_code(df_zt)
# stocks_code_industry_concept = get_industry_and_concept_of_stocks(stock_zt_list)
stocks_code_industry_concept = {'002917': [['化学制品'],
                                           ['民爆概念', '昨日涨停_含一字', '昨日连板_含一字', '机器视觉', '军工',
                                            '智能机器', '工业互联', '机器人概念', '一带一路', '预盈预增', '人工智能',
                                            '深圳特区'], '金奥博'], '002534': [['电源设备'],
                                                                               ['昨日涨停_含一字', '钒电池', '转债标的',
                                                                                '钙钛矿电池', '节能环保', '深股通',
                                                                                '融资融券', '预盈预增', '核能核电',
                                                                                '创投', '燃料电池', '太阳能',
                                                                                '熔盐储能', '储能'], '西子洁能'],
                                '300344': [['软件开发'],
                                           ['昨日涨停_含一字', '国产软件', '数据安全', '数字孪生', '光伏建筑一体化',
                                            '云计算', '创业板综', '新材料', '装配建筑', '智慧城市', '边缘计算',
                                            '在线教育', '算力概念'], '立方数科'], '600128': [['贸易行业'],
                                                                                             ['昨日涨停_含一字',
                                                                                              '黄金概念',
                                                                                              '昨日连板_含一字',
                                                                                              '参股期货', '内贸流通',
                                                                                              '机构重仓', '国企改革',
                                                                                              '长江三角', '创投',
                                                                                              '跨境电商', 'NFT概念'],
                                                                                             '苏豪弘业'],
                                '603990': [['软件开发'],
                                           ['昨日涨停_含一字', '国产软件', '人形机器人', '昨日连板_含一字', '昨日涨停',
                                            '低空经济', '并购重组概念', '预亏预减', '互联医疗', '融资融券', '国企改革',
                                            '机器人概念', '人工智能', '辅助生殖', '华为概念'], '麦迪科技'],
                                '603068': [['半导体'],
                                           ['昨日涨停_含一字', '昨日连板_含一字', '昨日涨停', '北斗导航', '无人机',
                                            '富时罗素', '预盈预增', '无人驾驶', '物联网', '上海自贸', '华为概念',
                                            '国产芯片', '半导体概念', 'ETC', '星闪概念', '无线耳机', '小米概念',
                                            '汽车芯片', 'WiFi', '昨日连板'], '博通集成'], '600601': [['电子元件'],
                                                                                                     ['昨日涨停_含一字',
                                                                                                      '昨日连板_含一字',
                                                                                                      '昨日涨停',
                                                                                                      '沪股通',
                                                                                                      '融资融券',
                                                                                                      '国企改革',
                                                                                                      '预盈预增',
                                                                                                      '长江三角',
                                                                                                      '华为概念',
                                                                                                      '5G概念',
                                                                                                      'CPO概念', 'PCB',
                                                                                                      '昨日连板'],
                                                                                                     '方正科技'],
                                '600657': [['房地产开发'],
                                           ['昨日涨停_含一字', '昨日涨停', '破净股', '央企改革', '化债(AMC)概念',
                                            '沪股通', '融资融券', '国企改革', '富时罗素', '标准普尔', '证金持股'],
                                           '信达地产'], '002811': [['专业服务'],
                                                                   ['昨日涨停_含一字', '昨日连板_含一字', '昨日涨停',
                                                                    '转债标的', '装配建筑', '一带一路', '预盈预增',
                                                                    '深圳特区', '昨日连板'], '郑中设计'],
                                '603777': [['食品饮料'],
                                           ['昨日涨停_含一字', '白酒', '社区团购', '昨日连板_含一字', '昨日涨停',
                                            '内贸流通', '预亏预减', '进口博览', '融资融券', '人工智能', '电商概念',
                                            '新零售', 'AIGC概念', 'ChatGPT概念', '昨日连板'], '来伊份'],
                                '600202': [['电源设备'],
                                           ['昨日涨停_含一字', '微盘股', '中俄贸易概念', '昨日涨停', '东北振兴',
                                            '国企改革', '一带一路', '核能核电', '智能电网'], '哈空调'],
                                '603667': [['通用设备'], ['机器人执行器', '昨日涨停_含一字', '减速器', '人形机器人',
                                                          '昨日连板_含一字', '昨日涨停', '特斯拉', '沪股通', '风能',
                                                          '融资融券', '机器人概念', '新能源车', '昨日连板'],
                                           '五洲新春'], '605033': [['农药兽药'],
                                                                   ['昨日涨停_含一字', '昨日连板_含一字', '西部大开发',
                                                                    '昨日涨停', '昨日连板'], '美邦股份'],
                                '002346': [['电网设备'],
                                           ['昨日涨停_含一字', '锂电池', '昨日涨停', '融资融券', '参股银行', '长江三角',
                                            '创投', '半导体概念', '碳化硅', '体育产业', '充电桩'], '柘中股份'],
                                '000561': [['通信设备'],
                                           ['昨日涨停_含一字', '商业航天', '西部大开发', '昨日涨停', '军民融合', '军工',
                                            '低空经济', '空间站概念', '大飞机', '预亏预减', '深股通', '北斗导航',
                                            '国企改革'], '烽火电子'], '002571': [['家用轻工'],
                                                                                 ['昨日涨停_含一字', '医疗器械概念',
                                                                                  '昨日连板_含一字', '昨日涨停',
                                                                                  '机构重仓', '预盈预增', '参股银行',
                                                                                  '创投', '网络游戏', '太阳能',
                                                                                  '影视概念', 'C2M概念', '拼多多概念',
                                                                                  '昨日连板'], '德力股份'],
                                '301511': [['电池'],
                                           ['昨日涨停_含一字', '锂电池', '昨日涨停', '创业板综', '专精特新', '深股通',
                                            '融资融券', '固态电池', '柔性屏(折叠屏)', 'PCB'], '德福科技'],
                                '002265': [['汽车零部件'],
                                           ['昨日涨停_含一字', '减速器', '西部大开发', '昨日涨停', '军民融合', '军工',
                                            '央企改革', '智能机器', '深股通', '国企改革', '无人机', '机器人概念',
                                            '新能源车', '新型工业化', '无人驾驶', '人工智能'], '建设工业'],
                                '603166': [['汽车零部件'],
                                           ['昨日涨停_含一字', '减速器', '农业种植', '西部大开发', '昨日涨停', '军工',
                                            '专精特新', '机器人概念', '新能源车'], '福达股份'],
                                '002536': [['汽车零部件'],
                                           ['昨日涨停_含一字', '昨日连板_含一字', '昨日涨停', '军工', '深股通',
                                            '汽车热管理', '融资融券', '无人机', '机器人概念', '新能源车', '人工智能',
                                            '燃料电池', '国产芯片', '液冷概念', '昨日连板'], '飞龙股份'],
                                '603188': [['化学制品'], ['昨日涨停_含一字', '昨日涨停', '预盈预增'], '亚邦股份'],
                                '002686': [['通用设备'], ['昨日涨停_含一字', '昨日涨停', '军工', '专精特新', '新材料',
                                                          '化债(AMC)概念', '国企改革', '新能源车', '水利建设'],
                                           '亿利达'], '600530': [['食品饮料'],
                                                                 ['昨日涨停_含一字', '养老概念', '昨日涨停', 'IPO受益',
                                                                  '参股券商', '预盈预增', '长江三角', '电商概念'],
                                                                 '交大昂立'], '002629': [['采掘行业'],
                                                                                         ['昨日涨停_含一字', '油气设服',
                                                                                          '微盘股', '天然气',
                                                                                          '昨日涨停', '机构重仓',
                                                                                          '预盈预增', 'QFII重仓'],
                                                                                         '仁智股份'],
                                '002660': [['消费电子'],
                                           ['昨日涨停_含一字', '昨日涨停', '智能机器', '国企改革', '无人机', '区块链',
                                            '新能源', '独角兽', '深圳特区', '太阳能', '储能', 'OLED', 'LED',
                                            '第三代半导体', '智慧灯杆', '充电桩', '氮化镓'], '茂硕电源'],
                                '603666': [['专用设备'],
                                           ['昨日涨停_含一字', '人形机器人', '昨日涨停', '专精特新', '低空经济',
                                            '机构重仓', '预亏预减', '机器人概念', '富时罗素', '标准普尔', '多模态AI',
                                            '智能电网', '特高压', '充电桩'], '亿嘉和'], '002042': [['纺织服装'],
                                                                                                   ['昨日涨停_含一字',
                                                                                                    '农业种植',
                                                                                                    '昨日涨停',
                                                                                                    '东盟自贸区概念',
                                                                                                    '深股通',
                                                                                                    '融资融券',
                                                                                                    '富时罗素',
                                                                                                    '标准普尔',
                                                                                                    '绿色电力',
                                                                                                    '新型工业化',
                                                                                                    '职业教育',
                                                                                                    '参股银行', '创投',
                                                                                                    '贬值受益',
                                                                                                    'C2M概念',
                                                                                                    '算力概念',
                                                                                                    '东数西算'],
                                                                                                   '华孚时尚'],
                                '600053': [['多元金融'],
                                           ['昨日涨停_含一字', '昨日涨停', '沪股通', '预亏预减', '融资融券', '富时罗素',
                                            '标准普尔', '创投', '参股新三板'], '九鼎投资'], '600650': [['铁路公路'], [
        '昨日涨停_含一字', '昨日涨停', 'IPO受益', '参股券商', 'AB股', '机构重仓', '国企改革', '冷链物流', '长江三角',
        '上海自贸', '沪企改革'], '锦江在线'], '605178': [['装修装饰'],
                                                         ['昨日涨停_含一字', '微盘股', '昨日涨停', '智慧城市', '物联网',
                                                          '智慧灯杆'], '时空科技'], '603072': [['小金属'],
                                                                                               ['昨日涨停_含一字',
                                                                                                '小金属概念',
                                                                                                '稀土永磁', '昨日涨停',
                                                                                                '次新股',
                                                                                                '注册制次新股',
                                                                                                '新材料', '融资融券'],
                                                                                               '天和磁材'],
                                '603086': [['农药兽药'], ['昨日涨停_含一字', '昨日涨停', '破净股', '股权激励'],
                                           '先达股份'], '600967': [['交运设备'],
                                                                   ['昨日涨停_含一字', '西部大开发', '昨日涨停',
                                                                    '军民融合', '军工', '央企改革', '机构重仓',
                                                                    '沪股通', '融资融券', '国企改革', '机器人概念',
                                                                    '标准普尔', '铁路基建'], '内蒙一机'],
                                '605488': [['塑料制品'],
                                           ['昨日涨停_含一字', '昨日涨停', '转债标的', '专精特新', '新材料', '无线充电',
                                            '节能环保', '降解塑料', '一带一路', '传感器', '预盈预增', '苹果概念',
                                            '华为概念', 'AI手机', '智能穿戴', '小米概念'], '福莱新材'],
                                '603015': [['专用设备'],
                                           ['昨日涨停_含一字', '昨日连板_含一字', '昨日涨停', '智能机器', '融资融券',
                                            '工业4.0', '机器人概念', '新能源', '人工智能', '可控核聚变', '物联网',
                                            '太阳能', '储能', '充电桩'], '弘讯科技'], '603283': [['专用设备'],
                                                                                                 ['昨日涨停_含一字',
                                                                                                  '锂电池', '昨日涨停',
                                                                                                  '特斯拉', '上证380',
                                                                                                  '沪股通', '融资融券',
                                                                                                  '新能源车',
                                                                                                  '标准普尔',
                                                                                                  '预盈预增',
                                                                                                  '苹果概念',
                                                                                                  '半导体概念',
                                                                                                  '英伟达概念',
                                                                                                  '无线耳机'],
                                                                                                 '赛腾股份'],
                                '002187': [['商业百货'],
                                           ['昨日涨停_含一字', '黄金概念', '预制菜概念', '退税商店', '昨日涨停',
                                            '内贸流通', '机构重仓', '国企改革', '粤港自贸', '创投', '电商概念',
                                            '新零售', '首发经济', '网红直播'], '广百股份'], '000573': [['房地产开发'], [
        '昨日涨停_含一字', '昨日连板_含一字', '昨日涨停', '预亏预减', '创投', '壳资源', '昨日连板'], '粤宏远Ａ']}

industry_dic, concept_dic = group_and_sort(stocks_code_industry_concept)
print(industry_dic)
print(sorted(industry_dic.items(), key=lambda x: x[1], reverse=True))
print(concept_dic)
print(sorted(concept_dic.items(), key=lambda x: x[1], reverse=True))
