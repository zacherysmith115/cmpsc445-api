import pandas as pd
from controllers import Database
from dtos import DataResponse
from dtos import DataAvailableResponse
from dtos import TimeSeries
from typing import Union


from dtos.data_dto import DataAvailableResponse

db = Database()

class DataService(object):
    
    def read_data(self, symbol: str) -> Union[DataResponse, None]:
        if symbol not in db.keys:
            return None
        
        conn = db.engine.connect()
        df = pd.read_sql_table(symbol, conn)

        historic_time_series = TimeSeries(dates = df["date"].to_list(), values=df["close"].to_list())
        # TODO: Need to feed data into model to get prediction response

        dto = DataResponse(symbol, historic_time_series, None)
        
        return dto

    def read_available_data(self) -> DataAvailableResponse:

        dto = DataAvailableResponse(tickers=db.keys)

        return dto