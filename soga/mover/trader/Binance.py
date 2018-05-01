# -*- coding: utf-8 -*-
from mover.api.BinanceApi import *
import decimal
from  decimal import Decimal

class BinanceTrader(BinanceApi):

    def __init__(self):
        BinanceApi.__init__(self)

    def account_info(self):
        balances = self.get_account()
        for balance in balances['balances']:
            if float(balance['locked']) > 0 or float(balance['free']) > 0:
                print('%s: %s' % (balance['asset'], balance['free']))


    def _make_code(self, keystr):
        quoteAsset = keystr[-3:]
        if quoteAsset == 'BTC':
            return '%sETH'
        else:
            return '%sBTC'

    def filters(self):
        #生成一份过滤清单,去掉不活跃的品种,24小时成交量小于100W
        coins = self.get_products()
        decimal.getcontext().prec = 16
        badlist = []
        for coin in coins['data']:

            if coin['quoteAsset'] == 'BNB':
                pr = self.bnbP
            elif coin['quoteAsset'] == 'ETH':
                pr = self.ethP
            elif coin['quoteAsset'] == 'BTC':
                pr = self.btcP
            else:
                continue

            #print pr
            #print type(pr)
            tradedMoney = Decimal(coin['tradedMoney']) * pr
            if tradedMoney < 1000000:
                badlist.append(coin['symbol'])
                print "%s===%s" % (coin['symbol'], tradedMoney)
                continue

        return badlist
            #
            #print type(tradedMoney)
            #print Decimal(tradedMoney)
            #sys.exit()


    def tickers(self):
        decimal.getcontext().prec = 10

        #汇率计算价格
        #cny_usd = self.get_cny_usd()
        #cny_usd = Decimal(cny_usd)
        cny_usd = Decimal('6.2767')
        #生成一份过滤清单,去掉不活跃的品种

        #self.binance_api()
        tickers = self.get_all_tickers()

        ticker_data = dict()
        #for x in xrange(0, len(tickers)):
        for ticker in tickers:
            ticker_data[ticker['symbol']] = ticker
            #print('%s: %s' % (tickers[x]['symbol'], tickers[x]['price']))
            #ticker_data[tickers[x]['symbol']] = tickers[x]
        btc = Decimal(ticker_data['BTCUSDT']['price'])
        eth = Decimal(ticker_data['ETHUSDT']['price'])
        bnb = Decimal(ticker_data['BNBUSDT']['price'])

        self.ethP = eth * cny_usd
        self.btcP = btc * cny_usd
        self.bnbP = bnb * cny_usd

        print "%s====%s===%s" % (self.btcP, self.ethP, self.bnbP)
        #bnb_rate = 用 bnb 万分之五

        #badlist = self.filters()
        #decimal.getcontext().prec = 8
        #print badlist

        #sys.exit()

        buyList = []
        trkeys = ticker_data.keys()
        for (k,v) in  ticker_data.items():
            if k[-4:] == 'USDT' or k == 'ETHBTC':
                continue

            isend = k[-3:]
            if isend == 'BTC':
                p1_code = k
                p2_code = self._make_code(k) % k[0:-3]
                if p2_code not in trkeys:
                    continue
            elif isend == 'ETH':
                p1_code = self._make_code(k) % k[0:-3]
                if p1_code not in trkeys:
                    continue
                p2_code = k

            #print 1111
            pA = Decimal(ticker_data[p1_code]['price'])
            pB = Decimal(ticker_data[p2_code]['price'])
            #print "%s==%s==%s===%s" % (p1_code, p2_code, pA, pB)
            #if isend == 'BTC':
            pA = pA * self.btcP
            pB = pB * self.ethP
            #else:
            #pA = pA * eth * cny_usd
            #pB = pB * btc * cny_usd
            vmax = max(pA, pB)
            vmin = min(pA, pB)

            #print "%s==%s==%s===%s" % (p1_code, p2_code, pA, pB)
            vprofit = ((vmax - vmin) / vmax) * 100
            #print vprofit
            if p1_code in buyList:
                continue
            buyList.append(p1_code)

            #continue
            if vprofit < 1.1:
                continue

            print "B:%s===S:%s===(%s)===(%s)===BTC:%s===ETH:%s===P:%s" % (pA,pB,p1_code,p2_code,self.btcP, self.ethP, vprofit)
            #print 1111
            order_btc = self.get_book_ticker(p1_code)
            #print orders
            ifbb_btc = Decimal(order_btc['bidPrice']) * self.btcP
            ifss_btc = Decimal(order_btc['askPrice']) * self.btcP
            ifnu_btc = Decimal(order_btc['bidQty'])

            #order_eth = self.get_order_books(p2_code, 5)
            order_eth = self.get_book_ticker(p2_code)
            #print orders
            ifbb_eth = Decimal(order_eth['bidPrice']) * self.ethP
            ifss_eth = Decimal(order_eth['askPrice']) * self.ethP
            ifnu_eth = Decimal(order_eth['bidQty'])


            #从最小值开始买进
            minA = min(ifbb_btc, ifbb_eth)
            #whomax = p1_code
            profit = ((ifbb_eth - ifbb_btc) /  ifbb_btc) * 100
            whobuy = p1_code
            whosell = p2_code
            buy_price = ifbb_btc
            sell_price = ifbb_eth
            real_vol = ifnu_btc
            #btc入eth出

            #当前应该买入eth的单位
            #sb_m = eth
            #sb_s = btc
            #单次交易金额为100元等值
            maxMoney = Decimal(u'50')
            #if profit > 1.8:
            #    maxMoney = Decimal(u'300')

            #换算成btc或eth购买的数量
            buynum = Decimal(maxMoney/ifbb_btc)

            if minA == ifbb_eth:
                profit = ((ifbb_btc - ifbb_eth) /  ifbb_eth) * 100
                whobuy = p2_code
                whosell = p1_code
                buynum = Decimal(maxMoney/ifbb_eth)
                buy_price = ifbb_eth
                sell_price = ifbb_btc
                real_vol = ifnu_eth
            #实时利润
            if profit < 1.1:
                continue

            print u"%s实时盘口=M1:%s==S1:%s" % (p1_code, ifbb_btc, ifss_btc)
            print u"%s实时盘口=M1:%s==S1:%s" % (p2_code, ifbb_eth, ifss_eth)
            print "B:%s===S:%s===WB(%s)===WS(%s)===BTC:%s===ETH:%s===P:%s===RealVolume:%s===BuyNum:%s" % (buy_price, sell_price, whobuy, whosell, self.btcP, self.ethP, profit, real_vol, buynum)

            if real_vol < buynum:
                buynum = real_vol
            if buynum > 1:
                buynum = int(buynum)
            else:
                buynum = "{:.3f}".format(buynum)

            continue
            buyRes = self.buy_market(whobuy, buynum)
            print buyRes
            origQty = buyRes['executedQty']
            print self.sell_market(whosell, buynum)
            #sys.exit()
        sys.exit()
        '''
            #print v
            #print k
            #p1code 都是btc开始
            isend = k[-3:]
            #print isend
            if isend == 'BTC':
                p1_code = k
                p2_code = self._make_code(k) % k[0:-3]
                if p2_code not in trkeys:
                    continue
                p1 = Decimal(v['price']) * btc * cny_usd
                p2 = Decimal(ticker_data[p2_code]['price']) * eth * cny_usd

                #只展示不用于计算
                p1_price = v['price']
                p2_price = ticker_data[p2_code]['price']

            elif isend == 'ETH':
                p1_code = self._make_code(k) % k[0:-3]
                if p1_code not in trkeys:
                    continue
                p2_code = k
                p1 = Decimal(ticker_data[p1_code]['price']) * btc * cny_usd
                p2 = Decimal(v['price']) * eth * cny_usd

                #只展示不用于计算
                p1_price = ticker_data[p1_code]['price']
                p2_price = v['price']

            #print "%s====%s" % (p1, p2)

            maxA = max(p1, p2)
            #默认etc卖出eth买入
            whomax = p1_code
            profit = ((p1 - p2) /  p1) * 100
            whobuy = p2_code
            whosell = p1_code
            #当前应该买入eth的单位
            sb_m = eth
            sb_s = btc
            #单次交易金额为100元等值
            maxMoney = Decimal(u'50')
            #if profit > 1.8:
            #    maxMoney = Decimal(u'300')

            #换算成btc或eth购买的数量
            buynum = Decimal(maxMoney/p2)
            if maxA == p2:
                whomax = p2_code
                profit = ((p2 - p1) /  p2) * 100
                whobuy = p1_code
                whosell = p2_code
                #默认btc买入
                sb_m = btc
                sb_s = eth
                #if profit > 1.8:
                #    maxMoney = u'100'
                buynum = Decimal(maxMoney/p1)

            if whobuy in buyList:
                continue
            buyList.append(whobuy)

            if profit > 1.1:
                print "%s(%s)===%s(%s)===BTC:%s===ETH:%s==Buy:%s===Sell:%s===P:%s====BuyNum:%s" % (p1, p1_price, p2, p2_price, Decimal(btc * cny_usd), Decimal(eth * cny_usd), whobuy, whosell, profit, buynum)
                orders = self.get_order_books(whobuy, 5)
                print orders
                ifbb = Decimal(orders['bids'][0][0]) * sb_m * cny_usd
                ifss = Decimal(orders['asks'][0][0]) * sb_m * cny_usd
                print u"预计买入实时盘口=M1:%s==S1:%s" % (ifbb, ifss)

                orders2 = self.get_order_books(whosell, 5)
                print orders2
                ifbb2 = Decimal(orders2['bids'][0][0]) * sb_s * cny_usd
                ifss2 = Decimal(orders2['asks'][0][0]) * sb_s * cny_usd
                print u"预计卖出实时盘口=M1:%s==S1:%s" % (ifbb2, ifss2)



            #获取实际盘口,确认是否可以交易

            if profit < 1.7:
                continue


            #buynum = "{:.3f}".format(float(buynum))
            #0.00064819
            #print "%s===%s===%s" % (p1, p2, maxA)
            print whomax

            if p1 > 700:
                continue



            if buynum > 1:
                buynum = int(buynum)
            else:
                buynum = "{:.3f}".format(price)

            print buynum
            #sys.exit()
            #buyRes = self.buy_market(whobuy, buynum)
            #print buyRes
            #origQty = buyRes['executedQty']executedQty
            #print self.sell_market(whosell, buynum)
            #sys.exit()
        sys.exit()

        #计算利润最大化执行一笔交易
        symbol = 'CDTETH'
        num = 1


        self.profits()
        sys.exit()
        #orders = self.get_order_books(symbol, 5)
        #print orders
        orders = {u'lastUpdateId': 15090118, u'bids': [[u'0.00009303', u'38856.00000000', []], [u'0.00009265', u'600.00000000', []], [u'0.00009264', u'2158.00000000', []], [u'0.00009251', u'621.00000000', []], [u'0.00009231', u'2245.00000000', []]], u'asks': [[u'0.00009319', u'639.00000000', []], [u'0.00009332', u'1059.00000000', []], [u'0.00009333', u'7481.00000000', []], [u'0.00009349', u'4000.00000000', []], [u'0.00009350', u'316.00000000', []]]}
        #lastBid = self._format(orders['bids'][0][0]) #last buy price (bid)
        #lastAsk = self._format(orders['asks'][0][0]) #last sell price (ask)
        lastBid = float(orders['bids'][0][0]) #last buy price (bid)
        lastAsk = float(orders['asks'][0][0]) #last sell price (ask)
        profit = (lastAsk - lastBid) /  lastBid * 100
        print('%.2f%% profit : %s (bid:%.8f-ask%.8f)' % (profit, symbol, lastBid, lastAsk))
        '''


    def profits(self, asset='BTC'):

        btc = 51034
        eth = 3225

        #77.57 eos

        ethtobtc = 0.063181

        #btc=10000000
        btc=50000

        p1 = 1 * 0.00108
        p1_code = 'EOSBTC'
        p2 = 1 * ethtobtc * 0.015102
        p2_code = 'EOSETH'
        p1 = float(p1*btc)
        p2 = float(p2*btc)

        maxA = max(p1, p2)

        #单次交易金额为100元等值
        maxMoney = 100

        vv = float(100)/float(btc)
        buynum = self._format(vv)
        print "%s===%s===%s" % (p1, p2, maxA)
        whomax = p1_code
        profit = ((p1 - p2) /  p1) * 100
        print('%.2f%% profit ' % (profit))

        whobuy = p2_code
        whosell = p1_code
        if maxA == p2:
            whomax = p2_code
            profit = ((p2 - p1) /  p2) * 100

            whobuy = p1_code
            whosell = p2_code

        print whomax

        print "%s===%s===Buy:%s===Sell:%s===P:%s====BuyNum:%s" % (p1, p2, whobuy, whosell, profit, buynum)


        #print whomax

        sys.exit()

        if p1 > p2:
            profitA = (p1-p2)/p1 * 100
        elif p2 > p1:
            profitA = (p2-p1)/p2 * 100

        print "%s====%s" % (p1*btc, p2*btc)
        sys.exit()

        coins = self.get_products()
        for coin in coins['data']:
            if coin['symbol'] != 'BNBBTC' and coin['symbol'] != 'BNBETH':
                continue
            orders = self.get_order_books(coin['symbol'], 5)
            lastBid = float(orders['bids'][0][0]) #last buy price (bid)
            lastAsk = float(orders['asks'][0][0]) #last sell price (ask)

            profit = (lastAsk - lastBid) /  lastBid * 100

            print('%.2f%% profit : %s (bid:%.8f-ask%.8f)' % (profit, coin['symbol'], lastBid, lastAsk))

    def exchange_info(self):
        print self.get_exchange_info()



    def my_trades(self):
        #交易历史最大500条
        #print self.get_book_ticker(symbol)
        '''
        自动交易返回
        #self.buy_market(symbol, num)
        #print self.sell_market(symbol, num)
        {u'orderId': 8104847, u'clientOrderId': u'yxxa2d0UqdJ34eZPkVBw8i', u'origQty': u'1.00000000', u'symbol': u'CDTETH', u'side': u'SELL', u'timeInForce': u'GTC', u'status': u'FILLED', u'transactTime': 1523946161606, u'type': u'MARKET', u'price': u'0.00000000', u'executedQty': u'1.00000000'}

        [
        {u'orderId': 23079803, u'isBuyer': True, u'price': u'0.01600000', u'isMaker': False, u'qty': u'10.00000000', u'commission': u'0.00328150', u'time': 1523926563431, u'commissionAsset': u'BNB', u'id': 6505070, u'isBestMatch': True},
        {u'orderId': 23080381, u'isBuyer': False, u'price': u'0.01604600', u'isMaker': True, u'qty': u'10.00000000', u'commission': u'0.00329108', u'time': 1523926865455, u'commissionAsset': u'BNB', u'id': 6505239, u'isBestMatch': True}
        ]
        '''
        print self.get_my_trades('EOSETH')
