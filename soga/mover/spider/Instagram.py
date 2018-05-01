# -*- coding: utf-8 -*-
import logging

import re
import json
import requests
from mover.core.Spider import *


class InstagramSpider(SpiderEngine):

    def __init__(self):
        SpiderEngine.__init__(self)
        self.header = {'User-Agent': 'Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5'};
        self.proxies = self.config['proxies']

    def run(self):
        #self.get_user_list()
        self.get_user_page('designhome')


    def get_user_list(self):
        #关键字用户列表
        url = "https://www.instagram.com/web/search/topsearch/?query=home&rank_token=0.00001"
        res = requests.get(url, headers=self.header, timeout=30, verify=True, proxies=self.proxies)
        re = res.json()

        aurl = self.config["server_api"]+"/index2.php"
        res = requests.post(aurl, data=json.dumps(re))
        print res.text


    def get_user_page(self, name):
        #用户主页
        url = "https://www.instagram.com/%s/" % name
        print self.header
        res = requests.get(url, headers=self.header, timeout=30, verify=True, proxies=self.proxies)
        res2 = self.sMatch('window\._sharedData =', ';<\/script>', res.text, 0)

        print res2[0]