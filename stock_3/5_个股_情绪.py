import akshare as ak
from snownlp import SnowNLP
# stock_info_global_cls_df = ak.stock_info_global_cls(symbol="全部")
#
# print(stock_info_global_cls_df)


# https://blog.csdn.net/lildkdkdkjf/article/details/128771330



import time
import akshare as ak
from snownlp import SnowNLP

stock_code = '600887'
date = time.strftime("%Y%m%d", time.localtime())
stock_news_em_df = ak.stock_news_em(symbol=stock_code)

# print(stock_news_em_df.columns)
# print(stock_news_em_df.iloc[0, 0])
# print(stock_news_em_df.iloc[0, 1])
# print(stock_news_em_df.iloc[0, 2])
# print(stock_news_em_df.iloc[0, 3])
# print(stock_news_em_df.iloc[0, 4])
# print(stock_news_em_df.iloc[0, 5])
print(stock_news_em_df.iloc[-1, 1])

positive = 0
negative = 0

for i in stock_news_em_df.values[:, 1]:
    text = str(i)
    s = SnowNLP(text)
    print(len(s.sentences))
    for sentence in s.sentences:
        print(sentence, SnowNLP(sentence).sentences)





























