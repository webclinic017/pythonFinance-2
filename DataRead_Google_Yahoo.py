import datetime as dt
import os
import sys
import threading
import traceback

import urllib3
from pandas import DataFrame
from pandas_datareader import data, data
from yahoo_finance import Share
import googlefinance.client as google_client
import xlrd
import pandas as pd
import pandas_datareader.data as web

from Utils.Utils import get_current_function_name, split_list

str1 = "http://d.yimg.com/autoc.finance.yahoo.com/autoc?query="
str2 = "&region=1&lang="
str3 = "&callback=YAHOO.Finance.SymbolSuggest.ssCallback"

stocks = []
names = []


def read_data_from_google_with_client(stock_name, interval="86400", period="1M"):
    if stock_name is None:
        raise NotImplementedError

    param = {
        'q': stock_name,  # Stock symbol (ex: "AAPL")
        'i': interval,  # Interval size in seconds ("86400" = 1 day intervals)
        # 'x': "INDEXDJX", # Stock exchange symbol on which stock is traded (ex: "NASD")
        'p': period  # Period (Ex: "1Y" = 1 year)
    }
    # get price data (return pandas dataframe)
    df = google_client.get_price_data(param)
    return df


def read_data_from_google_with_pandas(stock_name, start_date, end_date, read_yahoo_today=False):
    """
    read data from google server
    :param read_yahoo_today:
    :param stock_name: stock name
    :param start_date: start date and time
    :param end_date: end date and time
    :return: stock data
    """

    if stock_name is None or start_date is None or end_date is None:
        raise NotImplementedError

    try:
        stock52_w = data.DataReader(stock_name, "google", start_date.strftime("%Y-%m-%d"),
                                    end_date.strftime("%Y-%m-%d"))

    except:
        # Try with another stock market ETR
        stock52_w = data.DataReader("ETR:" + stock_name, "google", start_date.strftime("%Y-%m-%d"),
                                    end_date.strftime("%Y-%m-%d"))

        # TODO data of today contains less volume because not finished
        if read_yahoo_today:
            if len(stock52_w) > 0:
                try:
                    stock52_w = stock52_w.append(read_current_day_from_yahoo(stock_name))
                except Exception as e:
                    sys.stderr.write("Can not get stock data of stock " + stock_name + " from yahoo\n")

        if len(stock52_w) == 0:
            sys.stderr.write("Stock: " + stock_name + " does not exist on!\n")

    return stock52_w


def read_data_from_yahoo(stock_name, start_date, end_date):
    if stock_name is None or start_date is None or end_date is None:
        raise NotImplementedError

    # see also:
    #  https: // github.com / lukaszbanasiak / yahoo - finance
    #  https://pypi.python.org/pypi/yahoo-finance

    # yahoo = Share('APPL')
    # print(yahoo.get_avg_daily_volume())
    # print(yahoo.get_open())
    # print (yahoo.get_historical('2014-04-25', '2014-04-29'))


    from pandas_datareader import data as pdr
    import fix_yahoo_finance as yf
    yf.pdr_override()  # <== that's all it takes :-)
    data = pdr.get_data_yahoo(stock_name, start=start_date, end=end_date)

    return data


def read_current_day_from_yahoo(stock_name):
    if stock_name is None:
        raise NotImplementedError

    # TODO google does not provide data from today, workarround: add yahoo data manually:
    #  maybe try this: https://pypi.python.org/pypi/googlefinance.client
    stock_name = optimize_name_for_yahoo(stock_name)
    cols = ['Date', 'Open', 'High', 'Low', 'Close', 'Volume']
    lst = []
    stock_markets_to_try = ["", ".DE", ".VI"]
    for stock_market in stock_markets_to_try:

        try:
            yahoo = Share(stock_name + stock_market)
            currDate = (yahoo.get_trade_datetime())[0:10]
            lst.append([currDate, float(yahoo.get_price()), float(yahoo.get_days_high()), float(yahoo.get_days_low()),
                        float(yahoo.get_price()),
                        float(yahoo.get_volume())])
            break

        except:
            # nothing to do
            no = []

    df1 = DataFrame(lst, columns=cols)
    df1.index.name = 'Date'
    # df1.set_index([str(currDate)])
    df1 = df1.set_index(['Date'])
    return df1

    # stock52_w.loc[len(stock52_w)]=[yahoo.get_price(),yahoo.get_days_high(),yahoo.get_days_low(),yahoo.get_price(),yahoo.get_volume()]
    # stock52_w.iloc[len(stock52_w) - 1].name = datetime.utcnow()
    # print("name: " + str(stock52_w.index.name))

    return []


