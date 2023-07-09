from src.exception import CustomException
from src.logger import logging
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pandas as pd
import numpy as np
import os
import sys
from dataclasses import dataclass
import warnings

warnings.simplefilter('ignore')
my_url = URL.create(
    "mysql+pymysql",
    username="root",
    password="12345678rk",
    host="localhost",
    database="amazon_sales_data"
)
connection = create_engine(my_url)


@dataclass
class DataIngesionConfig:
    engine = connection


class InitiateDataIngesion:
    def __init__(self):
        self.config = DataIngesionConfig

    def get_data(self, data=('raw', 'processed')):
        if data == 'raw':
            raw_data = pd.read_sql_table(
                table_name='sales_data_raw', con=self.config.engine.connect(), index_col=None
            )
            logging.info('Fetched the raw data from database')
            return raw_data
        elif data == 'processed':
            processed_data = pd.read_sql_table(
                table_name='sales_data', con=self.config.engine.connect(), index_col=None
            )
            logging.info('Fetched the processed data from database')
            return processed_data

    def preprocess_raw_data(self, raw_data):
        try:
            data = raw_data.copy()
            data.drop([
                'DateKey', 'Invoice Number', 'Item Class', 'Item Number', 'Line Number', 'Order Number',
                'Promised Delivery Date', 'Sales Rep', 'U/M'
            ], inplace=True, axis=1)

            # filling null values with 0
            data.fillna(0, axis=0, inplace=True)

            # Extracting date to year and month
            data['Year'] = 0
            data['Month'] = 0
            data['Year'] = data['Invoice Date'].apply(lambda a: int(str(a).split('-')[0]))
            data['Month'] = data['Invoice Date'].apply(lambda a: int(str(a).split('-')[1]))
            data.drop('Invoice Date', inplace=True, axis=1)

            # sales quantity have a negative value so i am dropping the row
            data.drop(data[data['Sales Quantity'] < 0].index[0], axis=0, inplace=True)

            return data
        except Exception as e:
            raise CustomException(e, sys)

    def insert_into_database(self, raw_data=None, processed_data=None):
        try:
            if raw_data is not None:
                # Raw data insert into database
                processed_data.to_sql('sales_data_raw', self.config.engine, index=None, if_exists='append')
                logging.info('Inserted raw data into database')
            if processed_data is not None:
                # processed data insert into database
                processed_data.to_sql('sales_data', self.config.engine, index=None, if_exists='append')
                logging.info('Insertd processed data into database')
        except Exception as e:
            raise CustomException(e, sys)
