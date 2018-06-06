import os
from abc import abstractmethod

class StockScreener():
    def prepare_strategy(self, strategy_to_create, stock_data_container_list, parameter_list):
        strategy = self._create_strategy(strategy_to_create, stock_data_container_list, parameter_list)
        return strategy

    @abstractmethod
    def _create_strategy(self, strategy_to_create):
        raise Exception("Abstractmethod")


