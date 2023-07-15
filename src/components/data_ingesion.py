import os
import streamlit as st
import numpy as np
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
    notebook_data = 'notebook_amazon_sales/SALESDATA.xlsx'
    raw_data = 'artifacts/raw_data.csv'
    data = 'artifacts/data.csv'


class InitiateDataIngesion:
    def __init__(self):
        self.config = DataIngesionConfig
        os.makedirs(os.path.dirname(self.config.data), exist_ok=True)

    def get_data(self, data_from='data'):
        # Raw data from mysql table
        if data_from == 'raw':
            raw_data = pd.read_sql_table(
                table_name='sales_data_raw', con=self.config.engine.connect(), index_col=None
            )
            logging.info('Fetched the raw data from database')
            return raw_data

        # Processed data from mysql table
        elif data_from == 'processed':
            processed_data = pd.read_sql_table(
                table_name='sales_data', con=self.config.engine.connect(), index_col=None
            )
            logging.info('Fetched the processed data from database')
            return processed_data

        # Raw data local
        elif data_from == 'local_raw_data':
            raw_local = pd.read_csv(self.config.raw_data)
            return raw_local

        # Processed data local
        elif data_from == 'data':
            data = pd.read_csv(self.config.data)
            return data

        # Actual data
        elif data_from == 'notebook':
            data = pd.read_excel(self.config.notebook_data)
            return data

    def preprocess_raw_data(self, raw_data):
        try:
            logging.info('Got the local data for preprocess')
            data = raw_data.copy()
            data.drop([
                'CustKey', 'DateKey', 'Invoice Number', 'Item Class', 'Item Number', 'Line Number', 'Order Number',
                'Promised Delivery Date', 'Sales Rep', 'U/M'
            ], inplace=True, axis=1)

            # filling null values with 0
            data.fillna(0, axis=0, inplace=True)

            # Extracting date to year and month
            data['Year'] = 0
            data['Month'] = 0
            data['Year'] = data['Invoice Date'].apply(lambda a: str(str(a).split('-')[0]))
            data['Month'] = data['Invoice Date'].apply(lambda a: int(str(a).split('-')[1]))
            data = data.sort_values(by=['Year', 'Month']).reset_index(drop=True)
            data['Year'] = data['Year'].astype(str)
            data['Month'] = data['Month'].map({
                1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct',
                11: 'Nov', 12: 'Dec'
            })
            data.drop('Invoice Date', inplace=True, axis=1)

            # sales quantity have a negative value so i am dropping the row
            data.drop(data[data['Sales Quantity'] < 0].index[0], axis=0, inplace=True)
            logging.info('Processed data successfully')
            return data
        except Exception as e:
            raise CustomException(e, sys)

    def save_data(self, raw_data=None, processed_data=None, location='local'):
        try:
            if location == 'local':
                if raw_data is not None:
                    # save raw data in local
                    raw_data.to_csv(self.config.raw_data, index=False)
                if processed_data is not None:
                    # processed data save in local
                    processed_data.to_csv(self.config.data, index=False)
            elif location == 'database':
                if raw_data is not None:
                    # Raw data insert into database
                    raw_data.to_sql('sales_data_raw', self.config.engine, index=False, if_exists='replace')
                    logging.info('Inserted raw data into database')
                if processed_data is not None:
                    # processed data insert into database
                    processed_data.to_sql('sales_data', self.config.engine, index=False, if_exists='replace')
                    logging.info('Inserted processed data into database')
        except Exception as e:
            raise CustomException(e, sys)

    def single_data_entry(self, old_data):
        with st.form('Data Entry'):
            col1, col2, col3, col4, col5 = st.columns(5)
            col6, col7, col8, col9, col10 = st.columns(5)
            col11, col12, col13, col14, col15 = st.columns(5)
            with col1:
                CustKey = st.text_input('Customer')
            with col2:
                Invoice_Date = st.date_input('Invoice Date')
            with col3:
                Promised_Delivery_Date = st.date_input('Promised Delivery Date')
            with col4:
                Invoice_Number = st.text_input('Invoice Number')
            with col5:
                Order_Number = st.text_input('Order Number')
            with col6:
                Item_Number = st.text_input('Item Number')
            with col7:
                Line_Number = st.text_input('Line Number')
            with col8:
                Item_Class = st.selectbox('Item Class', (['P01', np.nan]))
            with col9:
                Item = st.selectbox('Item', (old_data['Item'].unique()))
            with col10:
                Sales_Quantity = st.number_input('Sales Quantity')
            with col11:
                List_Price = st.number_input('List Price')
            with col12:
                Sales_Price = st.number_input('Sales Price')
            with col13:
                Sales_Cost_Amount = st.number_input('Sales Cost Amount')
            with col14:
                Sales_Rep = st.text_input('Sales Rep')
            with col15:
                UM = st.selectbox('U/M', (old_data['U/M'].unique()))
            submit = st.form_submit_button('Submit')
            if submit:
                if int(CustKey) > 0 and int(Order_Number) > 0:
                    Sales_Amount_Based_on_List_Price = List_Price * Sales_Quantity
                    Sales_Amount = Sales_Price * Sales_Quantity
                    Sales_Margin_Amount = Sales_Amount - Sales_Cost_Amount
                    Discount_Amount = Sales_Amount_Based_on_List_Price - Sales_Amount
                    DateKey = Invoice_Date
                    new_data = {
                        'CustKey': CustKey, 'DateKey': DateKey, 'Discount Amount': Discount_Amount,
                        'Invoice Date': Invoice_Date, 'Invoice Number': Invoice_Number, 'Item Class': Item_Class,
                        'Item Number': Item_Number, 'Item': Item, 'Line Number': Line_Number,
                        'List Price': List_Price, 'Order Number': Order_Number,
                        'Promised Delivery Date': Promised_Delivery_Date, 'Sales Amount': Sales_Amount,
                        'Sales Amount Based on List Price': Sales_Amount_Based_on_List_Price,
                        'Sales Cost Amount': Sales_Cost_Amount, 'Sales Margin Amount': Sales_Margin_Amount,
                        'Sales Price': Sales_Price, 'Sales Quantity': Sales_Quantity,
                        'Sales Rep': Sales_Rep, 'U/M': UM
                    }
                    st.dataframe(pd.DataFrame([new_data]))
                    new_data = pd.concat([old_data, pd.DataFrame([new_data])], axis=0, ignore_index=True)
                    self.save_data(raw_data=new_data)
                    processed = self.preprocess_raw_data(raw_data=new_data)
                    self.save_data(processed_data=processed)
                    self.save_data(raw_data=new_data, processed_data=processed, location='database')
                    st.caption('New data inserted')
                    logging.info('File updated successfully')
        return old_data

    def mulltiple_entry(self, old_data):
        st.caption('Bunch input from csv file')
        uploaded_file = st.file_uploader("Choose a csv file")
        if uploaded_file is not None:
            try:
                df = pd.read_csv(uploaded_file)
                st.dataframe(df)
                new_data = pd.concat([df, old_data], axis=0, ignore_index=True)
                self.save_data(raw_data=new_data)
                processed = self.preprocess_raw_data(raw_data=new_data)
                self.save_data(processed_data=processed)
                self.save_data(raw_data=new_data, processed_data=processed, location='database')
                logging.info('Data updated')
                st.caption('File updated successfully')
            except:
                st.caption(':red[Check file format or file content]')

if __name__=='__main__':
    raw_data = InitiateDataIngesion().get_data(data_from='notebook')
    processed_data = InitiateDataIngesion().preprocess_raw_data(raw_data=raw_data)
    InitiateDataIngesion().save_data(raw_data=raw_data, processed_data=processed_data, location='local')
    InitiateDataIngesion().save_data(raw_data=raw_data, processed_data=processed_data, location='database')
