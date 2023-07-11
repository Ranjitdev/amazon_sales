import os

from src.exception import CustomException
from src.logger import logging
from sqlalchemy import create_engine
from sqlalchemy.engine import URL
import pandas as pd
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
    local_data = 'notebook_amazon_sales/SALESDATA.xlsx'
    raw_data = 'artifacts/raw_data.csv'
    data = 'artifacts/data.csv'


class InitiateDataIngesion:
    def __init__(self):
        self.config = DataIngesionConfig
        os.makedirs(os.path.dirname(self.config.data), exist_ok=True)

    def get_data(self, data_from='data'):
        if data_from == 'raw':
            raw_data = pd.read_sql_table(
                table_name='sales_data_raw', con=self.config.engine.connect(), index_col=None
            )
            logging.info('Fetched the raw data from database')
            return raw_data

        elif data_from == 'processed':
            processed_data = pd.read_sql_table(
                table_name='sales_data', con=self.config.engine.connect(), index_col=None
            )
            logging.info('Fetched the processed data from database')
            return processed_data

        elif data_from == 'local_raw_data':
            df = pd.read_excel(self.config.local_data)
            df.to_csv(self.config.raw_data, index=False, header=True)
            return df

        elif data_from == 'data':
            df = pd.read_csv(self.config.data)
            return df

    def preprocess_raw_data(self, raw_data):
        try:
            logging.info('Got the local data for preprocess')
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
            data = data.sort_values(by=['Year', 'Month']).reset_index(drop=True)
            data['Month'] = data['Month'].map({
                1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',
                11: 'Nov', 12: 'Dec'
            })
            data.drop('Invoice Date', inplace=True, axis=1)

            # sales quantity have a negative value so i am dropping the row
            data.drop(data[data['Sales Quantity'] < 0].index[0], axis=0, inplace=True)

            data.to_csv(self.config.data, index=False, header=True)
            logging.info('Saved the processed data in  artifacts')
            return data
        except Exception as e:
            raise CustomException(e, sys)

    def insert_into_database(self, raw_data=None, processed_data=None):
        try:
            if raw_data is not None:
                # Raw data insert into database
                processed_data.to_sql('sales_data_raw', self.config.engine, index=None, if_exists='replace')
                logging.info('Inserted raw data into database')
            if processed_data is not None:
                # processed data insert into database
                processed_data.to_sql('sales_data', self.config.engine, index=None, if_exists='replace')
                logging.info('Insertd processed data into database')
        except Exception as e:
            raise CustomException(e, sys)


if __name__ == '__main__':
    df = InitiateDataIngesion().get_data(data_from='local_raw_data')
    data = InitiateDataIngesion().preprocess_raw_data(raw_data=df)
    InitiateDataIngesion().insert_into_database(raw_data=df, processed_data=data)
