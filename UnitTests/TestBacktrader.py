import unittest

import backtrader as bt
import backtrader.analyzers as btanalyzer
import pandas as pd
from datetime import datetime
from pandas import DataFrame
from backtrader.feeds import GenericCSVData

from Backtesting.Backtrader.BacktraderWrapper import BacktraderWrapper
# from directory UnitTests to --> root folder with: ..\\..\\
from DataContainerAndDecorator.StockDataContainer import StockDataContainer
from Strategies.StrategyFactory import StrategyFactory
from Utils.GlobalVariables import *

test_filepath = GlobalVariables.get_data_files_path() + 'TestData\\'


class TestBacktrader(unittest.TestCase):

    def test_backtrader_52whi_(self):
        tbt = BacktraderWrapper()
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict(False).items():
            labels.append(value)

        data_in_1 = [
            ('2016-09-30', 46.35, 46.91, 46.24, 46.8, 33900),
            ('2016-10-03', 46.68, 46.69, 46.39, 46.5, 31600),
            ('2016-10-04', 46.52, 46.64, 46.39, 46.28, 31700),
            ('2016-10-05', 46.28, 46.51, 46.27, 46.43, 31500),
            ('2016-10-06', 46.38, 46.56, 46.29, 46.48, 42000),
            ('2016-10-07', 46.58, 46.65, 46.37, 46.48, 43000),
            ('2016-10-10', 46.62, 46.88, 46.55, 46.77, 44000),
            ('2016-10-11', 46.62, 46.74, 46.01, 46.16, 45000),
            ('2016-10-12', 26.16, 27, 26.11, 26, 46000),
            ('2016-10-13', 46.52, 46.64, 46.39, 46.468, 32000),
            ('2016-10-14', 46.52, 46.64, 46.39, 46.0, 33000),
            ('2016-10-15', 39.7, 20, 17, 39.5, 33000),
            ('2016-10-16', 39, 19, 16, 15, 33000)
        ]

        data_in_2 = [
            ('2016-09-30', 23.35, 23.91, 23.24, 23.8, 31800),
            ('2016-10-03', 23.68, 23.69, 23.39, 23.5, 31600),
            ('2016-10-04', 23.52, 23.64, 23.18, 23.28, 31700),
            ('2016-10-05', 23.28, 23.51, 23.27, 23.43, 31500),
            ('2016-10-06', 23.38, 23.56, 23.29, 23.48, 42000),
            ('2016-10-07', 23.58, 23.65, 23.37, 23.48, 43000),
            ('2016-10-10', 23.62, 23.88, 23.55, 23.77, 44000),
            ('2016-10-11', 23.62, 23.74, 23.01, 23.16, 45000),
            ('2016-10-12', 26.16, 27, 26.11, 26, 46000),
            ('2016-10-13', 23.52, 23.64, 23.18, 23.238, 32000),
            ('2016-10-14', 23.52, 23.64, 23.18, 23.0, 33000),
            ('2016-10-15', 18.7, 20, 17, 18.5, 33000),
            ('2016-10-16', 18, 19, 16, 15, 33000)]

        df_1 = pd.DataFrame.from_records(data_in_1, columns=labels)
        df_2 = pd.DataFrame.from_records(data_in_2, columns=labels)

        data_list = []
        dfs = [df_1, df_2]

        for i in range(0, len(dfs)):
            df_in = dfs[i]
            data_pd = bt.feeds.PandasData(
                dataname=df_in,
                name="Data Frame " + str(i + 1),
                datetime=0,
                open=1, high=2, low=3,
                close=4, volume=5,
                openinterest=-1
            )
            data_list.append(data_pd)

        analyzers = [btanalyzer.AnnualReturn, btanalyzer.Calmar, btanalyzer.DrawDown, btanalyzer.TimeDrawDown,
                     btanalyzer.GrossLeverage, btanalyzer.PositionsValue, btanalyzer.Returns,
                     btanalyzer.SharpeRatio, btanalyzer.TradeAnalyzer]
        strategy_to_test = "W52HighTechnicalStrategy"
        backtesting_parameters = {'BacktestingFramework': 'BacktraderWrapper', 'initial_cash': 30000,
                                  'trade_commission_percent': 0.005}
        analysis_parameters = {'check_days': 5, 'min_cnt': 3, 'min_vol_dev_fact': 1.2,
                               'within52w_high_fact': 0.99}

        risk_model = {'FixedSizeRiskModel': {'OrderTarget': 'order_target_value', 'TargetValue': 2500}}

        backtesting_result_instance, res = tbt.run_test(data_list, strategy_to_test, backtesting_parameters,
                                                        analysis_parameters,
                                                        risk_model, analyzers)
        # TODO backtesting_result_instance.plot(style='candlestick', barup='green', bardown='red')
        portvalue = round(backtesting_result_instance.broker.getvalue(), 2)
        pnl = round(portvalue - backtesting_parameters['initial_cash'], 2)

        self.assertNotEqual(None, backtesting_result_instance)
        self.assertNotEqual(backtesting_parameters['initial_cash'], pnl)

    def test_BacktraderWrapper_run_test(self):
        tbt = BacktraderWrapper()
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict(True).items():
            labels.append(value)

        data_in_2 = [
            ('2016-09-30', 23.35, 23.91, 23.24, 23.8, 31800),
            ('2016-10-03', 23.68, 23.69, 23.39, 23.5, 31600),
            ('2016-10-04', 23.52, 23.64, 23.18, 23.28, 31700),
            ('2016-10-05', 23.28, 23.51, 23.27, 23.43, 31500),
            ('2016-10-06', 23.38, 23.56, 23.29, 23.48, 42000),
            ('2016-10-07', 23.58, 23.65, 23.37, 23.48, 43000),
            ('2016-10-10', 23.62, 23.88, 23.55, 23.77, 44000),  # --> buy
            ('2016-10-11', 23.62, 23.74, 23.41, 23.41, 45000),
            ('2016-10-12', 26.16, 27, 26.0, 26, 46000),
            ('2016-10-13', 23.52, 23.64, 23.18, 23.238, 32000),  # --> sell
            ('2016-10-14', 23.52, 23.64, 23.18, 23.2, 33000),
            ('2016-10-15', 18.7, 20, 17, 18.7, 33000),
            ('2016-10-16', 18, 19, 16, 15, 33000)]
        df_2 = pd.DataFrame.from_records(data_in_2, columns=labels)

        data_list = []
        dfs = [df_2]

        for i in range(0, len(dfs)):
            df_in = dfs[i]
            data_pd = bt.feeds.PandasData(
                dataname=df_in,
                name="Data Frame " + str(i + 1),
                datetime=0,
                open=1, high=2, low=3,
                close=4, volume=5,
                openinterest=-1
            )
            data_list.append(data_pd)

        analyzers = [btanalyzer.AnnualReturn, btanalyzer.Calmar, btanalyzer.DrawDown, btanalyzer.TimeDrawDown,
                     btanalyzer.GrossLeverage, btanalyzer.PositionsValue, btanalyzer.Returns,
                     btanalyzer.SharpeRatio, btanalyzer.TradeAnalyzer]
        strategy_to_test = "W52HighTechnicalStrategy"
        backtesting_parameters = {'BacktestingFramework': 'BacktraderWrapper', 'initial_cash': 30000,
                                  'trade_commission_percent': 0}
        analysis_parameters = {'check_days': 5, 'min_cnt': 3, 'min_vol_dev_fact': 1.2,
                               'within52w_high_fact': 0.99}

        risk_model = {'FixedSizeRiskModel': {'OrderTarget': 'order_target_size', 'TargetValue': 100}}

        backtesting_result_instance, res = tbt.run_test(data_list, strategy_to_test, backtesting_parameters,
                                                        analysis_parameters,
                                                        risk_model, analyzers)

        portvalue = round(backtesting_result_instance.broker.getvalue(), 2)
        pnl = round(portvalue - backtesting_parameters['initial_cash'], 2)

        self.assertNotEqual(None, backtesting_result_instance)
        self.assertNotEqual(backtesting_parameters['initial_cash'], pnl)
        self.assertEqual(29969.0, portvalue)
        self.assertEqual(-31, pnl)

    def test_run_test2(self):
        tbt = BacktraderWrapper()
        data_list = []
        datafile_path = GlobalVariables.get_data_files_path() + "TestData\\TestBacktraderRun_test2.csv"

        data = bt.feeds.GenericCSVData(
            dataname=datafile_path,
            nullvalue=0.0,
            dtformat=GlobalVariables.get_stock_data_dtformat(),
            datetime=0,
            open=1, high=2, low=3,
            close=4, volume=5,
            openinterest=-1
        )
        data_list.append(data)
        analyzers = [btanalyzer.AnnualReturn, btanalyzer.Calmar, btanalyzer.DrawDown, btanalyzer.TimeDrawDown,
                     btanalyzer.GrossLeverage, btanalyzer.PositionsValue, btanalyzer.Returns,
                     btanalyzer.SharpeRatio, btanalyzer.TradeAnalyzer]
        strategy_to_test = "W52HighTechnicalStrategy"
        backtesting_parameters = {'BacktestingFramework': 'BacktraderWrapper', 'initial_cash': 30000,
                                  'trade_commission_percent': 0}
        analysis_parameters = {'check_days': 5, 'min_cnt': 3, 'min_vol_dev_fact': 1.2,
                               'within52w_high_fact': 0.99}

        risk_model = {'FixedSizeRiskModel': {'OrderTarget': 'order_target_size', 'TargetValue': 100}}

        backtesting_result_instance, res = tbt.run_test(data_list, strategy_to_test, backtesting_parameters,
                                                        analysis_parameters,
                                                        risk_model, analyzers)

        portvalue = round(backtesting_result_instance.broker.getvalue(), 2)
        pnl = round(portvalue - backtesting_parameters['initial_cash'], 2)

        self.assertNotEqual(None, backtesting_result_instance)
        self.assertEqual(29969.0, portvalue)
        self.assertEqual(-31, pnl)

    def test_GenericBacktraderCsvNewsData(self):
        tbt = BacktraderWrapper()
        data_file_path = GlobalVariables.get_data_files_path()
        data_list = [data_file_path + '\\TestData\\TestBacktraderRun_test2.csv']
        analyzers = [btanalyzer.AnnualReturn, btanalyzer.Calmar, btanalyzer.DrawDown, btanalyzer.TimeDrawDown,
                     btanalyzer.GrossLeverage, btanalyzer.PositionsValue, btanalyzer.Returns,
                     btanalyzer.SharpeRatio, btanalyzer.TradeAnalyzer]

        analysis_parameters = {'news_threshold': 0.7,
                               'german_tagger': data_file_path + 'nltk_german_classifier_data.pickle'}

        strategy_to_test = "SimplePatternNewsStrategy"
        backtesting_parameters = {'BacktestingFramework': 'BacktraderWrapper', 'initial_cash': 30000,
                                  'trade_commission_percent': 0.005}

        risk_model = {'FixedSizeRiskModel': {'OrderTarget': 'order_target_value', 'TargetValue': 2500}}
        backtesting_result_instance, backtest_result = tbt.run_test(data_list, strategy_to_test, backtesting_parameters,
                                                                    analysis_parameters,
                                                                    risk_model, analyzers)

        portvalue = round(backtesting_result_instance.broker.getvalue(), 2)
        pnl = round(portvalue - backtesting_parameters['initial_cash'], 2)

        self.assertNotEqual(None, backtesting_result_instance)
        self.assertNotEqual(backtesting_parameters['initial_cash'], pnl)

    def test_BacktraderStrategyWrapper(self):
        labels = []
        for key, value in GlobalVariables.get_stock_data_labels_dict().items():
            labels.append(value)
        data = [('2016-09-30', 23.35, 23.91, 23.24, 23.8, 31000),
                ('2016-10-03', 23.68, 23.69, 23.39, 23.5, 31000),
                ('2016-10-04', 23.52, 23.64, 23.18, 23.28, 31000),
                ('2016-10-05', 23.28, 23.51, 23.27, 23.43, 31000),
                ('2016-10-06', 23.38, 23.56, 23.29, 23.48, 42000),
                ('2016-10-07', 23.58, 23.65, 23.37, 23.48, 43000),
                ('2016-10-10', 23.62, 23.88, 23.55, 23.77, 44000),
                ('2016-10-11', 23.62, 23.74, 23.01, 23.16, 45000),
                ('2016-10-12', 23.16, 26, 23.11, 23.18, 46000)]

        analysis_parameters = {
            'sma_timeperiod': int(5),
            'ema_timeperiod': int(5),
            'roc_timeperiod': int(5)
        }

        data0 = bt.feeds.YahooFinanceData(dataname='AAPL',
                                          fromdate=datetime(2017, 1, 1),
                                          todate=datetime(2017, 12, 31))

        backtesting_parameters = {'BacktestingFramework': 'BacktraderWrapper', 'initial_cash': 50000,
                                  'trade_commission_percent': 0.001}
        risk_model = {'FixedSizeRiskModel': {'OrderTarget': 'order_target_value', 'TargetValue': 5000}}
        tbt = BacktraderWrapper()

        backtesting_result_instance, res = tbt.run_test([data0], "StrategyAsta_SMA_and__EMA_or_RoC",
                                                        backtesting_parameters,
                                                        analysis_parameters,
                                                        risk_model, [])

        self.assertNotEqual(None, backtesting_result_instance)
        # TODO wert anpassen
        self.assertEqual(29969.0, backtesting_result_instance.broker.getvalue())

