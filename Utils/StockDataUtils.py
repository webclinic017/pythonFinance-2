import traceback

import numpy
import numpy as np
import pandas as pd
from scipy.stats import norm

from DataContainerAndDecorator.NewsDataContainerDecorator import NewsDataContainerDecorator
from DataContainerAndDecorator.StockDataContainer import StockDataContainer
from Utils.CommonUtils import is_next_day_or_later
from Utils.GlobalVariables import GlobalVariables
from time import sleep
from datetime import datetime

def calc_avg_vol(stock_data):
    """
    Calculates the average volume of stock data except the days to skip from end.
    :param stock_data: stock data
    :return: Average Value
    """

    if stock_data is None or len(stock_data) <= 0:
        raise NotImplementedError

    vol_avg = stock_data[GlobalVariables.get_stock_data_labels_dict()["Volume"]].mean()
    return vol_avg


def calculate_stopbuy_and_stoploss(stock_data, stop_buy_limit_percent=1.005, stop_loss_limit_percent=0.97):
    """
    calculates stop buy and stop loss values
    :param stop_loss_limit_percent: stop loss 3% lower than stop buy
    :param stop_buy_limit_percent: stop buy 0,5% higher than last val
    :param stock_data: 52w stock data
    :return: stop buy and stop loss: {'sb':sb, 'sl': sl}
    """

    if stock_data is None:
        raise NotImplementedError

    if len(stock_data) <= 0:
        return 0, 0

    # sl sb from last high value
    data_len = len(stock_data[GlobalVariables.get_stock_data_labels_dict()['High']])
    calc_val = stock_data[GlobalVariables.get_stock_data_labels_dict()['High']][data_len - 1]
    sb = calc_val * stop_buy_limit_percent  # stop buy 0,5% higher than last val
    sl = sb * stop_loss_limit_percent  # stop loss 3% lower than stop buy

    return sl, sb


def calc_true_range(tday_high_value, tday_low_value, yesterday_close_value):
    """
    # max of todays high - low, abs(high - yday close), abs (low - yday Close)
    :param tday_high_value:
    :param tday_low_value:
    :param yesterday_close_value:
    :return:
    """

    today_high_low = tday_high_value - tday_low_value
    high_yday_close = abs(tday_high_value - yesterday_close_value)
    low_yday_close = abs(tday_low_value - yesterday_close_value)

    true_range = max(today_high_low, high_yday_close, low_yday_close)

    return true_range


def calc_mean_true_range(stock_data):
    """
    TODO replace with atr?
    :param stock_data:
    :return:
    """
    tr = []
    i = 0
    while i < len(stock_data):
        yesterday_close_value = stock_data.iloc[i - 1][GlobalVariables.get_stock_data_labels_dict()['Close']]
        tday_high_value = stock_data.iloc[i][GlobalVariables.get_stock_data_labels_dict()['High']]
        tday_low_value = stock_data.iloc[i][GlobalVariables.get_stock_data_labels_dict()['Low']]
        tr.append(calc_true_range(tday_high_value, tday_low_value, yesterday_close_value))

        i += 1

    return numpy.mean(tr)


def convert_backtrader_to_dataframe(data):
    """
    Convert the backtrader data to the dataframe data.
    :param data: backtrader data
    :return: pandas data frame
    """
    cols = []
    for key, value in GlobalVariables.get_stock_data_labels_dict().items():
        cols.append(value)
    lst = []

    # the data starts at [0] with the current value
    # and goes negative for older values
    i = - len(data.open) + 1
    while i <= 0:
        try:
            lst.append([
                "-",
                float(data.open[i]),
                float(data.high[i]),
                float(data.low[i]),
                float(data.close[i]),
                float(data.volume[i])])
        except Exception as e:
            # nothing to do
            break
        i += 1

    df1 = pd.DataFrame(lst, columns=cols)

    return df1


def convert_backtrader_to_asta_data(hist_data, news_data_dict, date_time, stock_data_container_list):
    """
    Converts the backtrader nect-data into asta stock data container format
    :param hist_data: historical dat in backtrader format
    :param news_data_dict: dict with all news data
    :param date_time: current date to look up in news
    :param stock_data_container_list: list to insert result
    :return: - return as ref of the data list
    """
    stock_name = hist_data._name
    dataname = hist_data._dataname
    curr_news = ""
    # add the news text because backtrader does not support news
    # data from pandas do not have a name --> not add news
    if isinstance(dataname, str):
        if dataname in news_data_dict:
            news_data = news_data_dict[dataname]
            if hasattr(news_data, "NewsText") and hasattr(news_data, "Date"):
                for currEntry in range(0, len(news_data.Date)):
                    if str(date_time) in news_data.Date[currEntry]:
                        try:
                            curr_news = str(news_data.NewsText[currEntry])
                        except Exception as e:
                            pass
                        break

    # convert backtrader format to asta-format
    df1 = convert_backtrader_to_dataframe(hist_data)
    # ticker not implemented, but not needed
    stock_data_container = StockDataContainer(stock_name, "", "")
    stock_data_container.set_historical_stock_data(df1)
    news_dec = NewsDataContainerDecorator(stock_data_container, 0, 0, curr_news)
    stock_data_container_list.append(news_dec)