def __get_symbol_from_name_from_yahoo(name, stock_exchange):
    """
    TODO
    name: name to convert
    """
    if name is None or stock_exchange is None:
        raise NotImplementedError

    names_to_get = []
    names_to_get.append(optimize_name_for_yahoo(name))
    names_to_get.append(optimize_name_for_yahoo(name, False))
    names_to_get.append(optimize_name_for_yahoo(name, False, True))

    for name in names_to_get:

        try:

            http = urllib3.PoolManager()
            # query: http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=Priceline&region=1&lang=en&callback=YAHOO.Finance.SymbolSuggest.ssCallback"

            try:
                #ex: 'http://d.yimg.com/autoc.finance.yahoo.com/autoc?query=BMW+AG&region=1&lang=de&callback=YAHOO.Finance.SymbolSuggest.ssCallback'
                req = str1 + name + str2 + stock_exchange + str3
                r = http.request('GET', req)  # build url
            except Exception as e:
                #TODO return " "
                sys.stderr.write("no symbol found for " + name + ", str_res: " + str_res + "\n")

            str_res = str(r.data)
            if len(str_res) > 0 and "symbol" in str_res:
                symbol = str_res.rsplit('{"symbol":"')[1].rsplit('"')[0]
                if "." in symbol:
                    symbol = symbol.rsplit('.')[0]  # cut the stock exchange market from yahoo
                return symbol
            #else:
             #   sys.stderr.write("no symbol found for " + name + ", str_res: " + str_res + "\n")
                #return " "  # no symbol found

        except Exception as e:
            sys.stderr.write("Exception: no symbol found for " + name + ", str_res: " + str_res + str(e) + "\n")
            #return " "  # no symbol found

    sys.stderr.write("no symbol found for " + name + ", str_res: " + str_res + "\n")
    return " "

def get52_w__h__symbols__from_excel(file_stock_list, file_excel):
    if file_stock_list is None or file_excel is None:
        raise NotImplementedError

    f = open(file_stock_list, 'w')
    f.write("Name,   Symbol \n")  # python will convert \n to os.linesep

    sh = xlrd.open_workbook(file_excel).sheet_by_index(0)

    from MyThread import MyThread
    get_symbol_threads = MyThread("get_symbol_threads")

    for rownum in range(sh.nrows):
        try:
            if rownum != 0:
                name = str(sh.cell(rownum, 0).value)
                date_from_file = str(sh.cell(rownum, 1).value)

                # values from today contain a time (=Uhr) and not a date
                # TODO google data is from yesterday
                if not "Uhr" in date_from_file:  # but google data is from yesterday
                    get_symbol_threads.append_thread(threading.Thread(target=symbol_thread, kwargs={'name': name}))

        except Exception as e:
            sys.stderr.write("Method exception in: " + get_current_function_name()
                             + ": stock name: " + str(name) + " is faulty: " + str(e) + "\n")
            traceback.print_exc()

    get_symbol_threads.execute_threads()

    cnt = 0
    while (cnt < len(names)):
        for symbol in stocks:
            f.write(names[cnt] + ",  " + symbol + "\n")  # python will convert \n to os.linesep
            cnt += 1

    f.close()  # you can omit in most cases as the destructor will call it
    return stocks


