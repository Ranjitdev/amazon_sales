from src.components.data_ingesion import InitiateDataIngesion
from src.components.chart_generator import InitiateChartGenerator
from src.utils import connect_mysql
from PIL import Image
import streamlit as st
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.figure_factory as ff
import pandas as pd
import numpy as np
data = InitiateDataIngesion().get_data(data='processed')

st.subheader(':blue[______________________________________________________]')
st.title(':blue[Amazon Sales data analysis]')
st.subheader(':blue[______________________________________________________]')

col1, col2 = st.columns(2)
with col1:
    trend_selection = st.radio(
        'Generate sales trend charts Yearly, Monthly and Combined', (
            'Default', 'Monthly', 'Yearly', 'Yearly Month wise', 'Monthly Year wise'
        )
    )
with col2:
    file = InitiateChartGenerator(trend_selection).generate_chart()
    if type(file) != list:
        chart = Image.open(file)
        st.image(chart, caption='Hover on image and click extend for full size')

    elif type(file) == list:
        chart1 = Image.open(file[0])
        st.image(chart1, caption='Hover on image and click full size')
        chart2 = Image.open(file[1])
        st.image(chart2, caption='Hover on image and click full size')
        chart3 = Image.open(file[2])
        st.image(chart3, caption='Hover on image and click full size')

select_single = st.selectbox(
    'Find data distributions with count plot',
    ([i for i in data.columns if data[i].dtype != 'O' if i != 'Year' and i != 'CustKey'])
)
fig, ax = plt.subplots()
sns.histplot(data=data, x=select_single, hue='Year', bins=5, palette='bright', kde=True, alpha=0.3, ax=ax)
st.pyplot(fig)


