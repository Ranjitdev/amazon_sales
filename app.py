from src.components.data_ingesion import InitiateDataIngesion
from src.components.chart_generator import InitiateChartGenerator, InitiatePlotChart
from src.utils import connect_mysql
import streamlit as st

# df = InitiateDataIngesion().get_data(data_from='local_raw_data')
# data = InitiateDataIngesion().preprocess_raw_data(raw_data=df)
# InitiateDataIngesion().insert_into_database(raw_data=df, processed_data=data)
# my_db, cursor = connect_mysql()

# Header
st.subheader(':blue[______________________________________________________]')
st.title(':blue[Amazon Sales data analysis]')
st.subheader(':blue[______________________________________________________]')

# Trend selection and chart generator uses InitiateChartGenerator class
col1, col2 = st.columns(2)
with col1:
    trend_selection = st.radio(
        ':blue[Generate sales trend chart Yearly, Monthly, Combined and other charts]', (
            'Default', 'Monthly', 'Yearly', 'Yearly Month wise', 'Monthly Year wise', 'Top products'
        )
    )
with col2:
    chart_fig = InitiateChartGenerator(trend_selection).generate_trend_chart()
    if type(chart_fig) != list:
        st.pyplot(chart_fig)

    elif type(chart_fig) == list:
        for i in chart_fig:
            st.pyplot(i)

# Selection of one of the price column and plot distribution uses InitiatePlotChart class
selected = st.selectbox(
    ':blue[Select the column to generate Data distribution count plot]',
    (['Discount Amount', 'List Price', 'Sales Amount', 'Sales Amount Based on List Price', 'Sales Cost Amount',
      'Sales Margin Amount', 'Sales Price', 'Sales Quantity']))
InitiatePlotChart().distribution_plot(selected)

# Select two column to compare
st.header(':blue[Comparison chart yearly month wise: -]')
col1, col2 = st.columns(2)
with col1:
    option1 = st.radio(
        'Select First column',
        ['Discount Amount', 'List Price', 'Sales Amount', 'Sales Amount Based on List Price', 'Sales Cost Amount',
         'Sales Margin Amount', 'Sales Price', 'Sales Quantity'][::-1])
with col2:
    option2 = st.radio(
        'Select second column',
        ['Discount Amount', 'List Price', 'Sales Amount', 'Sales Amount Based on List Price', 'Sales Cost Amount',
         'Sales Margin Amount', 'Sales Price', 'Sales Quantity'])
InitiatePlotChart().multi_features_plot(option1, option2)

