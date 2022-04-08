from dataclasses import dataclass
from datetime import date
from typing import List

@dataclass
class TimeSeriesDatum:
    date: date
    close: float

@dataclass
class DataResponse:
    symbol: str
    historic_timeseries: List[TimeSeriesDatum]
    prediction_timeseries: List[TimeSeriesDatum]