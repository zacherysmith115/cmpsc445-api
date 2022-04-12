from dataclasses import dataclass
from datetime import date
from typing import List

@dataclass
class TimeSeries:
    dates: List[date]
    values: List[float]

@dataclass
class DataResponse:
    symbol: str
    historic_timeseries: TimeSeries
    prediction_timeseries: TimeSeries

@dataclass
class DataAvailableResponse:
    tickers: List[str]