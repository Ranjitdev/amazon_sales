from src.components.data_ingesion import InitiateDataIngesion
from src.logger import logging
import os
import mysql.connector
import streamlit as st


def connect_mysql():
    database = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="12345678rk",
        database="amazon_sales_data"
    )
    cursor = database.cursor()
    logging.info('Connected to mysql')
    return database, cursor

def data_columns():
    df = InitiateDataIngesion().get_data(data_from='data')
    columns = [i for i in df.columns if i != 'Item' and i != 'Year' and i != 'Month']
    reverse_columns = columns[::-1]
    return df, columns, reverse_columns

def download(raw_data):
    csv = raw_data.to_csv(index=False)
    st.download_button(
        label="Download data as CSV", data=csv, file_name='Data.csv', mime='text/csv',
    )
    logging.info('Downloaded the csv file')

def developer():
    selection = st.selectbox('', ['Logs', 'Readme'])
    if selection == 'Logs':
        logs = []
        for (root, dirs, files) in os.walk('./logs', topdown=True):
            for name in files:
                logs.append(os.path.join(root, name))
        log = st.radio('Logs', logs)
        with open(log, 'r') as file:
            st.dataframe(file.readlines())

    if selection == 'Readme':
        with open('README.md', 'r') as file:
            st.dataframe(file.readlines())

