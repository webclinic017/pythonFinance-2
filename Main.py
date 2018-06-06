import os
from datetime import datetime
from DataReading.NewsStockDataReaders.DataReaderFactory import DataReaderFactory
from Strategies.StrategyFactory import StrategyFactory
from Utils.file_utils import FileUtils, read_tickers_from_file
from Utils.news_utils import NewsUtils


def run_screening(strat_selection, strategy_parameter_dict, other_params):
    thr_start = datetime.now()

    # TODO 10: only temp:
    reload = False
    stock_data_container_list = read_tickers_from_file(other_params['stock_data_container_file'], reload)
    # TODO abstract factory: http://python-3-patterns-idioms-test.readthedocs.io/en/latest/Factory.html
    # TODO eventuell als return statt als call by reference: stock_data_container_list = data_storage.read_data("HistoricalDataReader", stock_data_container_list, weeks_delta, global_filepath + 'stock_dfs')
    # TODO releod data
    data_storage = DataReaderFactory()
    stock_data_reader = data_storage.prepare("HistoricalDataReader", stock_data_container_list, other_params['weeks_delta'],
                                             other_params['stock_data_container_file'], other_params['data_source'],
                                             reload_stockdata=reload)
    stock_data_reader.read_data()

    ##################################################
    # 52 w strategy

    if strat_selection == "W52HighTechnicalStrategy":
        stock_screener = StrategyFactory()
        w52_hi_strat = stock_screener.prepare_strategy("W52HighTechnicalStrategy", stock_data_container_list,
                                                       strategy_parameter_dict)
        results = w52_hi_strat.run_strategy()

        print("")
        print("-----------------------------------")
        for data in results:
            print("buy: " + data.stock_name + ", " + data.stock_ticker)

    ##################################################
    # News strategy + 52 w auf results
    elif strat_selection =="SimplePatternNewsStrategy":

        # TODO auch hier parallel
        news_data_storage = DataReaderFactory()
        news_stock_data_reader = news_data_storage.prepare("TraderfoxNewsDataReader", stock_data_container_list,
                                                           other_params['weeks_delta'], other_params['stock_data_container_file'], other_params['data_source'],
                                                           reload_stockdata=reload)
        all_news_text_list = news_stock_data_reader.read_data(other_params['last_date_time_file'])

        stock_screener = StrategyFactory()
        news_strategy = stock_screener.prepare_strategy("SimplePatternNewsStrategy", stock_data_container_list,
                                                        strategy_parameter_dict)
        results = news_strategy.run_strategy(all_news_text_list)

        # TODO 10:
        import os
        os.remove("C:\\temp\\pythonFinance\\pythonFinance\\DataFiles\\last_date_time.csv")

        # todo 10 des stimmt garned zaum zwischen current price und was er wirklich is
        # for data in results:
        #     if len(data.historical_stock_data) > 0:
        #         data.set_stock_current_prize(data.historical_stock_data.High[len(results) - 1])
        #     else:
        #         print("ERROR: failed load hist data for " + data.stock_name)

        # 52 w strat------------------------------------------------------
        # TODO 10: warum nur mit results --> weil mehr nichts bringt bei verknüpfung
        # TODO 10: eig nur de positiven nehmen???
        if 0:
            stock_data_reader = data_storage.prepare("HistoricalDataReader", results, other_params['weeks_delta'],
                                                     other_params['stock_data_container_file'], other_params['data_source'],
                                                     reload_stockdata=reload)
            stock_data_reader.read_data()

            w52_hi_strat = stock_screener.prepare_strategy("W52HighTechnicalStrategy", results, strategy_parameter_dict)
            results = w52_hi_strat.run_strategy()

        # print result -------------------------
        res_str = NewsUtils.format_news_analysis_results(results)

        if res_str is not None and len(res_str) > 0:
            print()
            print('------------------------')
            print(res_str)
            # FileUtils.append_to_file(res_str, global_filepath + "Backtesting.txt")  # TODO da ghert a aktuelle abfrage fuer preis
            # TODO CommonUtils.send_stock_email(res_str, "News Trading: New news available")
        else:
            print("News analysis: no news")

        # time.sleep(60)  # check for new news after x seconds
    print("Runtime check um " + str(datetime.now()) + " und dauer: " + str(datetime.now() - thr_start))

    # TODO 10: dazu
    # result = calculate_stopbuy_and_stoploss(stock_data_container)

    return results


if __name__ == '__main__':
    thr_start = datetime.now()
    ROOT_DIR = os.path.dirname(os.path.abspath(__file__))
    # TODO ev in config file -->  gui load
    filepath = ROOT_DIR + '\\DataFiles\\'
    #data_source = 'iex'
    #weeks_delta = 52  # one year in the past
    selection = "SimplePatternNewsStrategy"
    news_parameter_dict = {'news_threshold': 0.7, 'german_tagger': filepath + 'nltk_german_classifier_data.pickle'}
    w52hi_parameter_dict = {'check_days': 7, 'min_cnt': 3, 'min_vol_dev_fact': 1.2, 'within52w_high_fact': 0.98}

    # TODO des geht nima
    run_screening(selection, news_parameter_dict)
