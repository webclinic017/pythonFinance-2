import pandas as pd
from pandas_datareader import data, wb
# import pandas.io.data as web  # Package and modules for importing data; this code may change depending on pandas version
from datetime import datetime, date, time
import plotly
import plotly.plotly as py
import plotly.graph_objs as go
from datetime import timedelta
import sys
import threading
import webbrowser

from MyThread import MyThread
from Utils import  is52_w_high, is_volume_high_enough, split_stock_list, get_symbol_from_name, \
    get52_w__h__symbols__from_excel, \
    write_stocks_to_buy_file, print_stocks_to_buy
from Strategies import strat_scheduler

import time
import logging

threads = []
stocks_to_buy = []
err = []
program_start_time = datetime.now()

##########################
# config
num_of_stocks_per_thread = 5
volume_day_delta = 5
volume_avg_day_delta = 15
end = datetime.now()
ago52_w = (end - timedelta(weeks=52))

data_provider = "google"
filepath = 'C:\\Users\\Tom\\OneDrive\\Dokumente\\Thomas\\Aktien\\'

# enhanced stock messages:
# logging.basicConfig(level=logging.DEBUG)

##########################

# symbols to read
nasdaq100__symbols = ["AAPL", "ADBE", "ADI", "ADP", "ADSK", "AKAM", "ALXN",
                     "AMAT", "AMGN", "AMZN", "ATVI", "AVGO", "BBBY", "BIDU", "BIIB",
                     "BRCM", "CA", "CELG", "CERN", "CHKP", "CHRW", "CHTR", "CMCSA",
                     "COST", "CSCO", "CTRX", "CTSH", "CTXS", "DISCA", "DISCK", "DISH",
                     "DLTR", "EBAY", "EQIX", "ESRX", "EXPD", "EXPE", "FAST",
                     "FB", "FFIV", "FISV", "FOXA", "GILD", "GMCR", "GOOG",
                     "GRMN", "HSIC", "ILMN", "INTC", "INTU", "ISRG", "KLAC", "KRFT",
                      "LBTYA", "LLTC", "LMCA", "LMCK", "LVNTA", "MAR", "MAT", "MDLZ",
                      "MNST", "MSFT", "MU", "MXIM", "MYL", "NFLX", "NTAP", "NVDA",
                      "NXPI", "ORLY", "PAYX", "PCAR", "PCLN", "QCOM", "QVCA", "REGN",
                      "ROST", "SBAC", "SBUX", "SIAL", "SIRI", "SNDK", "SPLS", "SRCL",
                      "STX", "SYMC", "TRIP", "TSCO", "TSLA", "TXN", "VIAB", "VIP",
                      "VOD", "VRSK", "VRTX", "WDC", "WFM", "WYNN", "XLNX", "YHOO", "NOC"]

dax_symbols = ["ETR:ADS", "ETR:ALV", "ETR:BAS", "ETR:BAY", "ETR:BMW", "ETR:CBK", "ETR:CON", "ETR:DAI",
               "ETR:DB1", "ETR:DBK", "ETR:DPB", "ETR:DPW", "ETR:DTE", "ETR:FME", "ETR:HEN3",
               "ETR:IFX", "ETR:LHA", "ETR:LIN", "ETR:MAN", "ETR:MEO", "ETR:MRK.DE", "ETR:MUV2",
               "ETR:RWE", "ETR:SAP", "ETR:SIE", "ETR:TKA", "ETR:TUI1", "ETR:VOW", "ETR:BAYN",
               "ETR:FNTN", "ETR:O2D", "ETR:QIA", "ETR:DRI", "ETR:AM3D", "ETR:O1BC", "ETR:GFT", "ETR:NDX1",
               "ETR:SBS", "ETR:COK", "ETR:DLG", "ETR:DRW3", "ETR:SMHN", "ETR:WDI", "ETR:BC8", "ETR:MOR",
               "ETR:SOW", "ETR:AIXA", "ETR:ADV", "ETR:PFV", "ETR:JEN", "ETR:AFX", "ETR:UTDI", "ETR:NEM", "ETR:SRT3",
               "ETR:EVT", "ETR:WAF", "ETR:RIB", "ETR:S92", "ETR:COP", "ETR:TTR1", "ETR:SZG", "ETR:VT9"]

all_symbols = []

###############################################################################################
# enter stock filter options
# 0 = alles (Dax + nasdaq + excel)
# 1 = VERSUCH DAX
# 2 = VERSUCH NASDAQ
# 3 = nur finanzen excel
# 4 = NORMAL nur DAX und NASDAQ
option = 4
###########################################################

# versuch DAX
if option == 1:
    dax_symbols = ["ETR:WAF"]
    all_symbols.extend(dax_symbols)

# versuch NASDAQ
if option == 2:
    nasdaq100__symbols = ["AAPL"]
    all_symbols.extend(nasdaq100__symbols)

# ----------------------------------------------
# alles Dax + nasdaq + excel
if option == 0:
    symbols52W_Hi = get52_w__h__symbols__from_excel()
    all_symbols.extend(symbols52W_Hi)
    all_symbols.extend(nasdaq100__symbols)
    all_symbols.extend(dax_symbols)

# nur finanzen excel
if option == 3:
    symbols52W_Hi = get52_w__h__symbols__from_excel()
    all_symbols.extend(symbols52W_Hi)

# NORMAL: nur DAX und NASDAQ
if option == 4:
    all_symbols.extend(nasdaq100__symbols)
    all_symbols.extend(dax_symbols)

# Create new threads
splits = split_stock_list(all_symbols, num_of_stocks_per_thread)
stock_screening_threads = MyThread("stock_screening_threads")


def function_for_threading_strat_scheduler(ch, provider, ago52_w_time, end_l):
    print("Started with: " + str(ch))
    stocks_to_buy.extend(strat_scheduler(ch, provider, ago52_w_time, end_l))


i = 0
while i < len(splits):
    ch = splits[i]
    stock_screening_threads.append_thread(
        threading.Thread(target=function_for_threading_strat_scheduler, kwargs={'ch': ch, 'provider': data_provider,
                                                                                'ago52_w_time': ago52_w, 'end_l': end}))
    i += 1

# Start new Threads to schedule all stocks
stock_screening_threads.execute_threads()

#print the results
print_stocks_to_buy (stocks_to_buy, num_of_stocks_per_thread, program_start_time, datetime.now())
