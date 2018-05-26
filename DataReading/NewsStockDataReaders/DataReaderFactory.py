from DataReading.DataStorage import DataStorage
from DataReading.HistoricalDataReaders.HistoricalDataReader import HistoricalDataReader
from DataReading.NewsStockDataReaders.TraderfoxNewsDataReader import TraderfoxNewsDataReader


# todo umstellen auf abstract factory
# https://sourcemaking.com/design_patterns/factory_method
class DataReaderFactory(DataStorage):

    def _create_data_storage(self, storage_to_create):
        if storage_to_create in "TraderfoxNewsDataReader":
            storage = TraderfoxNewsDataReader()

        elif storage_to_create in "HistoricalDataReader":
            storage = HistoricalDataReader()
        else:
            raise NotImplementedError

        return storage
