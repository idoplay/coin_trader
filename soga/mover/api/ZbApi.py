#! -*- coding:utf-8 -*-
import json
import hashlib
import struct
import sha
import time
import sys
import base64
from mover.core.Abstract import *

suc_codes = ["1000"]

errcode = {
    "1000": "success",
    "1001": "normal error",
    "1002": "internal error",
    "1003": "verify not passed",
    "1004": "fund security password locked",
    "1005": "fund security password not right",
    "1006": "real-name authentication verifying or not passed",
    "1009": "current api not in service",
    "2001": "RMB not sufficient",
    "2002": "BTC not sufficient",
    "2003": "LTC not sufficient",
    "2005": "ETH not sufficient",
    "2006": "ETC not sufficient",
    "2007": "BTS not sufficient",
    "2009": "balance not sufficient",
    "3001": "order not found",
    "3002": "invalid amount of money",
    "3003": "invalid count",
    "3004": "user not exists",
    "3005": "illegal argument",
    "3006": "IP error",
    "3007": "time expired",
    "3008": "trade history not found",
    "4001": "API locked or not opened",
    "4002": "requests too frequently"
}

class ZbApi(Abstract):

    def __init__(self):
        Abstract.__init__(self)
        self.mykey = self.config['zb_config']['access_key']
        self.mysecret = self.config['zb_config']['access_secret']
        self.trade_host = self.config['zb_config']['trade_host']
        self.hq_host = self.config['zb_config']['hq_host']

    def __fill(self, value, lenght, fillByte):
        if len(value) >= lenght:
            return value
        else:
            fillSize = lenght - len(value)
        return value + chr(fillByte) * fillSize

    def __doXOr(self, s, value):
        slist = list(s)
        for index in xrange(len(slist)):
            slist[index] = chr(ord(slist[index]) ^ value)
        return "".join(slist)

    def __hmacSign(self, aValue, aKey):
        keyb = struct.pack("%ds" % len(aKey), str(aKey))
        value = struct.pack("%ds" % len(aValue), str(aValue))
        k_ipad = self.__doXOr(keyb, 0x36)
        k_opad = self.__doXOr(keyb, 0x5c)
        k_ipad = self.__fill(k_ipad, 64, 54)
        k_opad = self.__fill(k_opad, 64, 92)
        m = hashlib.md5()
        m.update(k_ipad)
        m.update(value)
        dg = m.digest()

        m = hashlib.md5()
        m.update(k_opad)
        subStr = dg[0:16]
        m.update(subStr)
        dg = m.hexdigest()
        return dg

    def __digest(self, aValue):
        value = struct.pack("%ds" % len(aValue), str(aValue))
        print value

        h = sha.new()
        h.update(value)
        dg = h.hexdigest()
        return dg

    def __http_get(self, url):
        if self.config['env'] == 'dev':
            httpRequest = SafeSession()
            httpRequest.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5'})
            urlx = self.config['zb_config']['dev_api'] + base64.b64encode(url)
            print urlx
            res = httpRequest.get(urlx)
            return res.text
        else:
            httpRequest = SafeSession()
            httpRequest.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5'})
            res = httpRequest.get(url)
            return res.text

    def __api_call(self, path, params=''):

        SHA_secret = self.__digest(self.mysecret)
        sign = self.__hmacSign(params, SHA_secret)
        reqTime = (int)(time.time()*1000)
        params += '&sign=%s&reqTime=%d' % (sign, reqTime)
        url = self.trade_host + path + '?' + params
        #print url
        return self.__http_get(url)

    def query_markets(self):
        url = self.hq_host+ 'markets'
        print url
        return self.__http_get(url)

    def query_account(self):
        path = 'getAccountInfo'
        params = "accesskey="+self.mykey+"&method=getAccountInfo"
        data = self.__api_call(path, params)
        #print data.text
        return data

    def query_user_address(self, currency):
        path = 'getUserAddress'
        params = "accesskey="+self.mykey+"&currency="+currency+"&method=getUserAddress"
        data = self.__api_call(path, params)
        return data


if __name__ == '__main__':
    access_key = '0'
    access_secret = '2'

    #api = ZbApi(access_key, access_secret)

    #print api.query_account()
