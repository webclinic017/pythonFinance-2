import datetime
import traceback
from datetime import datetime

import bs4 as bs
import pandas as pd
import requests

from DataReading.Abstract_StockDataReader import Abstract_StockDataReader
from DataContainerAndDecorator.NewsDataContainerDecorator import NewsDataContainerDecorator
from DataContainerAndDecorator.StockDataContainer import StockDataContainer
from Utils.FileUtils import is_date_actual
from Utils.GlobalVariables import *
from Utils.Logger_Instance import logger
from NewsTrading.GermanTaggerAnalyseNews import GermanTaggerAnalyseNews


class TraderfoxNewsDataReader(Abstract_StockDataReader):

    def __init__(self, stock_data_container_list, reload_stockdata, parameter_dict):
        super().__init__(stock_data_container_list, reload_stockdata, parameter_dict)
        self.text_analysis = None

    def read_data(self):
        from Utils.FileUtils import FileUtils
        if self.reload_stockdata:
            FileUtils.check_file_exists_and_delete(self._parameter_dict['last_check_date_file'])

        # self._read_news_from_traderfox(self._parameter_dict['last_check_date_file'])
        # TODO enable for enhanced info
        # url = "https://traderfox.de/nachrichten/dpa-afx-compact/kategorie-2-5-8-12/"  # analysen, ad hoc, unternehmen, pflichtmitteilungen
        start_time = datetime.now()

        self.text_analysis = GermanTaggerAnalyseNews(self.stock_data_container_list, None,
                                                     self._parameter_dict['german_tagger'])

        # ex: #news = "27.02. 10:41 dpa-AFX: ANALYSE-FLASH: Bryan Garnier hebt Morphosys auf 'Buy' - Ziel 91 Euro"
        all_news = []
        all_articles = self._read_news_from_traderfox(self._parameter_dict['last_check_date_file'])

        # all_news.extend(self.map_list(all_articles))
        self.map_list(all_articles)

        print("Time diff map_list:" + (str(datetime.now() - start_time)))

        # TODO returnen
        # return all_news

    def _method_to_execute(self, elm):
        """
        read news from traderfox home page with dpa-afx-compact news
        :param date_time_format: news datetime format
        :param date_file: file for last check date
        :param url: traderfox news page url
        :return: news as list
        """
        from Utils.FileUtils import FileUtils
        all_news = []

        date_time = (str(elm.footer.span.get_text()))  # date and Time
        date_time = date_time.rsplit(' Uhr')[0]  # TODO: split because of datetime format

        article_text = (str(elm.h2.get_text(strip=True)))  # h2 --> article head line
        news_text = date_time.replace(',', '.') + ", " + article_text.replace(',', '.')
        # TODO REMOVE THAT
        # THIS IS JUST FOR BACKTESTING NEWS DATA COLLECTION
        FileUtils.append_textline_to_file(news_text,
                                          GlobalVariables.get_data_files_path() + "NewsForBacktesting.txt",
                                          True)
        all_news.append(news_text)

        prep_news = self.text_analysis.optimize_text_for_german_tagger(news_text)
        name_ticker_exchange_target_prize = \
            self.text_analysis.identify_stock_name_and_stock_ticker_and_target_price_from_news_nltk_german_classifier(
                news_text)

        if name_ticker_exchange_target_prize is not None and name_ticker_exchange_target_prize.get_stock_name() != "":
            container = StockDataContainer(name_ticker_exchange_target_prize.get_stock_name(),
                                           name_ticker_exchange_target_prize.stock_ticker(),
                                           name_ticker_exchange_target_prize.stock_exchange())

            if container in self.stock_data_container_list:
                idx = self.stock_data_container_list.index(container)
                container_2 = self.stock_data_container_list[idx]
                if isinstance(container_2, StockDataContainer):
                    container = container_2
                    self.stock_data_container_list.remove(container_2)

            news_dec = NewsDataContainerDecorator(container,
                                                  name_ticker_exchange_target_prize.stock_target_price(),
                                                  0, prep_news)

            self.stock_data_container_list.append(news_dec)

        # return all_news

    def _read_news_from_traderfox(self, date_file, date_time_format="%d.%m.%Y um %H:%M",
                                  url="https://traderfox.de/nachrichten/dpa-afx-compact/kategorie-5/"):

        """
        read news from traderfox home page with dpa-afx-compact news
        :param date_time_format: news datetime format
        :param date_file: file for last check date
        :param url: traderfox news page url
        :return: news as list
        """
        from Utils.FileUtils import FileUtils

        # TODO enable for enhanced info
        # url = "https://traderfox.de/nachrichten/dpa-afx-compact/kategorie-2-5-8-12/"  # analysen, ad hoc, unternehmen, pflichtmitteilungen

        resp = requests.get(url)
        soup = bs.BeautifulSoup(resp.text, 'lxml')
        # article --> h2 --> a href for news text, article --> footer for date
        all_articles = soup.find_all("article")

        # ex: #news = "27.02. 10:41 dpa-AFX: ANALYSE-FLASH: Bryan Garnier hebt Morphosys auf 'Buy' - Ziel 91 Euro"
        news_to_evaluate = []
        last_date = ""
        for elm in reversed(all_articles):
            date_time = (str(elm.footer.span.get_text()))  # date and Time
            date_time = date_time.rsplit(' Uhr')[0]  # TODO: split because of datetime format
            datetime_object = datetime.strptime(date_time, date_time_format)
            is_a_new_news, last_date = is_date_actual(datetime_object, date_file, last_date)

            if is_a_new_news:
                news_to_evaluate.append(elm)

        return news_to_evaluate
