from dtos import DataResponse
from services import DataService

class DataView(object):

    def __init__(self, service=DataService()) -> None:
        self.service = service

    def root(self):
        """ / """
        return "CMPSC 445 API is up and running!"

    def read_data(self, symbol: str):
        """ /data/{symbol} """

        dto: DataResponse = self.service.read_data(symbol)

        return dto