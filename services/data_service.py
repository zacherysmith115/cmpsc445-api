from controllers import Database
from dtos import DataResponse
from dtos import TimeSeriesDatum
from datetime import date

db = Database()

class DataService(object):
    
    def read_data(self, symbol: str) -> DataResponse:

        ts1 = TimeSeriesDatum(date(2022, 4, 7), 1.0)
        ts2 = TimeSeriesDatum(date(2022, 4, 8), 1.1)
        ts3 = TimeSeriesDatum(date(2022, 4, 9), 1.2)
        dto = DataResponse(symbol, [ts1, ts2], [ts3])


        return dto