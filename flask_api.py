from flask import Flask, jsonify, request
import json
import re
import jieba
import jieba.analyse
import math
import pandas as pd
import numpy as np
import jieba.posseg as pseg
from bs4 import BeautifulSoup
jieba.load_userdict('金融专有名词.txt')
from flask import Flask, request

app = Flask(__name__)


@app.route('/get', methods=['GET', 'POST'])
def get():
    if request.method == 'POST':
        #获取传递过来的文件
        data = request.form.get('file')
        # num = request.args.get('topk')
        # 读取文本
        with open(data, 'r', encoding='utf-8') as fp:
            art = fp.read().strip().splitlines()
        # 转化为Series
        li_text = pd.Series(art)

        # 通过re过流掉一些东西
        content = ''
        remove = re.compile(r'\s')
        douhao = re.compile(r',')
        for string in art:
            string = re.sub(remove, '', string)
            string = re.sub(douhao, '', string)
            content += string
        """
                处理每行的文本数据
                返回分词结果
        """
        # 1. 使用正则表达式去除非中文字符
        filter_pattern = re.compile('[^\u4E00-\u9FD5]+')
        chinese_only = filter_pattern.sub('', content)
        # 2. 结巴分词+词性标注
        words_lst = pseg.cut(chinese_only)

        # 3. 去除停用词
        stopword = [line.rstrip() for line in open('the_test_stopword.csv', 'r', encoding='utf-8')]
        meaninful_words = []
        for word, flag in words_lst:
            # if (word not in stopwords) and (flag == 'v'):
            # 也可根据词性去除非动词等
            if word not in stopword:
                meaninful_words.append(word)
        content = ' '.join(meaninful_words)
        # 然后处理后的数据进行切词
        jieba.enable_parallel(4)
        keyword = jieba.analyse.extract_tags(content, topK=10, withWeight=False, allowPOS=())
        # 以json的形式返回
        t = {}
        t['data'] = keyword
        return json.dumps(t, ensure_ascii=False)
    else:
        return '错了'


if __name__ == '__main__':
    app.run(debug=True, port=6887, host='0.0.0.0')