from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
import numpy as np
import pandas as pd
import sys
import os
import mysql.connector


def mysql_connector():
    database = mysql.connector.connect(
        host="localhost",
        user="root",
        passwd="12345678rk",
        database="amazon_sales_data"
    )
    cursor = database.cursor()
    return database, cursor
