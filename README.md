# Amazon Sales Data Analysis

## Overview of Amazon sales data analysis: -  
**Sales management has gained importance to meet increasing competition and the need for improved methods of distribution to reduce cost and to increase profits. Sales management today is the most important function in a commercial and business enterprise.**  
**So I decided to develop an application for meet the insights  of sales trends.**   

## Data location: -  
- description: [Here](https://drive.google.com/file/d/1fK7DM6WZjh7lBANXlqdkDjojOMdRDqbs/view)  
- data:
  - drive: [Here](https://drive.google.com/file/d/1fK7DM6WZjh7lBANXlqdkDjojOMdRDqbs/view)
  - local processed data: [Here](artifacts/data.csv)
  - local raw data: [Here](artifacts/raw_data.csv)
- database: MySQL/localhost/amazon_sales_data  
- tables:  
  - raw data: sales_data_raw  
  - processed data: sales_data  
- project notebook: [notebook](notebook_amazon_sales/EDA.ipynb)  
- data details: [report](notebook_amazon_sales/report.html)  

## Functions description:
  - InitiateDataIngesion().get_data(data_from='data') # Get data from various locations
    - data: local processed data
    - raw: raw data from Mysql database
    - processed: processed data from mysql database
    - local_raw_data: local raw data
    - notebook: actual excel file
  - InitiateDataIngesion().preprocess_raw_data(raw_data) # Data preprocessor function
  - InitiateDataIngesion().save_data(self, raw_data=None, processed_data=None, location='local') # Saving option
    - raw_data: by default None if not none saves the raw data into location
    - processed_data: by default None if not none saves the processed data into location
    - location: by default saves in local dir if database saves data in database
  - InitiateDataIngesion().single_data_entry(old_data) # single data entry operation with gui
  - InitiateDataIngesion().mulltiple_entry(old_data) # single data entry operation with gui
    - fetches data from csv file and updates the old data if all columns are same

## Setup: -
  - Run for create virtual environment
    - > conda create -p venv python=3.10 -y
  - Run before start application: -
    - > pip install -r requirements.txt
  - Run the application: -
  - > streamlit run app.py
  - Access in browser: -
  - > localhost:8501
  - Run for create docker image: -
    - > docker build -t ranjitkundu/amazon_sales:v1 .
    - Show docker images: -
      - > docker images
    - Run the docker image in container: - 
      - > docker run -p 8501:8501 ranjitkundu/amazon_sales:v1
  - Push code in GitHub: -
    - > git init
    - Add all files in GitHub: -
      - > git add .
    - Commit code in GitHub: -
      - > git commit -m "message"
    - Push code in GitHub: -
      - > git push -u origin main
- AWS deploy: -
  -  Create an Ubuntu EC2 Instance during creation download the key pair
  -  Launch Instance
  -  When the instance is ready, click “Connect” and choose the tab EC2 Instance Connect and find for public ip and username
  -  Go to PuTTYgen and generate key using previously downloaded key pair
  - connect in PuTTY with that key in ssh>auth and ip in ip address and username in data
  - Go to WinSCP connect with aws file server drag and drop the required files
  - Pass the commands on PuTTY to install requirement files and setup
    - > sudo apt-get update
    - > sudo apt-get install python3-pip
    - > pip3 install -r requirements.txt
    - > streamlit run app.py
    - > screen -R deploy streamlit run app.py
  
  - AWS link: - http://ec2-13-53-77-189.eu-north-1.compute.amazonaws.com:8501/
