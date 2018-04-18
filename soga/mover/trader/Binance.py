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

    def tickers(self):
        #print self.get_my_trades('EOSBTC')
        #print self.get_my_trades('EOSETH')
        #sys.exit()
        decimal.getcontext().prec = 4

        #汇率计算价格
        #cny_usd = self.get_cny_usd()
        #cny_usd = Decimal(cny_usd)
        cny_usd = Decimal(u'6.2667')

        self.binance_api()
        tickers = self.client.get_all_tickers()
        #print tickers
        #tickers = [{u'symbol': u'ETHBTC', u'price': u'0.06331900'}, {u'symbol': u'LTCBTC', u'price': u'0.01618700'}, {u'symbol': u'BNBBTC', u'price': u'0.00153500'}, {u'symbol': u'NEOBTC', u'price': u'0.00830600'}, {u'symbol': u'123456', u'price': u'0.00030000'}, {u'symbol': u'QTUMETH', u'price': u'0.03240400'}, {u'symbol': u'EOSETH', u'price': u'0.01703500'}, {u'symbol': u'SNTETH', u'price': u'0.00023160'}, {u'symbol': u'BNTETH', u'price': u'0.00618000'}, {u'symbol': u'BCCBTC', u'price': u'0.09489900'}, {u'symbol': u'GASBTC', u'price': u'0.00243400'}, {u'symbol': u'BNBETH', u'price': u'0.02426200'}, {u'symbol': u'BTCUSDT', u'price': u'7998.99000000'}, {u'symbol': u'ETHUSDT', u'price': u'506.24000000'}, {u'symbol': u'HSRBTC', u'price': u'0.00083100'}, {u'symbol': u'OAXETH', u'price': u'0.00119550'}, {u'symbol': u'DNTETH', u'price': u'0.00014406'}, {u'symbol': u'MCOETH', u'price': u'0.01523900'}, {u'symbol': u'ICNETH', u'price': u'0.00225310'}, {u'symbol': u'MCOBTC', u'price': u'0.00096900'}, {u'symbol': u'WTCBTC', u'price': u'0.00131050'}, {u'symbol': u'WTCETH', u'price': u'0.02071700'}, {u'symbol': u'LRCBTC', u'price': u'0.00007959'}, {u'symbol': u'LRCETH', u'price': u'0.00126263'}, {u'symbol': u'QTUMBTC', u'price': u'0.00205500'}, {u'symbol': u'YOYOBTC', u'price': u'0.00001242'}, {u'symbol': u'OMGBTC', u'price': u'0.00192600'}, {u'symbol': u'OMGETH', u'price': u'0.03049500'}, {u'symbol': u'ZRXBTC', u'price': u'0.00009382'}, {u'symbol': u'ZRXETH', u'price': u'0.00148000'}, {u'symbol': u'STRATBTC', u'price': u'0.00060990'}, {u'symbol': u'STRATETH', u'price': u'0.00961000'}, {u'symbol': u'SNGLSBTC', u'price': u'0.00001120'}, {u'symbol': u'SNGLSETH', u'price': u'0.00017750'}, {u'symbol': u'BQXBTC', u'price': u'0.00031399'}, {u'symbol': u'BQXETH', u'price': u'0.00495090'}, {u'symbol': u'KNCBTC', u'price': u'0.00017315'}, {u'symbol': u'KNCETH', u'price': u'0.00272800'}, {u'symbol': u'FUNBTC', u'price': u'0.00000507'}, {u'symbol': u'FUNETH', u'price': u'0.00008006'}, {u'symbol': u'SNMBTC', u'price': u'0.00001991'}, {u'symbol': u'SNMETH', u'price': u'0.00031386'}, {u'symbol': u'NEOETH', u'price': u'0.13100000'}, {u'symbol': u'IOTABTC', u'price': u'0.00019956'}, {u'symbol': u'IOTAETH', u'price': u'0.00315716'}, {u'symbol': u'LINKBTC', u'price': u'0.00005150'}, {u'symbol': u'LINKETH', u'price': u'0.00081489'}, {u'symbol': u'XVGBTC', u'price': u'0.00001245'}, {u'symbol': u'XVGETH', u'price': u'0.00019700'}, {u'symbol': u'SALTBTC', u'price': u'0.00033880'}, {u'symbol': u'SALTETH', u'price': u'0.00536100'}, {u'symbol': u'MDABTC', u'price': u'0.00011551'}, {u'symbol': u'MDAETH', u'price': u'0.00182500'}, {u'symbol': u'MTLBTC', u'price': u'0.00047190'}, {u'symbol': u'MTLETH', u'price': u'0.00745400'}, {u'symbol': u'SUBBTC', u'price': u'0.00007636'}, {u'symbol': u'SUBETH', u'price': u'0.00121055'}, {u'symbol': u'EOSBTC', u'price': u'0.00107960'}, {u'symbol': u'SNTBTC', u'price': u'0.00001470'}, {u'symbol': u'ETCETH', u'price': u'0.03196600'}, {u'symbol': u'ETCBTC', u'price': u'0.00201800'}, {u'symbol': u'MTHBTC', u'price': u'0.00001139'}, {u'symbol': u'MTHETH', u'price': u'0.00017995'}, {u'symbol': u'ENGBTC', u'price': u'0.00023005'}, {u'symbol': u'ENGETH', u'price': u'0.00363910'}, {u'symbol': u'DNTBTC', u'price': u'0.00000911'}, {u'symbol': u'ZECBTC', u'price': u'0.02801200'}, {u'symbol': u'ZECETH', u'price': u'0.44101000'}, {u'symbol': u'BNTBTC', u'price': u'0.00039142'}, {u'symbol': u'ASTBTC', u'price': u'0.00005222'}, {u'symbol': u'ASTETH', u'price': u'0.00082570'}, {u'symbol': u'DASHBTC', u'price': u'0.04506800'}, {u'symbol': u'DASHETH', u'price': u'0.71083000'}, {u'symbol': u'OAXBTC', u'price': u'0.00007562'}, {u'symbol': u'ICNBTC', u'price': u'0.00014299'}, {u'symbol': u'BTGBTC', u'price': u'0.00642600'}, {u'symbol': u'BTGETH', u'price': u'0.10169000'}, {u'symbol': u'EVXBTC', u'price': u'0.00015190'}, {u'symbol': u'EVXETH', u'price': u'0.00238350'}, {u'symbol': u'REQBTC', u'price': u'0.00002611'}, {u'symbol': u'REQETH', u'price': u'0.00041143'}, {u'symbol': u'VIBBTC', u'price': u'0.00002143'}, {u'symbol': u'VIBETH', u'price': u'0.00034129'}, {u'symbol': u'HSRETH', u'price': u'0.01317200'}, {u'symbol': u'TRXBTC', u'price': u'0.00000524'}, {u'symbol': u'TRXETH', u'price': u'0.00008270'}, {u'symbol': u'POWRBTC', u'price': u'0.00005180'}, {u'symbol': u'POWRETH', u'price': u'0.00082237'}, {u'symbol': u'ARKBTC', u'price': u'0.00032810'}, {u'symbol': u'ARKETH', u'price': u'0.00519800'}, {u'symbol': u'YOYOETH', u'price': u'0.00019370'}, {u'symbol': u'XRPBTC', u'price': u'0.00008229'}, {u'symbol': u'XRPETH', u'price': u'0.00130000'}, {u'symbol': u'MODBTC', u'price': u'0.00031760'}, {u'symbol': u'MODETH', u'price': u'0.00498900'}, {u'symbol': u'ENJBTC', u'price': u'0.00001452'}, {u'symbol': u'ENJETH', u'price': u'0.00022925'}, {u'symbol': u'STORJBTC', u'price': u'0.00011896'}, {u'symbol': u'STORJETH', u'price': u'0.00188370'}, {u'symbol': u'BNBUSDT', u'price': u'12.27160000'}, {u'symbol': u'VENBNB', u'price': u'0.27050000'}, {u'symbol': u'YOYOBNB', u'price': u'0.00809000'}, {u'symbol': u'POWRBNB', u'price': u'0.03401000'}, {u'symbol': u'VENBTC', u'price': u'0.00041355'}, {u'symbol': u'VENETH', u'price': u'0.00653442'}, {u'symbol': u'KMDBTC', u'price': u'0.00043350'}, {u'symbol': u'KMDETH', u'price': u'0.00687800'}, {u'symbol': u'NULSBNB', u'price': u'0.18268000'}, {u'symbol': u'RCNBTC', u'price': u'0.00001473'}, {u'symbol': u'RCNETH', u'price': u'0.00023159'}, {u'symbol': u'RCNBNB', u'price': u'0.00954000'}, {u'symbol': u'NULSBTC', u'price': u'0.00028097'}, {u'symbol': u'NULSETH', u'price': u'0.00440000'}, {u'symbol': u'RDNBTC', u'price': u'0.00021020'}, {u'symbol': u'RDNETH', u'price': u'0.00332010'}, {u'symbol': u'RDNBNB', u'price': u'0.13545000'}, {u'symbol': u'XMRBTC', u'price': u'0.02421100'}, {u'symbol': u'XMRETH', u'price': u'0.38233000'}, {u'symbol': u'DLTBNB', u'price': u'0.01601000'}, {u'symbol': u'WTCBNB', u'price': u'0.85100000'}, {u'symbol': u'DLTBTC', u'price': u'0.00002458'}, {u'symbol': u'DLTETH', u'price': u'0.00038570'}, {u'symbol': u'AMBBTC', u'price': u'0.00004438'}, {u'symbol': u'AMBETH', u'price': u'0.00070111'}, {u'symbol': u'AMBBNB', u'price': u'0.02870000'}, {u'symbol': u'BCCETH', u'price': u'1.50090000'}, {u'symbol': u'BCCUSDT', u'price': u'759.63000000'}, {u'symbol': u'BCCBNB', u'price': u'61.75000000'}, {u'symbol': u'BATBTC', u'price': u'0.00003372'}, {u'symbol': u'BATETH', u'price': u'0.00053400'}, {u'symbol': u'BATBNB', u'price': u'0.02211000'}, {u'symbol': u'BCPTBTC', u'price': u'0.00005948'}, {u'symbol': u'BCPTETH', u'price': u'0.00094389'}, {u'symbol': u'BCPTBNB', u'price': u'0.03886000'}, {u'symbol': u'ARNBTC', u'price': u'0.00015500'}, {u'symbol': u'ARNETH', u'price': u'0.00243980'}, {u'symbol': u'GVTBTC', u'price': u'0.00245360'}, {u'symbol': u'GVTETH', u'price': u'0.03879700'}, {u'symbol': u'CDTBTC', u'price': u'0.00000586'}, {u'symbol': u'CDTETH', u'price': u'0.00009244'}, {u'symbol': u'GXSBTC', u'price': u'0.00036060'}, {u'symbol': u'GXSETH', u'price': u'0.00568600'}, {u'symbol': u'NEOUSDT', u'price': u'66.36800000'}, {u'symbol': u'NEOBNB', u'price': u'5.39500000'}, {u'symbol': u'POEBTC', u'price': u'0.00000503'}, {u'symbol': u'POEETH', u'price': u'0.00007958'}, {u'symbol': u'QSPBTC', u'price': u'0.00001981'}, {u'symbol': u'QSPETH', u'price': u'0.00031380'}, {u'symbol': u'QSPBNB', u'price': u'0.01292000'}, {u'symbol': u'BTSBTC', u'price': u'0.00002660'}, {u'symbol': u'BTSETH', u'price': u'0.00041995'}, {u'symbol': u'BTSBNB', u'price': u'0.01738000'}, {u'symbol': u'XZCBTC', u'price': u'0.00410300'}, {u'symbol': u'XZCETH', u'price': u'0.06509900'}, {u'symbol': u'XZCBNB', u'price': u'2.69000000'}, {u'symbol': u'LSKBTC', u'price': u'0.00132360'}, {u'symbol': u'LSKETH', u'price': u'0.02087300'}, {u'symbol': u'LSKBNB', u'price': u'0.86180000'}, {u'symbol': u'TNTBTC', u'price': u'0.00001218'}, {u'symbol': u'TNTETH', u'price': u'0.00019229'}, {u'symbol': u'FUELBTC', u'price': u'0.00000921'}, {u'symbol': u'FUELETH', u'price': u'0.00014590'}, {u'symbol': u'MANABTC', u'price': u'0.00001182'}, {u'symbol': u'MANAETH', u'price': u'0.00018764'}, {u'symbol': u'BCDBTC', u'price': u'0.00294300'}, {u'symbol': u'BCDETH', u'price': u'0.04620000'}, {u'symbol': u'DGDBTC', u'price': u'0.03024600'}, {u'symbol': u'DGDETH', u'price': u'0.47821000'}, {u'symbol': u'IOTABNB', u'price': u'0.13022000'}, {u'symbol': u'ADXBTC', u'price': u'0.00009419'}, {u'symbol': u'ADXETH', u'price': u'0.00148670'}, {u'symbol': u'ADXBNB', u'price': u'0.06103000'}, {u'symbol': u'ADABTC', u'price': u'0.00003341'}, {u'symbol': u'ADAETH', u'price': u'0.00052848'}, {u'symbol': u'PPTBTC', u'price': u'0.00316510'}, {u'symbol': u'PPTETH', u'price': u'0.04997700'}, {u'symbol': u'CMTBTC', u'price': u'0.00001261'}, {u'symbol': u'CMTETH', u'price': u'0.00019975'}, {u'symbol': u'CMTBNB', u'price': u'0.00821000'}, {u'symbol': u'XLMBTC', u'price': u'0.00003522'}, {u'symbol': u'XLMETH', u'price': u'0.00055571'}, {u'symbol': u'XLMBNB', u'price': u'0.02304000'}, {u'symbol': u'CNDBTC', u'price': u'0.00001079'}, {u'symbol': u'CNDETH', u'price': u'0.00017026'}, {u'symbol': u'CNDBNB', u'price': u'0.00704000'}, {u'symbol': u'LENDBTC', u'price': u'0.00000703'}, {u'symbol': u'LENDETH', u'price': u'0.00011120'}, {u'symbol': u'WABIBTC', u'price': u'0.00012256'}, {u'symbol': u'WABIETH', u'price': u'0.00193000'}, {u'symbol': u'WABIBNB', u'price': u'0.07944000'}, {u'symbol': u'LTCETH', u'price': u'0.25565000'}, {u'symbol': u'LTCUSDT', u'price': u'129.40000000'}, {u'symbol': u'LTCBNB', u'price': u'10.54000000'}, {u'symbol': u'TNBBTC', u'price': u'0.00000478'}, {u'symbol': u'TNBETH', u'price': u'0.00007508'}, {u'symbol': u'WAVESBTC', u'price': u'0.00060190'}, {u'symbol': u'WAVESETH', u'price': u'0.00950300'}, {u'symbol': u'WAVESBNB', u'price': u'0.39360000'}, {u'symbol': u'GTOBTC', u'price': u'0.00003205'}, {u'symbol': u'GTOETH', u'price': u'0.00050745'}, {u'symbol': u'GTOBNB', u'price': u'0.02089000'}, {u'symbol': u'ICXBTC', u'price': u'0.00035910'}, {u'symbol': u'ICXETH', u'price': u'0.00568300'}, {u'symbol': u'ICXBNB', u'price': u'0.23503000'}, {u'symbol': u'OSTBTC', u'price': u'0.00002409'}, {u'symbol': u'OSTETH', u'price': u'0.00038062'}, {u'symbol': u'OSTBNB', u'price': u'0.01583000'}, {u'symbol': u'ELFBTC', u'price': u'0.00012608'}, {u'symbol': u'ELFETH', u'price': u'0.00199332'}, {u'symbol': u'AIONBTC', u'price': u'0.00037340'}, {u'symbol': u'AIONETH', u'price': u'0.00590900'}, {u'symbol': u'AIONBNB', u'price': u'0.24300000'}, {u'symbol': u'NEBLBTC', u'price': u'0.00122150'}, {u'symbol': u'NEBLETH', u'price': u'0.01929900'}, {u'symbol': u'NEBLBNB', u'price': u'0.79117000'}, {u'symbol': u'BRDBTC', u'price': u'0.00006731'}, {u'symbol': u'BRDETH', u'price': u'0.00106230'}, {u'symbol': u'BRDBNB', u'price': u'0.04364000'}, {u'symbol': u'MCOBNB', u'price': u'0.62595000'}, {u'symbol': u'EDOBTC', u'price': u'0.00022920'}, {u'symbol': u'EDOETH', u'price': u'0.00363600'}, {u'symbol': u'WINGSBTC', u'price': u'0.00006300'}, {u'symbol': u'WINGSETH', u'price': u'0.00100140'}, {u'symbol': u'NAVBTC', u'price': u'0.00014170'}, {u'symbol': u'NAVETH', u'price': u'0.00222700'}, {u'symbol': u'NAVBNB', u'price': u'0.09239000'}, {u'symbol': u'LUNBTC', u'price': u'0.00127260'}, {u'symbol': u'LUNETH', u'price': u'0.02008400'}, {u'symbol': u'TRIGBTC', u'price': u'0.00012020'}, {u'symbol': u'TRIGETH', u'price': u'0.00190200'}, {u'symbol': u'TRIGBNB', u'price': u'0.07800000'}, {u'symbol': u'APPCBTC', u'price': u'0.00005498'}, {u'symbol': u'APPCETH', u'price': u'0.00087000'}, {u'symbol': u'APPCBNB', u'price': u'0.03584000'}, {u'symbol': u'VIBEBTC', u'price': u'0.00002711'}, {u'symbol': u'VIBEETH', u'price': u'0.00043050'}, {u'symbol': u'RLCBTC', u'price': u'0.00014970'}, {u'symbol': u'RLCETH', u'price': u'0.00236100'}, {u'symbol': u'RLCBNB', u'price': u'0.09750000'}, {u'symbol': u'INSBTC', u'price': u'0.00015890'}, {u'symbol': u'INSETH', u'price': u'0.00252000'}, {u'symbol': u'PIVXBTC', u'price': u'0.00056660'}, {u'symbol': u'PIVXETH', u'price': u'0.00892300'}, {u'symbol': u'PIVXBNB', u'price': u'0.36769000'}, {u'symbol': u'IOSTBTC', u'price': u'0.00000443'}, {u'symbol': u'IOSTETH', u'price': u'0.00006976'}, {u'symbol': u'CHATBTC', u'price': u'0.00001120'}, {u'symbol': u'CHATETH', u'price': u'0.00017660'}, {u'symbol': u'STEEMBTC', u'price': u'0.00034260'}, {u'symbol': u'STEEMETH', u'price': u'0.00542200'}, {u'symbol': u'STEEMBNB', u'price': u'0.22325000'}, {u'symbol': u'NANOBTC', u'price': u'0.00074780'}, {u'symbol': u'NANOETH', u'price': u'0.01181000'}, {u'symbol': u'NANOBNB', u'price': u'0.48580000'}, {u'symbol': u'VIABTC', u'price': u'0.00023990'}, {u'symbol': u'VIAETH', u'price': u'0.00378100'}, {u'symbol': u'VIABNB', u'price': u'0.15462000'}, {u'symbol': u'BLZBTC', u'price': u'0.00005710'}, {u'symbol': u'BLZETH', u'price': u'0.00090051'}, {u'symbol': u'BLZBNB', u'price': u'0.03703000'}, {u'symbol': u'AEBTC', u'price': u'0.00022080'}, {u'symbol': u'AEETH', u'price': u'0.00347600'}, {u'symbol': u'AEBNB', u'price': u'0.14350000'}, {u'symbol': u'RPXBTC', u'price': u'0.00001151'}, {u'symbol': u'RPXETH', u'price': u'0.00018204'}, {u'symbol': u'RPXBNB', u'price': u'0.00748000'}, {u'symbol': u'NCASHBTC', u'price': u'0.00000525'}, {u'symbol': u'NCASHETH', u'price': u'0.00008309'}, {u'symbol': u'NCASHBNB', u'price': u'0.00343000'}, {u'symbol': u'POABTC', u'price': u'0.00006486'}, {u'symbol': u'POAETH', u'price': u'0.00102646'}, {u'symbol': u'POABNB', u'price': u'0.04230000'}, {u'symbol': u'ZILBTC', u'price': u'0.00000795'}, {u'symbol': u'ZILETH', u'price': u'0.00012558'}, {u'symbol': u'ZILBNB', u'price': u'0.00516000'}, {u'symbol': u'ONTBTC', u'price': u'0.00050840'}, {u'symbol': u'ONTETH', u'price': u'0.00803300'}, {u'symbol': u'ONTBNB', u'price': u'0.33112000'}, {u'symbol': u'STORMBTC', u'price': u'0.00000447'}, {u'symbol': u'STORMETH', u'price': u'0.00007090'}, {u'symbol': u'STORMBNB', u'price': u'0.00293000'}, {u'symbol': u'QTUMBNB', u'price': u'1.33584000'}, {u'symbol': u'QTUMUSDT', u'price': u'16.35700000'}, {u'symbol': u'XEMBTC', u'price': u'0.00004164'}, {u'symbol': u'XEMETH', u'price': u'0.00066172'}, {u'symbol': u'XEMBNB', u'price': u'0.02722000'}, {u'symbol': u'WANBTC', u'price': u'0.00067990'}, {u'symbol': u'WANETH', u'price': u'0.01072400'}, {u'symbol': u'WANBNB', u'price': u'0.44328000'}, {u'symbol': u'WPRBTC', u'price': u'0.00001643'}, {u'symbol': u'WPRETH', u'price': u'0.00025990'}, {u'symbol': u'QLCBTC', u'price': u'0.00001966'}, {u'symbol': u'QLCETH', u'price': u'0.00031118'}, {u'symbol': u'SYSBTC', u'price': u'0.00004714'}, {u'symbol': u'SYSETH', u'price': u'0.00074737'}, {u'symbol': u'SYSBNB', u'price': u'0.03046000'}, {u'symbol': u'QLCBNB', u'price': u'0.01278000'}, {u'symbol': u'GRSBTC', u'price': u'0.00009145'}, {u'symbol': u'GRSETH', u'price': u'0.00144710'}, {u'symbol': u'ADAUSDT', u'price': u'0.26700000'}, {u'symbol': u'ADABNB', u'price': u'0.02170000'}]
        ticker_data = dict()
        for x in xrange(0, len(tickers)):
            #print('%s: %s' % (tickers[x]['symbol'], tickers[x]['price']))
            ticker_data[tickers[x]['symbol']] = tickers[x]
        btc = Decimal(ticker_data['BTCUSDT']['price'])
        eth = Decimal(ticker_data['ETHUSDT']['price'])
        #print btc

        #手续费
        #
        #04-17 21:45:12  EOS/BTC 限价  卖   0.0010864   0.0010864   1.00    1.00    0.0010864   --  完全成交
        #04-17 21:44:23  EOS/ETH 限价  买   0.017088    0.017088    1.00    1.00    0.017088    --

        #bnb_rate = 用 bnb 万分之五
        ethtobtc = Decimal(eth / btc);

        print "%s====%s===%s" % (btc, eth, ethtobtc)

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

            order_btc = self.get_order_books(p1_code, 5)
            #print orders
            ifbb_btc = Decimal(order_btc['bids'][0][0]) * btc * cny_usd
            ifss_btc = Decimal(order_btc['asks'][0][0]) * btc * cny_usd


            order_eth = self.get_order_books(p2_code, 5)
            #print orders
            ifbb_eth = Decimal(order_eth['bids'][0][0]) * eth * cny_usd
            ifss_eth = Decimal(order_eth['asks'][0][0]) * eth * cny_usd


            #从最小值开始买进
            minA = min(ifbb_btc, ifbb_eth)
            #whomax = p1_code
            profit = ((ifbb_eth - ifbb_btc) /  ifbb_btc) * 100
            whobuy = p1_code
            whosell = p2_code
            buy_price = ifbb_btc
            sell_price = ifbb_eth
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

            if whobuy in buyList:
                continue
            buyList.append(whobuy)

            if profit < 1.1:
                continue
            print u"%s实时盘口=M1:%s==S1:%s" % (p1_code, ifbb_btc, ifss_btc)
            print u"%s实时盘口=M1:%s==S1:%s" % (p2_code, ifbb_eth, ifss_eth)
            print "B:%s===S:%s===whobuy(%s)===whosell(%s)===BTC:%s===ETH:%s===P:%s===BuyNum:%s" % (buy_price, sell_price, whobuy, whosell, Decimal(btc * cny_usd), Decimal(eth * cny_usd), profit, buynum)

            if buynum > 1:
                buynum = int(buynum)
            else:
                buynum = "{:.3f}".format(buynum)
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

