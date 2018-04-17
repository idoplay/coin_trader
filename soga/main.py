# -*- coding: utf-8 -*-
import sys
import time

from mover.spider.ProductWords import *
from mover.spider.Demo import *
from mover.trader.Zb import *
from mover.trader.Binance import *

from binance.client import Client
import websocket


#python main.py get_dataoke_list
def Usage():
    print 'main.py usage:'
    print '\n'


def run_demo():
    DemoSpider().run()


def zb():
    obj = ZbTrader();
    #print obj.get_markets()

    print obj.account_info()

    print obj.get_user_address()

def binance():
    '''
    client = Client('m21J2lNN8S5KVpdZxq9KlqiXEmoqIcjTvi3Kl3VG6m7usGfj9WrfUWX89Qr2X1lE', '6ErHjH4hXw1duUnOSA2VfdCVKhZMTlipoJ8xU6B2vrXoGoI4FZFDWlDNnCFfGp9J')
    prices = client.get_all_tickers()
    print prices
    '''
    obj = BinanceTrader();

    #print obj.account_info()
    print obj.tickers()
    #print obj.get_book_ticker()


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
