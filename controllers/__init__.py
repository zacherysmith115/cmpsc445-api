import connexion
import threading
from flask_cors import CORS
from connexion.resolver import MethodViewResolver
from connexion import FlaskApp
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import Table

class Application(object):
    __app: FlaskApp = None
    __app_lock = threading.Lock()

    def __new__(cls):
        """
        Singleton Design Pattern for global scoping 
        """

        if Application.__app is None:
            with Application.__app_lock:
                Application.__app = connexion.App(__name__, specification_dir='./')
                CORS(Application.__app.app)
                Application.__app.add_api('../swagger.yaml', resolver=MethodViewResolver('controllers'))

        return Application.__app


class Database(object):

    def __init__(self) -> None:
        self.engine = create_engine('sqlite:///../cmpsc445-model/data/test.db')
        self.metadata = MetaData(self.engine)
        self.metadata.reflect(self.engine)

    def __new__(cls):
        """
        Singleton Design Pattern for global scoping 
        """

        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)

        return cls.instance

