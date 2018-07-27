from __future__ import (absolute_import, division, print_function,
                        unicode_literals)

import datetime  # For datetime objects
import os.path  # To manage paths
import sys  # To find out the script name (in argv[0])

# Import the backtrader platform
import backtrader as bt

####################################
# https://www.backtrader.com/docu/indautoref.html
#
####################################


# Create a Stratey
from pandas import DataFrame

from DataReading.StockDataContainer import StockDataContainer
from Strategies.StrategyFactory import StrategyFactory
from Utils.GlobalVariables import *
from Utils.common_utils import convert_backtrader_to_dataframe


class TestStrategy(bt.Strategy):
    params = (
        ('maperiod', 15),
    )

    def log(self, txt, dt=None):
        ''' Logging function fot this strategy'''
        dt = dt or self.datas[0].datetime.date(0)
        print('%s, %s' % (dt.isoformat(), txt))

    def __init__(self):
        # Keep a reference to the "close" line in the data[0] dataseries
        self.dataclose = self.datas[0].close
        self.datavol = self.datas[0].volume
        self.datahi = self.datas[0].high
        self.datalo = self.datas[0].low
        # self.dataclose = self.datas[0][GlobalVariables.get_stock_data_labels_dict()['Close']]
        # self.datavol = self.datas[0][GlobalVariables.get_stock_data_labels_dict()['Volume']]
        # self.datahi = self.datas[0][GlobalVariables.get_stock_data_labels_dict()['High']]
        # self.datalo = self.datas[0][GlobalVariables.get_stock_data_labels_dict()['Low']]
        self.buy_price = 0

        # To keep track of pending orders and buy price/commission
        self.order = None
        self.buyprice = None
        self.buycomm = None

        # Add a MovingAverageSimple indicator
        # self.sma = bt.indicators.SimpleMovingAverage(
        # self.datas[0], period=self.params.maperiod)

        self.highest_high = 0  # max (self.datahi)
        self.buyCnt = 0

        # Indicators for the plotting show

        # bt.indicators.ExponentialMovingAverage(self.datas[0], period=25)
        # bt.indicators.WeightedMovingAverage(self.datas[0], period=25,
        #                                     subplot=True)
        # bt.indicators.StochasticSlow(self.datas[0])
        # bt.indicators.MACDHisto(self.datas[0])
        # rsi = bt.indicators.RSI(self.datas[0])
        # bt.indicators.SmoothedMovingAverage(rsi, period=10)
        # bt.indicators.ATR(self.datas[0], plot=False)

        ##################################################
        # 52 w strategy
        self.w52hi_parameter_dict = {'check_days': 5, 'min_cnt': 3, 'min_vol_dev_fact': 1.2,
                                     'within52w_high_fact': 0.98}
        self.stock_screener = StrategyFactory()

    def notify_order(self, order):
        if order.status in [order.Submitted, order.Accepted]:
            # Buy/Sell order submitted/accepted to/by broker - Nothing to do
            return

        # Check if an order has been completed
        # Attention: broker could reject order if not enougth cash
        if order.status in [order.Completed]:
            if order.isbuy():
                self.log(
                    'BUY EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                    (order.executed.price,
                     order.executed.value,
                     order.executed.comm))

                self.buyprice = order.executed.price
                self.buycomm = order.executed.comm
            else:  # Sell
                self.log('SELL EXECUTED, Price: %.2f, Cost: %.2f, Comm %.2f' %
                         (order.executed.price,
                          order.executed.value,
                          order.executed.comm))

            self.bar_executed = len(self)

        elif order.status in [order.Canceled, order.Margin, order.Rejected]:
            self.log('Order Canceled/Margin/Rejected')

        # Write down: no pending order
        self.order = None

    def notify_trade(self, trade):
        if not trade.isclosed:
            return

        self.log('OPERATION PROFIT, GROSS %.2f, NET %.2f' %
                 (trade.pnl, trade.pnlcomm))

    def next(self):
        # Simply log the closing price of the series from the reference
        self.log('Close: ' + str(self.dataclose[0]) + ", volume: " + str(self.datavol[0]))
        # self.log(' from 1: Close: ' + str(self.dataclose[1]) + ", volume: " + str(self.datavol[1]))

        df1 = convert_backtrader_to_dataframe(self.datas[0])
        stock_data_container = StockDataContainer("Autodesk Inc.", "ADSK", "")
        stock_data_container.set_historical_stock_data(df1)
        stock_data_container_list = [stock_data_container]

        w52_hi_strat = self.stock_screener.prepare_strategy("W52HighTechnicalStrategy",
                                                            stock_data_container_list,
                                                            self.w52hi_parameter_dict)

        results = w52_hi_strat.run_strategy()

        # Check if an order is pending ... if yes, we cannot send a 2nd one
        if self.order:
            return

        # Check if we are in the market
        if not self.position:

            if len(results) > 0:
                # if raise_cnt < 3:
                self.buy_price = self.dataclose[0]
                self.log('BUY CREATE, %.2f' % self.dataclose[0])
                # Keep track of the created order to avoid a 2nd order
                # self.order = self.buy()
                # self.buyCnt = round((cerebro.broker.cash / self.dataclose[0]/10))  # TODO
                self.buyCnt = round((cerebro.broker.cash / self.dataclose[0])) - 10  # TODO
                self.buy(size=self.buyCnt)

        # --------------------------------------------------
        # Not yet ... we MIGHT BUY if ...
        # if self.dataclose[0] > self.sma[0]:
        #
        #     # BUY, BUY, BUY!!! (with all possible default parameters)
        #     self.log('BUY CREATE, %.2f' % self.dataclose[0])
        #
        #     # Keep track of the created order to avoid a 2nd order
        #     self.order = self.buy()
        # ------------------------------------------------------------
        else:

            cur_val = self.datalo[0]
            if cur_val > self.buy_price:
                self.buy_price = cur_val

            if cur_val < self.buy_price * 0.5:
                # SELL, SELL, SELL!!! (with all possible default parameters)
                self.log('SELL CREATE, %.2f' % self.dataclose[0])

                # Keep track of the created order to avoid a 2nd order
                self.order = self.sell(size=self.buyCnt)


