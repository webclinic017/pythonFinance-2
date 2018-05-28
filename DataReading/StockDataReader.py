from abc import ABC, abstractmethod
import _pickle as pickle
from Utils.common_utils import CommonUtils


class StockDataReader(ABC):

    def __init__(self, stock_data_container_list, weeks_delta, stock_data_container_file, data_source, reload_stockdata):
        self.stock_data_container_list = stock_data_container_list
        self.reload_stockdata = reload_stockdata
        self.data_source = data_source
        self.stock_data_container_file = stock_data_container_file
        self.weeks_delta = weeks_delta

    @abstractmethod
    def _method_to_execute(self, stock_data_container):
        raise Exception("Abstractmethod")

    def read_data(self):
        pool = CommonUtils.get_threading_pool()
        pool.map(self._method_to_execute, self.stock_data_container_list)

        with open(self.stock_data_container_file, "wb") as f:
            pickle.dump(self.stock_data_container_list, f)
