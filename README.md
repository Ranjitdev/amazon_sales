# Amazon Sales Data Analysis

## Overview of Amazon sales data analysis: -  
**Sales management has gained importance to meet increasing competition and the need for improved methods of distribution to reduce cost and to increase profits. Sales management today is the most important function in a commercial and business enterprise.**  
**So I decided to develop an application for meet the insights  of sales trends.**   

## Data location: -  
- description: [Here](https://drive.google.com/file/d/1fK7DM6WZjh7lBANXlqdkDjojOMdRDqbs/view)  
- data:
  - drive: [Here]([Here](https://drive.google.com/file/d/1fK7DM6WZjh7lBANXlqdkDjojOMdRDqbs/view))
  - local processed data: [Here](artifacts/data.csv)
  - local raw data: [Here](artifacts/raw_data.csv)
- database: MySQL/localhost/amazon_sales_data  
- tables:  
  - raw data: sales_data_raw  
  - processed data: sales_data  
- project notebook: [notebook](notebook_amazon_sales/EDA.ipynb)  
- data details: [report](notebook_amazon_sales/report.html)  

## Functions description:
  - > InitiateDataIngesion().get_data(data_from='data') # Data fetcher function
    - data: local processed data
    - raw: raw data from Mysql database
    - processed: processed data from mysql database
    - local_raw_data: local raw data
  - > InitiateDataIngesion().preprocess_raw_data(raw_data=df) # Raw data preprocessor function
  - > InitiateDataIngesion().insert_into_database(raw_data=df, processed_data=data) #Data insertion function in MySQL
  - > from src.utils import connect_mysql # MySQL connector function for sql query
  - > from src.components.chart_generator import InitiateChartGenerator, InitiatePlotChart # chart generator and plotter function

## Setup: -
  - Run for create virtual environment
    - > conda create -p venv python=3.10 -y
  - Run before start application: -
    - > pip install -r requirements.txt
  - Run for create docker image: -
    - > docker build -t ranjitkundu/amazon_sales:v1 .
  - Show docker images: -
    - > docker images
  - Run the docker image in container: - 
    - > docker run -p 8501:8501 ranjitkundu/amazon_sales:v1
  - Initiate GitHub: -
    - > git init
  - Add all files in GitHub: -
    - > git add .
  - Commit code in GitHub: -
    - > git commit -m "message"
  - Push code in GitHub: -
    - > git push -u origin main

