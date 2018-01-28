# -*- coding: utf-8 -*-
import sys
import time

from mover.spider.ProductWords import *
from mover.spider.Demo import *
from mover.core.ZbApi import *


#python main.py get_dataoke_list
def Usage():
    print 'main.py usage:'
    print '\n'


def run_demo():
    DemoSpider().run()


def zb():
    api = ZbApi()
    print api.query_account()


#百度关键词
def get_tb_words():
    #words = ProductWordsSpider().baseWords()
    ProductWordsSpider().run()


if __name__ == '__main__':
    print sys.argv
    #sys.exit()
    if len(sys.argv) < 2:
        Usage()
        sys.exit()

    start = time.time()
    function = eval(sys.argv[1])
    function()
    end = time.time()
    print end-start