def value_at_risk(df_close, portfolio_value, conv=0.99):
    per_change = df_close.pct_change()
    mu = np.mean(per_change)
    sigma = np.std(per_change)

    var = var_cov_var(portfolio_value, conv, mu, sigma)
    return var


def var_cov_var(P, c, mu, sigma):
    """
    Variance-Covariance calculation of daily Value-at-Risk
    using confidence level c, with mean of returns mu
    and standard deviation of returns sigma, on a portfolio
    of value P.
    """
    alpha = norm.ppf(1 - c, mu, sigma)
    return P - P * (alpha + 1)


def are_order_information_available(action, stock_data_container):
    """
    Check required order data due to action
    :param action: BUY / SELL
    :param stock_data_container: stock data container
    :return: False, if data not available
    """
    if action is "BUY":
        if stock_data_container.get_stop_buy() is None:
            return False

        if stock_data_container.get_stop_buy() is 0:
            return False

    elif action is "SELL":
        if stock_data_container.get_stop_loss() is None:
            return False

        if stock_data_container.get_stop_loss() is 0:
            return False

    if stock_data_container.get_position_size() is None:
        return False

    if stock_data_container.get_position_size() <= 0:
        return False

    return True


def buy_recommendations(broker, stocks, max_num_of_different_stocks_to_buy):
    """
    Automatically buy the recommendations from result list
    :return: -
    """
    from Utils.Logger_Instance import logger

    broker.connect()

    if len(stocks) <= 0:
        return

    try:
        # sort stocks by rank
        sorted_stock_container_list = sorted(stocks, key=lambda x: x.get_rank(), reverse=True)

        for i in range(len(sorted_stock_container_list)):
            if max_num_of_different_stocks_to_buy <= 0:  # do not buy more stocks
                logger.info("Max number of stocks to buy reached.")
                return

            # check if there are enough data to create stop buy and stop loss limit orders
            if not are_order_information_available("BUY", sorted_stock_container_list[i]) or \
                    not are_order_information_available("SELL", sorted_stock_container_list[i]):
                logger.info(
                    "Not enough information for order available: " + str(sorted_stock_container_list[i]))
                break

            # trade only, if not already traded today
            orders = broker.read_orders()
            date_time_str = None
            # find the last entry
            for curr_order_num in range(len(orders)):
                if orders['stock_ticker'][curr_order_num].startswith(
                        sorted_stock_container_list[i].stock_ticker()):
                    date_time_str = (orders['datetime'][curr_order_num])

            if date_time_str is not None:
                next_day_or_later = is_next_day_or_later(str(datetime.now()), "%Y-%m-%d %H:%M:%S.%f",
                                                         date_time_str,
                                                         "%Y-%m-%d %H:%M:%S.%f")
                # do not trade same recommendation again on one day
                if not next_day_or_later:
                    logger.info("No current recommendations to buy available for " +
                                str(sorted_stock_container_list[i]))
                    break

            # get stock quantity, only even number
            qty = int(sorted_stock_container_list[i].get_position_size())
            # rank < 0 means sell recommendation, > 0 a buy
            if sorted_stock_container_list[i].get_rank() > 0:
                # stop buy limit order
                broker.execute_order(sorted_stock_container_list[i].stock_ticker(),
                                     'LMT', 'BUY', qty,
                                     sorted_stock_container_list[i].get_stop_buy())
                # stop loss limit order
                broker.execute_order(sorted_stock_container_list[i].stock_ticker(),
                                     'LMT', 'SELL', qty,
                                     sorted_stock_container_list[i].get_stop_loss())

                max_num_of_different_stocks_to_buy = max_num_of_different_stocks_to_buy - 1

            # get the response
            # TODO without sleep
            sleep(0.5)
            error_message_list = broker.get_and_clear_error_message_list()

            if len(error_message_list) > 0:
                for error_msg in error_message_list:
                    logger.error(
                        "Unexpected response from broker while autotrading: " + str(
                            error_msg))
                    # TODO what to do in case of an error?

    except Exception as e:
        err_msg = "Unexpected Exception while autotrading: " + str(e) + "\n" + str(traceback.format_exc())
        logger.error(err_msg)
        print(err_msg)

    broker.disconnect()
