class MvcModel:
    def __init__(self, view_controller):
        """
        Init the mvc model with given controller
        :param view_controller: controller
        """
        self.vc = view_controller
        self.available_strategies = []
        self._other_params = {}
        self.strategy_parameter_dicts = {}
        self.strategy_selection_value = []
        self.result_stock_data_container_list = []
        self.is_thread_running = False
        self._column_list = []

    def get_column_list(self):
        return self._column_list

    def update_column_list(self, columns_to_add):
        """
        Adds columns to the column list, if not already there, does not add redundant entries.
        :param columns_to_add: list with columns to add
        :return: Returns True, if list is updated / a new entry is appended
        """
        is_updated = False
        for col in columns_to_add:
            if col not in self._column_list:
                self._column_list.append(col)
                self._column_list = list(dict.fromkeys(self._column_list))
                is_updated = True

        return is_updated

    def get_is_thread_running(self):
        return self.is_thread_running

    def set_is_thread_running(self, is_thread_running):
        self.is_thread_running = is_thread_running
        self.vc.is_thread_running_changed()

    def get_result_stock_data_container_list(self):
        return self.result_stock_data_container_list

    def clear_result_stock_data_container_list(self):
        self.result_stock_data_container_list = []
        self.vc.result_stock_data_container_list_changed()

    def extend_result_stock_data_container_list(self, stock_data_container_list):
        self.result_stock_data_container_list.extend(stock_data_container_list)
        self.vc.result_stock_data_container_list_changed()

    def set_strategy_selection_value(self, value):
        self.strategy_selection_value = value

    def get_strategy_selection_value(self):
        return self.strategy_selection_value


    # Delegates-- Model would call this on internal change
    def other_params_changed(self):
        self.vc.other_params_changed()

    def get_other_params(self):
        return self._other_params

    def add_to_other_params(self, items):
        assert (isinstance(items, dict))
        for key, value in items.items():
            self._other_params.update({key: value})
        self.other_params_changed()

    def clear_other_params(self):
        self._other_params = {}
        self.other_params_changed()


    # Delegates-- Model would call this on internal change
    def list_changed(self):
        self.vc.available_strategies_changed()

    # setters and getters
    def getList(self):
        return self.available_strategies

    def add_to_available_strategies(self, item):
        myList = self.available_strategies
        myList.append(item)
        self.available_strategies = myList
        self.list_changed()

    def clear_available_strategies_list(self):
        self.available_strategies = []
        self.list_changed()
