from dtos import DataResponse
from dtos import DataAvailableResponse
from services import DataService

class DataView(object):
    """
    View class to control the routing of end points, and return of the
    appropiate responses. All database interaction should be handled 
    through the services class. Each public function should have a 
    corresponding end point spcecified in swagger.yaml file. 
    """
    
    def __init__(self) -> None:
        self.service = DataService()

    def root(self):
        """ / """
        return "CMPSC 445 API is up and running!"

    def read_data(self, symbol: str):
        """ /data/{symbol} """

        dto = self.service.read_data(symbol)

        if dto:
            return dto, 200
        else:
            return None, 404

    def read_available_data(self):
        """ /data/avaiable """

        dto = self.service.read_available_data()

        return dto