def __get_symbols_from_names(symbol_names, stock_exchanges, num_of_stocks_per_thread=20):
    """
    TODO
    :param stock_exchanges:
    :param num_of_stocks_per_thread:
    :param symbol_names:
    :return:
    """

    if symbol_names is None:
        raise NotImplementedError

    from MyThread import MyThread
    get_symbol_threads = MyThread("get_symbol_threads")
    splits = split_list(symbol_names, num_of_stocks_per_thread)

    for split_names in splits:
        try:
            get_symbol_threads.append_thread(threading.Thread(target=symbol_thread, kwargs={'st_names': split_names,
                                                                                            'stock_exchanges': stock_exchanges}))

        except Exception as e:
            sys.stderr.write("Method exception in: " + get_current_function_name()
                             + ": stock name: " + str(split_names) + " is faulty: " + str(e) + "\n")
            traceback.print_exc()

    get_symbol_threads.execute_threads()

    return stocks, names


def optimize_name_for_yahoo(name, replace_whitespace=True, return_first_part=False):
    if name is None:
        raise NotImplementedError

    name = name.upper()
    if replace_whitespace:
        name = name.replace(" ", "+")
    name = name.replace(".", "")
    name = name.replace("\n", "")
    name = name.replace("Ü", "UE")
    name = name.replace("Ö", "OE")
    name = name.replace("Ä", "AE")

    if "ETR:" in name:
        name = name.replace("ETR:", "")
        name += ".DE"
    name = name.replace("FRA:", "")
    name = name.split("INC")[0]
    name = name.replace("^", "")
    if replace_whitespace:
        name_spl = name.split("+")
    else:
        name_spl = name.split(" ")

    if len(name_spl) > 2:
        name = name_spl[0] + "+" + name_spl[1]

    if return_first_part:
        name = name_spl[0]
    return name


def symbol_thread(st_names, stock_exchanges):
    if st_names is None or stock_exchanges is None:
        raise NotImplementedError

    i = 0
    while i < len(st_names):
        try:
            symbol = __get_symbol_from_name_from_yahoo(st_names[i], stock_exchanges[i])
            if symbol != " ":
                stocks.append(symbol)
                st_names.append(st_names[i])
        except Exception as e:
            sys.stderr.write(
                "EXCEPTION " + get_current_function_name() + ": " + str(st_names[i]) + ", "+ (str(e)) + "\n")
        i += 1


def get_ticker_data_with_webreader(ticker, stock_dfs_file, source='yahoo', reload_sp500=False, reload_stockdata=False):
    # if reload_sp500:
    #     read_and_save_sp500_tickers(tickers_file)
    # else:
    #     with open(tickers_file, "rb") as f:
    #         tickers = pickle.load(f)

    # if not os.path.exists(stock_dfs_file):
    #     os.makedirs(stock_dfs_file)

    df = []
    ticker = optimize_name_for_yahoo(ticker)

    retry = 3

    while retry > 0:
        try:
            # TODO does not reload new data
            if not os.path.exists(stock_dfs_file + '/{}.csv'.format(ticker)) or reload_stockdata:
                end = dt.datetime.now()
                start = (end - dt.timedelta(weeks=52))
                df = web.DataReader(ticker, source, start, end)
                if len(df) > 0:
                    df.to_csv(stock_dfs_file + '/{}.csv'.format(ticker))
                else:
                    print('FAILED: Reading {}'.format(ticker))
                    raise Exception
            else:
                # print('Already have {}'.format(ticker))
                df = pd.read_csv(stock_dfs_file + '/{}.csv'.format(ticker))

            break

        except Exception as e:
            sys.stderr.write(
                "EXCEPTION reading " + get_current_function_name() + ": " + str(ticker) + ", retry: " + str(
                    retry) + ", " + str(e) + "\n")
            # traceback.print_exc()
            # append_to_file(str(ticker), filepath + "failedReads.txt")
            if retry <= 0:
                break
            retry -= 1

    return df
