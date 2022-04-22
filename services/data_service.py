import pandas as pd
from controllers import Database
from controllers import Model
from dtos import DataResponse
from dtos import DataAvailableResponse
from dtos import TimeSeries
from typing import Union

db = Database()
model = Model()

class DataService(object):
    
    def read_data(self, symbol: str) -> Union[DataResponse, None]:
        if symbol not in db.keys:
            return None
        
        conn = db.engine.connect()
        df = pd.read_sql_table(symbol, conn, index_col='date', parse_dates=['date'])
        df = df.iloc[::-1]

        predicted_dates, predicted_values = model.predict(df)

        historic_time_series = TimeSeries(dates = df.index.to_list(), values=df["close"].to_list())
        forecasted_time_series = TimeSeries(predicted_dates, predicted_values)

        dto = DataResponse(symbol, historic_time_series, forecasted_time_series)
        
        return dto

    def read_available_data(self) -> DataAvailableResponse:

        dto = DataAvailableResponse(tickers=db.keys)

        return dto

    