# if __name__ == '__main__':
# Create a cerebro entity
cerebro = bt.Cerebro()

# Add a strategy
cerebro.addstrategy(TestStrategy)

# Datas are in a subfolder of the samples. Need to find where the script is
# because it could have been called from anywhere
# modpath = os.path.dirname(os.path.abspath(sys.argv[0]))
# datapath = os.path.join(modpath, '../../datas/orcl-1995-2014.txt')
# datapath = os.path.join(modpath, '../../datas/KMX.csv')

# Create a Data Feed
# data = bt.feeds.YahooFinanceData(
#     dataname="AAPL",
#     # Do not pass values before this date
#     fromdate=datetime.datetime(2017, 1, 2),
#     # Do not pass values before this date
#     todate=datetime.datetime(2018, 1, 2),
#     # Do not pass values after this date
#     reverse=False)

labels = []
for key, value in GlobalVariables.get_stock_data_labels_dict(False).items():
    labels.append(value)

data = [
    ('2016-09-30', 23.35, 23.91, 23.24, 23.8, 31800),
    ('2016-10-03', 23.68, 23.69, 23.39, 23.5, 31600),
    ('2016-10-04', 23.52, 23.64, 23.18, 23.28, 31700),
    ('2016-10-05', 23.28, 23.51, 23.27, 23.43, 31500),
    ('2016-10-06', 23.38, 23.56, 23.29, 23.48, 42000),
    ('2016-10-07', 23.58, 23.65, 23.37, 23.48, 43000),
    ('2016-10-10', 23.62, 23.88, 23.55, 23.77, 44000),
    ('2016-10-11', 23.62, 23.74, 23.01, 23.16, 45000),
    ('2016-10-12', 26.16, 26, 26.11, 26.18, 46000),
    ('2016-10-13', 23.52, 23.64, 23.18, 23.238, 32000),
    ('2016-10-14', 23.52, 23.64, 23.18, 23.12, 33000), ]

