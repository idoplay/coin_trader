#! -*- coding:utf-8 -*-
import json
import urllib2
import hashlib
import struct
import sha
import time
import sys
from mover.core.Abstract import *


class ZbApi(Abstract):

    def __init__(self):
        Abstract.__init__(self)
        self.mykey = self.config['zb_config']['access_key']
        self.mysecret = self.config['zb_config']['access_secret']

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

    def __api_call(self, path, params=''):

        SHA_secret = self.__digest(self.mysecret)
        sign = self.__hmacSign(params, SHA_secret)
        reqTime = (int)(time.time()*1000)
        params += '&sign=%s&reqTime=%d' % (sign, reqTime)
        url = 'https://trade.zb.com/api/' + path + '?' + params
        httpRequest = SafeSession()
        httpRequest.headers.update({'User-Agent': 'Mozilla/5.0 (X11; Linux i686; U;) Gecko/20070322 Kazehakase/0.4.5'})
        res = httpRequest.get(url)
        print res
        doc = json.loads(res.text)
        #request = urllib2.Request(url)
        #response = urllib2.urlopen(request, timeout=2)
        #doc = json.loads(response.read())
        return doc


    def query_account(self):
        params = "accesskey="+self.mykey+"&method=getAccountInfo"
        path = 'getAccountInfo'

        obj = self.__api_call(path, params)
        return obj



if __name__ == '__main__':
    access_key = '0'
    access_secret = '2'

    #api = ZbApi(access_key, access_secret)

    #print api.query_account()
