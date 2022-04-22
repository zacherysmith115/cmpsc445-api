import connexion
import threading
import os
import numpy as np
import tensorflow as tf
from flask_cors import CORS
from connexion.resolver import MethodViewResolver
from connexion import FlaskApp
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from datetime import date
from datetime import timedelta
from tensorflow import Tensor
from tensorflow.python.keras.models  import load_model
from pandas import DataFrame
from typing import Tuple
from typing import List
from numpy.typing import ArrayLike


"""
Tensorflow Logging: 
    0 = all messages printed (default)
    1 = INFO messages are not printed
    2 = INFO and WARNING messages are not printed
    3 = INFO, WARNING, and ERROR messages are not printed
"""
os.environ["TF_CPP_MIN_LOG_LEVEL"] = '1'

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
        self.keys = list(self.metadata.tables.keys())

    def __new__(cls):
        """
        Singleton Design Pattern for global scoping 
        """

        if not hasattr(cls, 'instance'):
            cls.instance = super(Database, cls).__new__(cls)

        return cls.instance

class Model(object):

    def __init__(self) -> None:
        self.model = load_model('../cmpsc445-model/model/weights/lstm')

    def __new__(cls):
        """
        Singleton Design Pattern for global scoping 
        """
        if not hasattr(cls, 'instance'):
            cls.instance = super(Model, cls).__new__(cls)

        return cls.instance

    def predict(self, df: DataFrame) -> Tuple[List[date], List[float]]:
        # Ensure these values match the configuation defined in model repo
        config = {
            "input_width": 30,
            "label_width": 5,
            "label_column": "close",
        }
       
        input_width = config["input_width"]
        label_width = config["label_width"]
        column = config["label_column"]
        column_indices = {col:i for i, col in enumerate(df.columns)}
 
        # Record corresponding dates for inputs
        input_dates: List[date] = [timestamp.date() for timestamp in df.index.tolist()]
        input_dates = input_dates[-1*input_width:]

        # Normalize the data
        inputs = df.to_numpy()
        mean = inputs.mean(axis=0)
        std = inputs.std(axis=0)
        inputs = (inputs - mean)/std
        inputs = inputs[-1*input_width:]

        # Convert to tensor and feed into the model to get predictions 
        inputs: Tensor = tf.convert_to_tensor(inputs[None, :, :], dtype=tf.float32)
        predictions = self.model(inputs)
        predictions: ArrayLike = predictions.numpy()

        # Convert to 2D
        predictions = predictions[0]

        # Invert the normalization 
        predictions = (predictions * std) + mean

        # Grab the close column
        predictions = predictions[:, column_indices[column]]
        predictions = np.round(predictions, 2)
        predictions = predictions.tolist()
 
        # Populate dates
        start_date = input_dates[-1]
        prediction_dates = [start_date + timedelta(days=i+1) for i in range(label_width)]

        assert len(prediction_dates) == len(predictions)

        return prediction_dates, predictions
