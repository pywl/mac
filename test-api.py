# import api #我自己封装的函数
# import pandas as pd
# art_text = '私募基金.txt'
# print(api.jieba_nlp(art_text))
# import requests
# import requests
#
# art_text = '私募基金.txt'
# r = requests.get("http://127.0.0.1:6677/api/html_rt={}".format(art_text))
# print(r)
import requests
import pandas as pd
url = 'http://0.0.0.0:6887/get'
data = '/Users/wulei/Desktop/test_flask_api/test/私募基金.txt'
data = {
    'file':data
}
ret = requests.post(url=url, data=data)
print(ret.text)

# #读取文本
# with open(ret.text,'r',encoding='utf-8') as fp:
#     art = fp.read().strip().splitlines()
# #转化为Series
# li_text = pd.Series(art)
# print(li_text)