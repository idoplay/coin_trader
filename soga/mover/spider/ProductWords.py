# -*- coding: utf-8 -*-
import urllib
import math
from mover.core.Spider import *
from mover.core.Worker import *
WORKER = 8


class ProductWordsSpider(SpiderEngine):
    '''
    更新指数
    '''
    def __init__(self):
        SpiderEngine.__init__(self)
        self.apiHost = {
            'get_base_words': '%s?c=baseWords' % self.config['api_host'],
            'get_two_words': '%s?c=twoWords' % self.config['api_host'],
        }
        #hashlib.md5(url).hexdigest()

    def baseWords(self):
        res = self.http_get(self.apiHost['get_base_words'])
        res = json.loads(res)
        return res['result']

    def twoWords(self):
        res = self.http_get(self.apiHost['get_two_words'])
        res = json.loads(res)
        return res['result']

    def whileRun(self, data):
        page = 40
        p = int(math.ceil(len(data) / page))
        p += 1
        for x in xrange(0, p):
            start = x * page
            aa = data[start: start+page]
            self.run_worker(aa, self.__get_tb_words)

    def run(self):
        wlist = self.twoWords()
        self.whileRun(wlist)

    def __get_tb_words(self, word):
        word = word.encode('utf-8')
        res = self.http_get('https://suggest.taobao.com/sug?code=utf-8&q=%s&callback=jsonp888' % urllib.quote(word))
        res = res.replace('jsonp888(', '').replace(')', '')
        res = res.strip()
        res = json.loads(res)
        pdata = []
        for l in range(0, len(res['result'])):
            rx = res['result'][l]
            _hash_str = self.get_hash_key(rx[0])
            rx.append(_hash_str[0])
            pdata.append(rx)
        print pdata
        apiUrl = '%s?c=run' % self.config['api_host']
        self.http_post(apiUrl, pdata)
