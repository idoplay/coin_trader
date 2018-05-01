# -*- coding: utf-8 -*-
import time
import hashlib
import requests
import hmac

try:
    from urllib import urlencode
# python3
except ImportError:
    from urllib.parse import urlencode

from mover.core.Abstract import *
from binance.client import Client

class BinanceApi(Abstract):
    BASE_URL = "https://www.binance.com/api/v1"
    BASE_URL_V3 = "https://api.binance.com/api/v3"
    PUBLIC_URL = "https://www.binance.com/exchange/public/product"

    def __init__(self):
        Abstract.__init__(self)
        self.key = self.config['binance_config']['access_key']
        self.secret = self.config['binance_config']['access_secret']
        self.proxies = self.config['proxies']

    def binance_api(self):
        self.client = Client(self.config['binance_config']['access_key'], self.config['binance_config']['access_secret'])

    def get_history(self, market, limit=50):
        path = "%s/historicalTrades" % self.BASE_URL
        params = {"symbol": market, "limit": limit}
        return self._get_no_sign(path, params)

    '''
    def search_history(self, market, startTime, endTime)
    historicalTrades
    '''
    def get_cny_usd(self):
        path = "https://www.binance.com/exchange/public/cnyusd"
        res = self._getss(path)
        return res['rate']

    def get_all_tickers_bak(self):
        #有缓存
        path = "https://www.binance.com/api/v1/ticker/allPrices"
        return self._getss(path)

    def get_all_tickers(self):
        #实时当前成交价
        path = "%s/ticker/price" % self.BASE_URL_V3
        params = {}
        return self._get_no_sign(path, params)

    def get_book_ticker(self,market=None):
        #返回买卖一的价位,为空返回所有数据
        '''
        {
        "symbol": "LTCBTC",
        "bidPrice": "4.00000000",
        "bidQty": "431.00000000",
        "askPrice": "4.00000200", 卖一价
        "askQty": "9.00000000"
        }
        '''
        path = "%s/ticker/bookTicker" % self.BASE_URL_V3
        params = {}
        if market is not None:
            params = {"symbol": market}
        return self._get_no_sign(path, params)

    def get_trades(self, market, limit=50):
        path = "%s/trades" % self.BASE_URL
        params = {"symbol": market, "limit": limit}
        return self._get_no_sign(path, params)

    def get_kline(self, market):
        path = "%s/klines" % self.BASE_URL
        params = {"symbol": market}
        return self._get_no_sign(path, params)

    def get_ticker(self, market):
        path = "%s/ticker/24hr" % self.BASE_URL
        params = {"symbol": market}
        return self._get_no_sign(path, params)

    def get_order_books(self, market, limit=50):
        path = "%s/depth" % self.BASE_URL
        params = {"symbol": market, "limit": limit}
        return self._get_no_sign(path, params)

    def get_account(self):
        path = "%s/account" % self.BASE_URL_V3
        return self._get(path, {})

    def get_products(self):
        return self._getss(self.PUBLIC_URL)

    def get_exchange_info(self):
        path = "%s/exchangeInfo" % self.BASE_URL
        return self._getss(path)

    def get_open_orders(self, market, limit = 100):
        path = "%s/openOrders" % self.BASE_URL_V3
        params = {"symbol": market}
        return self._get(path, params)

    def get_my_trades(self, market, limit = 50):
        #交易历史,交易历史最大500条
        path = "%s/myTrades" % self.BASE_URL_V3
        params = {"symbol": market, "limit": limit}
        return self._get(path, params)

    def buy_limit(self, market, quantity, price):
        #限价买入
        path = "%s/order" % self.BASE_URL_V3
        params = self._order(market, quantity, "BUY", price)
        return self._post(path, params)

    def sell_limit(self, market, quantity, rate):
        #限价卖出
        path = "%s/order" % self.BASE_URL_V3
        params = self._order(market, quantity, "SELL", price)
        return self._post(path, params)

    def buy_market(self, market, quantity):
        #卖一成交
        path = "%s/order" % self.BASE_URL_V3
        params = self._order(market, quantity, "BUY")
        return self._post(path, params)

    def sell_market(self, market, quantity):
        #买一成交
        path = "%s/order" % self.BASE_URL_V3
        params = self._order(market, quantity, "SELL")
        return self._post(path, params)

    def query_order(self, market, orderId):
        #查询order
        path = "%s/order" % self.BASE_URL_V3
        params = {"symbol": market, "orderId": orderId}
        return self._get(path, params)

    def cancel(self, market, order_id):
        path = "%s/order" % self.BASE_URL_V3
        params = {"symbol": market, "orderId": order_id}
        return self._delete(path, params)

    def _get_no_sign(self, path, params={}):
        query = urlencode(params)
        url = "%s?%s" % (path, query)
        return self._getss(url)

    def _sign(self, params={}):
        data = params.copy()

        ts = str(int(1000 * time.time()))
        data.update({"timestamp": ts})

        h = urlencode(data)
        b = bytearray()
        b.extend(self.secret.encode())
        signature = hmac.new(b, msg=h.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        data.update({"signature": signature})
        return data

    def _get(self, path, params={}):
        params.update({"recvWindow": 120000})
        query = urlencode(self._sign(params))
        url = "%s?%s" % (path, query)
        header = {"X-MBX-APIKEY": self.key}

        proxies = {
            'http': 'http://127.0.0.1:1087',
            'https': 'https://127.0.0.1:1087'
        }

        return requests.get(url, headers=header, \
            timeout=30, verify=True, proxies=proxies).json()

    def _getss(self, path, params={}):
        return requests.get(path, timeout=30, verify=True, proxies=self.proxies).json()

    def _post(self, path, params={}):
        params.update({"recvWindow": 120000})
        query = urlencode(self._sign(params))
        url = "%s?%s" % (path, query)
        header = {"X-MBX-APIKEY": self.key}

        proxies = {
            'http': 'http://127.0.0.1:1087',
            'https': 'https://127.0.0.1:1087'
        }

        return requests.post(url, headers=header, \
            timeout=30, verify=True, proxies=proxies).json()

    def _order(self, market, quantity, side, rate=None):
        params = {}

        if rate is not None:
            params["type"] = "LIMIT"
            params["price"] = self._format(rate)
            params["timeInForce"] = "GTC"
        else:
            params["type"] = "MARKET"

        params["symbol"] = market
        params["side"] = side
        params["quantity"] = '%.8f' % quantity

        return params

    def _format(self, price):
        return "{:.8f}".format(price)

    def _delete(self, path, params={}):
        params.update({"recvWindow": 120000})
        query = urlencode(self._sign(params))
        url = "%s?%s" % (path, query)
        header = {"X-MBX-APIKEY": self.key}
        return requests.delete(url, headers=header, \
            timeout=30, verify=True, proxies=self.proxies).json()