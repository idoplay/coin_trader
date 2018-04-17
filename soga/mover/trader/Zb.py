# -*- coding: utf-8 -*-
from mover.api.ZbApi import *


class ZbTrader(ZbApi):

    def __init__(self):
        ZbApi.__init__(self)

    def account_info(self):
        account_info = json.loads(self.query_account())
        coins = account_info['result']['coins']
        for x in xrange(0,len(coins)):
            freez = float(coins[x]['freez'])
            available = float(coins[x]['available'])
            enName = coins[x]['enName']
            if freez > 0 or available > 0.001 or coins[x]['enName'] =='ZB':
                freez = '%.2f' % freez
                available = '%.2f' % available
                self.print_green("%s==%s==%s" % (enName,available,freez))

    def get_user_address(self):
        return self.config['zb_config']['currency']
        '''
        for key in a.keys():
            b = self.query_user_address(key)
            print b
            print(key+':'+a[key]['address'])
        '''

    def get_markets(self):
        account_info = json.loads(self.query_markets())
        print account_info

