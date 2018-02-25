# -*- coding: utf-8 -*-
from mover.core.ZbApi import *


class ZbTrader(ZbApi):

    def __init__(self):
        ZbApi.__init__(self)

    def account_info(self):
        print self.query_account()
