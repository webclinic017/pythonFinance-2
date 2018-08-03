from abc import abstractmethod


class Abstract_StrategyFactory:
    def prepare_strategy(self, strategy_to_create, stock_data_container_list, parameter_dict):
        strategy = self._create_strategy(strategy_to_create, stock_data_container_list, parameter_dict)
        return strategy

    @abstractmethod
    def _create_strategy(self, strategy_to_create, stock_data_container_list, parameter_list):
        raise Exception("Abstractmethod")
