# -*- coding: utf-8 -*-
import urllib
import math
from mover.core.ZbApi import *


class ZbTrader(ZbApi):

    def __init__(self):
        SpiderEngine.__init__(self)

    def account_info(self):
        self.query_account()