data = [
    ('2017-05-30', 112.800003, 113.660004, 112.260002, 113.160004, 2560300),
    ('2017-05-31', 113.400002, 113.919998, 111.5, 111.769997, 3222600),
    ('2017-06-01', 111.720001, 113.120003, 110.940002, 113.029999, 2322600),
    ('2017-06-02', 113.779999, 113.879997, 111.760002, 112.910004, 2215100),
    ('2017-06-05', 112.739998, 113.139999, 110.230003, 110.879997, 4008000),
    ('2017-06-06', 110.400002, 112.269997, 110.190002, 111.449997, 2444800),
    ('2017-06-07', 111.379997, 112.080002, 110.599998, 111.169998, 2030100),
    ('2017-06-08', 111.510002, 111.949997, 110.199997, 111.120003, 2025100),
    ('2017-06-09', 111.160004, 111.699997, 103.620003, 105.949997, 3025600),
    ('2017-06-12', 104.209999, 108.620003, 100.699997, 107.440002, 5134000),
    ('2017-06-13', 107.599998, 108.239998, 105.169998, 107.550003, 2269800),
    ('2017-06-14', 108.519997, 108.650002, 105.019997, 106.199997, 1974800),
    ('2017-06-15', 104.769997, 106.040001, 103.480003, 105.580002, 1824800),
    ('2017-06-16', 105.5, 105.919998, 103.629997, 104.879997, 2565400),
    ('2017-06-19', 105.599998, 106.699997, 105.160004, 106.160004, 2481500),
    ('2017-06-20', 106.010002, 107.110001, 104.300003, 104.93, 1956000),
    ('2017-06-21', 105.879997, 106.559998, 104.82, 105.690002, 2645600),
    ('2017-06-22', 105.720001, 107.260002, 104.550003, 106.779999, 2327900),
    ('2017-06-23', 106.400002, 108.760002, 105.300003, 107.75, 3666200),
    ('2017-06-26', 107.760002, 109.07, 105.309998, 106.120003, 1873400),
    ('2017-06-27', 105.580002, 106.449997, 102.5, 102.919998, 2269700),
    ('2017-06-28', 103.690002, 104.860001, 101.540001, 104.279999, 1642400),
    ('2017-06-29', 103.57, 103.809998, 100.0, 101.389999, 2347000),
    ('2017-06-30', 102.32, 102.370003, 100.75, 100.82, 1671300),
    ('2017-07-03', 101.32, 101.82, 99.32, 99.360001, 1454200),
    ('2017-07-05', 99.370003, 103.040001, 99.220001, 102.599998, 2785200),
    ('2017-07-06', 101.589996, 103.110001, 100.790001, 102.050003, 2605700),
    ('2017-07-07', 102.290001, 104.279999, 102.290001, 103.32, 1695300),
    ('2017-07-10', 103.330002, 104.190002, 102.379997, 103.739998, 1191800),
    ('2017-07-11', 103.470001, 104.730003, 102.980003, 104.300003, 1461700),
    ('2017-07-12', 105.610001, 107.080002, 104.760002, 106.68, 2621600),
    ('2017-07-13', 107.489998, 108.5, 106.379997, 107.07, 1428000),
    ('2017-07-14', 107.459999, 108.910004, 107.010002, 108.739998, 1480600),
    ('2017-07-17', 108.900002, 109.0, 106.559998, 106.940002, 1180700),
    ('2017-07-18', 106.669998, 107.849998, 106.230003, 107.699997, 865700),
    ('2017-07-19', 108.5, 110.5, 108.470001, 110.25, 2044400),
    ('2017-07-20', 109.720001, 110.5, 108.879997, 109.910004, 1270900),
    ('2017-07-21', 109.410004, 110.540001, 109.080002, 109.75, 1116400),
    ('2017-07-24', 109.589996, 110.889999, 109.339996, 110.809998, 1953400),
    ('2017-07-25', 110.910004, 112.400002, 110.199997, 112.260002, 1342500),
    ('2017-07-26', 112.5, 114.099998, 112.410004, 114.080002, 1891200),
    ('2017-07-27', 114.970001, 115.25, 109.32, 111.519997, 2362400),
    ('2017-07-28', 110.599998, 112.279999, 110.330002, 111.5, 946200),
    ('2017-07-31', 111.650002, 112.32, 109.779999, 110.790001, 1393800),
    ('2017-08-01', 111.269997, 112.589996, 111.099998, 111.379997, 1315600),
    ('2017-08-02', 111.080002, 111.379997, 107.279999, 109.129997, 1757100),
    ('2017-08-03', 107.949997, 108.5, 105.599998, 107.879997, 2255600),
    ('2017-08-04', 108.349998, 109.040001, 107.559998, 108.389999, 1490900),
    ('2017-08-07', 108.669998, 111.0, 108.400002, 109.82, 1493100),
    ('2017-08-08', 109.379997, 110.269997, 108.0, 108.349998, 1224200),
    ('2017-08-09', 107.690002, 107.959999, 106.540001, 107.449997, 1151400),
    ('2017-08-10', 106.559998, 107.540001, 104.769997, 104.980003, 1878300),
    ('2017-08-11', 105.75, 108.760002, 105.099998, 108.010002, 1461200),
    ('2017-08-14', 109.199997, 110.0, 108.010002, 108.900002, 1637900),
    ('2017-08-15', 109.019997, 110.099998, 108.120003, 109.800003, 1263300),
    ('2017-08-16', 110.360001, 110.93, 109.360001, 110.489998, 1320500),
    ('2017-08-17', 110.07, 110.82, 107.730003, 107.889999, 1738700),
    ('2017-08-18', 107.860001, 110.099998, 107.190002, 108.559998, 1164300),
    ('2017-08-21', 108.370003, 110.300003, 108.370003, 109.75, 1279200),
    ('2017-08-22', 110.309998, 112.239998, 109.769997, 111.010002, 1708500),
    ('2017-08-23', 110.910004, 111.339996, 110.050003, 110.650002, 1636200),
    ('2017-08-24', 110.580002, 111.25, 109.040001, 110.610001, 3128400),
    ('2017-08-25', 115.0, 119.730003, 113.540001, 114.970001, 7121000),
    ('2017-08-28', 115.059998, 115.139999, 110.010002, 111.480003, 3618400),
    ('2017-08-29', 109.650002, 111.900002, 109.25, 111.269997, 1858600),
    ('2017-08-30', 111.269997, 113.669998, 110.610001, 113.290001, 1458900),
    ('2017-08-31', 113.629997, 114.699997, 112.82, 114.459999, 1467200),
    ('2017-09-01', 114.629997, 115.620003, 113.650002, 113.709999, 1566400),
    ('2017-09-05', 113.459999, 114.809998, 112.519997, 113.769997, 3092900),
    ('2017-09-06', 114.400002, 114.779999, 112.650002, 113.790001, 2339900),
    ('2017-09-07', 114.139999, 114.470001, 113.190002, 114.050003, 1731400),
    ('2017-09-08', 114.169998, 115.720001, 114.099998, 114.440002, 2656400),
    ('2017-09-11', 112.980003, 117.129997, 112.220001, 116.480003, 2294700),
    ('2017-09-12', 116.349998, 116.989998, 114.980003, 116.160004, 1607000),
    ('2017-09-13', 116.040001, 116.5, 115.25, 116.18, 1449900),
    ('2017-09-14', 115.620003, 116.139999, 114.5, 115.470001, 1649700),
    ('2017-09-15', 115.620003, 115.620003, 113.879997, 114.129997, 6232600),
    ('2017-09-18', 113.739998, 114.660004, 112.870003, 113.839996, 2030000),
    ('2017-09-19', 113.769997, 114.059998, 112.970001, 113.080002, 1954800),
    ('2017-09-20', 113.07, 113.339996, 111.349998, 112.730003, 1782700),
    ('2017-09-21', 112.82, 113.0, 111.370003, 112.290001, 1154500),
    ('2017-09-22', 111.68, 112.82, 111.639999, 111.779999, 1085000),
    ('2017-09-25', 111.669998, 111.830002, 108.650002, 109.82, 2026000),
    ('2017-09-26', 110.589996, 111.379997, 108.830002, 110.610001, 1590500),
    ('2017-09-27', 110.209999, 113.470001, 110.209999, 111.959999, 1731400),
    ('2017-09-28', 111.400002, 111.959999, 110.519997, 111.449997, 1358300),
    ('2017-09-29', 111.25, 112.760002, 111.0, 112.260002, 2033100),
    ('2017-10-02', 110.690002, 113.760002, 110.68, 112.470001, 1961300),
    ('2017-10-03', 112.389999, 113.730003, 111.669998, 113.629997, 1044800),
    ('2017-10-04', 113.790001, 114.07, 112.349998, 114.050003, 1122300),
    ('2017-10-05', 114.5, 116.830002, 113.900002, 116.540001, 1673800),
    ('2017-10-06', 116.18, 117.610001, 115.809998, 116.959999, 1806200),
    ('2017-10-09', 116.800003, 117.519997, 116.639999, 117.139999, 847100),
    ('2017-10-10', 117.220001, 117.529999, 116.32, 117.050003, 931500),
    ('2017-10-11', 117.019997, 118.660004, 116.93, 118.57, 1078400),
    ('2017-10-12', 118.550003, 119.839996, 118.510002, 118.989998, 1236600),
    ('2017-10-13', 119.769997, 119.769997, 118.449997, 119.629997, 1262900),
    ('2017-10-16', 119.690002, 119.970001, 118.669998, 119.199997, 1179600),
    ('2017-10-17', 119.349998, 119.760002, 118.059998, 118.720001, 1184700),
    ('2017-10-18', 118.5, 118.860001, 117.779999, 118.540001, 1010600),
    ('2017-10-19', 119.0, 119.32, 117.57, 119.290001, 1099300),
    ('2017-10-20', 119.980003, 121.879997, 119.699997, 120.809998, 1647600),
    ('2017-10-23', 120.989998, 121.720001, 118.730003, 118.989998, 1487500),
    ('2017-10-24', 118.959999, 119.610001, 117.900002, 119.290001, 1337800),
    ('2017-10-25', 119.0, 120.25, 118.050003, 119.940002, 1080000),
    ('2017-10-26', 120.209999, 121.949997, 119.459999, 121.349998, 902700),
    ('2017-10-27', 121.610001, 123.970001, 121.400002, 123.580002, 1523700),
    ('2017-10-30', 123.040001, 124.279999, 121.900002, 123.910004, 1610500),
    ('2017-10-31', 124.279999, 125.010002, 123.419998, 124.959999, 1839900),
    ('2017-11-01', 125.629997, 126.440002, 123.400002, 124.779999, 1622800),
    ('2017-11-02', 125.5, 125.650002, 123.510002, 124.720001, 1736000),
    ('2017-11-03', 124.5, 125.5, 124.110001, 124.849998, 1309700),
    ('2017-11-06', 125.0, 125.089996, 123.190002, 123.82, 1003200),
    ('2017-11-07', 124.260002, 124.540001, 122.610001, 123.400002, 828400),
    ('2017-11-08', 123.489998, 124.209999, 123.169998, 123.839996, 892500),
    ('2017-11-09', 122.900002, 123.089996, 120.010002, 122.400002, 1465500),
    ('2017-11-10', 121.949997, 123.32, 121.309998, 123.110001, 929400),
    ('2017-11-13', 124.339996, 125.019997, 122.690002, 124.639999, 1216700),
    ('2017-11-14', 124.400002, 124.82, 123.160004, 123.870003, 1225300),
    ('2017-11-15', 123.870003, 125.010002, 122.440002, 124.019997, 1442100),
    ('2017-11-16', 124.790001, 127.0, 124.639999, 127.0, 1545200),
    ('2017-11-17', 127.489998, 127.919998, 125.870003, 127.489998, 1460900),
    ('2017-11-20', 127.510002, 128.279999, 126.110001, 126.279999, 1786200),
    ('2017-11-21', 127.129997, 128.169998, 126.970001, 127.709999, 1642900),
    ('2017-11-22', 128.009995, 128.690002, 126.839996, 127.769997, 1469500),
    ('2017-11-24', 127.739998, 129.539993, 127.650002, 129.5, 1013600),
    ('2017-11-27', 130.190002, 130.919998, 129.259995, 130.240005, 2337200),
    ('2017-11-28', 130.759995, 131.100006, 127.489998, 129.949997, 4976600),
    ('2017-11-29', 114.029999, 114.459999, 106.199997, 109.339996, 19487000),
    ('2017-11-30', 109.639999, 111.580002, 106.540001, 109.699997, 8481000),
    ('2017-12-01', 108.809998, 110.120003, 106.290001, 107.059998, 4922900),
    ('2017-12-04', 108.0, 108.690002, 105.160004, 107.949997, 3986000),
    ('2017-12-05', 107.910004, 109.489998, 106.550003, 106.589996, 3002500),
    ('2017-12-06', 105.730003, 107.830002, 105.730003, 106.919998, 1686600),
    ('2017-12-07', 106.199997, 110.18, 106.0, 109.610001, 3074200),
    ('2017-12-08', 109.599998, 110.169998, 106.690002, 107.160004, 3124700),
    ('2017-12-11', 106.870003, 107.949997, 106.150002, 106.830002, 2412300),
    ('2017-12-12', 106.32, 107.980003, 105.580002, 106.330002, 2026100),
    ('2017-12-13', 107.029999, 107.889999, 105.510002, 106.019997, 1982900),
    ('2017-12-14', 105.949997, 107.120003, 105.949997, 106.25, 1503900),
    ('2017-12-15', 106.550003, 108.93, 106.470001, 108.400002, 2704200),
    ('2017-12-18', 108.660004, 109.43, 107.279999, 107.480003, 2362600),
    ('2017-12-19', 107.239998, 107.839996, 105.370003, 105.389999, 1862000),
    ('2017-12-20', 106.019997, 106.019997, 104.190002, 105.029999, 2513900),
    ('2017-12-21', 105.580002, 105.669998, 103.650002, 104.43, 3920700),
    ('2017-12-22', 104.849998, 104.849998, 103.779999, 103.889999, 1533800),
    ('2017-12-26', 103.449997, 104.150002, 103.190002, 103.800003, 1322200),
    ('2017-12-27', 103.970001, 105.199997, 103.480003, 104.580002, 1111800),
    ('2017-12-28', 104.660004, 105.220001, 104.199997, 105.07, 870900),
    ('2017-12-29', 105.040001, 105.650002, 104.529999, 104.830002, 1068400),
    ('2018-01-02', 105.339996, 107.160004, 104.389999, 107.120003, 2040600),
    ('2018-01-03', 107.0, 109.779999, 106.989998, 109.379997, 1953800),
    ('2018-01-04', 110.129997, 112.209999, 109.230003, 112.07, 2158700),
    ('2018-01-05', 113.07, 113.349998, 110.410004, 110.839996, 2384200),
    ('2018-01-08', 110.419998, 111.739998, 109.040001, 111.419998, 1782100),
    ('2018-01-09', 111.57, 112.309998, 110.650002, 112.110001, 1848900),
    ('2018-01-10', 111.709999, 112.610001, 110.550003, 111.470001, 1645000),
    ('2018-01-11', 111.669998, 113.959999, 111.470001, 113.260002, 2716000),
    ('2018-01-12', 113.57, 116.089996, 113.07, 115.910004, 2553000),
    ('2018-01-16', 116.239998, 117.080002, 111.720001, 111.980003, 2699000),
    ('2018-01-17', 112.879997, 113.099998, 111.059998, 113.0, 2932200),
    ('2018-01-18', 112.279999, 114.150002, 112.050003, 112.550003, 1625200),
    ('2018-01-19', 112.959999, 115.910004, 112.370003, 115.290001, 2804200),
    ('2018-01-22', 115.25, 118.449997, 114.029999, 117.43, 2905900),
    ('2018-01-23', 117.139999, 119.07, 116.5, 118.730003, 1985400),
    ('2018-01-24', 118.910004, 119.239998, 116.639999, 116.900002, 2221700),
    ('2018-01-25', 117.949997, 118.419998, 116.57, 116.870003, 1690400),
    ('2018-01-26', 117.550003, 118.849998, 117.120003, 117.779999, 1836300),
    ('2018-01-29', 117.699997, 118.470001, 116.190002, 116.379997, 1058800),
    ('2018-01-30', 115.459999, 116.349998, 113.769997, 115.019997, 1556400),
    ('2018-01-31', 115.650002, 116.639999, 114.900002, 115.620003, 1119800),
    ('2018-02-01', 114.720001, 117.699997, 114.080002, 115.57, 1596400),
    ('2018-02-02', 114.120003, 115.139999, 111.599998, 111.639999, 1808300),
    ('2018-02-05', 110.599998, 116.150002, 109.18, 109.18, 2890800),
    ('2018-02-06', 106.489998, 112.650002, 104.610001, 112.620003, 3144800),
    ('2018-02-07', 111.769997, 113.559998, 110.510002, 110.540001, 1599700),
    ('2018-02-08', 109.169998, 110.800003, 104.809998, 104.809998, 3056500),
    ('2018-02-09', 105.809998, 107.919998, 101.550003, 105.940002, 3923900),
    ('2018-02-12', 107.010002, 109.209999, 104.739998, 108.379997, 1994100),
    ('2018-02-13', 106.5, 110.199997, 106.230003, 109.790001, 1339000),
    ('2018-02-14', 108.360001, 110.339996, 107.410004, 109.919998, 1923900),
    ('2018-02-15', 111.160004, 114.709999, 110.010002, 113.519997, 2555000),
    ('2018-02-16', 113.580002, 114.529999, 112.099998, 112.949997, 1584200),
    ('2018-02-20', 112.510002, 115.059998, 112.0, 114.269997, 1354300),
    ('2018-02-21', 114.18, 115.720001, 112.32, 112.370003, 2045100),
    ('2018-02-22', 112.739998, 114.760002, 111.900002, 112.389999, 1817200),
    ('2018-02-23', 113.669998, 115.040001, 112.379997, 115.029999, 1818700),
    ('2018-02-26', 115.629997, 117.5, 114.730003, 116.919998, 2335200),
    ('2018-02-27', 117.0, 117.57, 115.139999, 116.120003, 1658000),
    ('2018-02-28', 117.019997, 119.739998, 116.650002, 117.470001, 2825400),
    ('2018-03-01', 117.949997, 118.980003, 114.010002, 114.739998, 2959600),
    ('2018-03-02', 113.300003, 116.43, 111.050003, 116.279999, 2681700),
    ('2018-03-05', 115.18, 119.300003, 115.050003, 118.870003, 2502600),
    ('2018-03-06', 119.25, 120.639999, 118.25, 119.870003, 4723900),
    ('2018-03-07', 133.009995, 137.899994, 130.059998, 137.699997, 12753500),
    ('2018-03-08', 137.009995, 137.690002, 133.940002, 137.289993, 5255200),
    ('2018-03-09', 138.440002, 140.0, 137.350006, 139.360001, 3752100),
    ('2018-03-12', 139.210007, 141.190002, 138.339996, 138.369995, 2109300),
    ('2018-03-13', 139.740005, 141.259995, 135.070007, 136.0, 2309000),
    ('2018-03-14', 136.850006, 137.610001, 135.050003, 136.190002, 1596400),
    ('2018-03-15', 136.690002, 137.919998, 135.429993, 136.720001, 1319200),
    ('2018-03-16', 136.330002, 139.009995, 135.440002, 135.75, 2438200),
    ('2018-03-19', 133.940002, 135.460007, 132.059998, 134.309998, 2047300),
    ('2018-03-20', 134.5, 136.289993, 133.889999, 134.600006, 1760600),
    ('2018-03-21', 135.009995, 137.600006, 133.869995, 135.539993, 2191000),
    ('2018-03-22', 133.820007, 135.929993, 131.149994, 131.410004, 2596500),
    ('2018-03-23', 131.75, 132.5, 128.0, 128.020004, 2763400),
    ('2018-03-26', 131.050003, 134.589996, 130.059998, 134.220001, 2290000),
    ('2018-03-27', 134.529999, 134.589996, 127.190002, 128.309998, 3043600),
    ('2018-03-28', 127.709999, 129.389999, 124.379997, 124.550003, 3534500),
    ('2018-03-29', 125.199997, 128.309998, 123.870003, 125.580002, 4263800),
    ('2018-04-02', 124.559998, 125.800003, 120.800003, 122.75, 2683300),
    ('2018-04-03', 124.18, 126.440002, 122.209999, 124.839996, 2292300),
    ('2018-04-04', 121.720001, 128.050003, 121.360001, 127.5, 2573800),
    ('2018-04-05', 128.679993, 129.139999, 126.980003, 128.020004, 2082200),
    ('2018-04-06', 126.690002, 127.959999, 124.959999, 125.75, 2527800),
    ('2018-04-09', 126.720001, 129.139999, 126.389999, 127.57, 1893000),
    ('2018-04-10', 129.25, 132.369995, 128.190002, 131.729996, 2156900),
    ('2018-04-11', 130.5, 132.660004, 130.070007, 130.940002, 1379900),
    ('2018-04-12', 131.539993, 133.039993, 131.119995, 132.169998, 1700300),
    ('2018-04-13', 133.550003, 133.550003, 127.980003, 129.169998, 2023400),
    ('2018-04-16', 130.490005, 131.149994, 128.770004, 129.720001, 1707600),
    ('2018-04-17', 131.210007, 133.639999, 130.940002, 132.580002, 2100600),
    ('2018-04-18', 133.190002, 134.729996, 132.080002, 133.869995, 1321600),
    ('2018-04-19', 133.490005, 134.029999, 131.490005, 132.330002, 1250800),
    ('2018-04-20', 132.470001, 132.470001, 128.960007, 130.089996, 1678500),
    ('2018-04-23', 130.639999, 132.039993, 128.289993, 129.179993, 1370000),
    ('2018-04-24', 130.639999, 131.279999, 122.050003, 123.68, 2513400),
    ('2018-04-25', 123.720001, 124.650002, 120.910004, 123.970001, 1978300),
    ('2018-04-26', 124.620003, 127.550003, 123.970001, 126.980003, 1912800),
    ('2018-04-27', 127.160004, 127.830002, 125.779999, 126.639999, 1175600),
    ('2018-04-30', 127.32, 128.089996, 125.809998, 125.900002, 1448500),
    ('2018-05-01', 125.300003, 127.370003, 125.290001, 127.059998, 1163000),
    ('2018-05-02', 126.82, 127.209999, 124.989998, 125.260002, 1483200),
    ('2018-05-03', 124.760002, 128.350006, 123.879997, 127.599998, 1531800),
    ('2018-05-04', 126.489998, 130.679993, 125.589996, 129.460007, 1632500),
    ('2018-05-07', 129.759995, 132.119995, 129.630005, 131.570007, 1333400),
    ('2018-05-08', 131.570007, 133.160004, 130.710007, 132.759995, 1152300),
    ('2018-05-09', 133.070007, 136.369995, 133.070007, 135.320007, 1678400),
    ('2018-05-10', 135.960007, 137.669998, 134.899994, 136.470001, 1374600),
    ('2018-05-11', 136.559998, 136.940002, 135.330002, 136.210007, 1477300),
    ('2018-05-14', 136.990005, 138.380005, 133.330002, 134.110001, 1698100),
    ('2018-05-15', 133.160004, 137.449997, 131.589996, 136.160004, 2089000),
    ('2018-05-16', 136.470001, 136.729996, 134.889999, 135.929993, 1465200),
    ('2018-05-17', 135.410004, 136.830002, 134.580002, 136.520004, 1404500),
    ('2018-05-18', 136.619995, 139.669998, 136.25, 138.850006, 1723600),
    ('2018-05-21', 139.610001, 139.940002, 136.929993, 137.669998, 2474800),
    ('2018-05-22', 138.509995, 139.169998, 136.460007, 136.710007, 1740500),
    ('2018-05-23', 135.309998, 139.5, 135.020004, 139.309998, 1929600),
    ('2018-05-24', 139.059998, 139.630005, 136.119995, 138.919998, 4021000),
    ('2018-05-25', 132.710007, 139.690002, 131.149994, 132.75, 6463800)]

df = DataFrame.from_records(data, columns=labels)

# Pass it to the backtrader datafeed and add it to the cerebro
data = bt.feeds.PandasData(
    dataname=df,
    datetime=0,
    open=1,
    high=2,
    low=3,
    close=4,
    volume=5,
    openinterest=-1
)

# Add the Data Feed to Cerebro
cerebro.adddata(data)

# Set our desired cash start
cerebro.broker.setcash(1000.0)

# Add a FixedSize sizer according to the stake
cerebro.addsizer(bt.sizers.FixedSize, stake=10)

# Set the commission
cerebro.broker.setcommission(commission=0.001)

# Print out the starting conditions
print('Starting Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Run over everything
cerebro.run()

# Print out the final result
print('Final Portfolio Value: %.2f' % cerebro.broker.getvalue())

# Plot the result
cerebro.plot()
