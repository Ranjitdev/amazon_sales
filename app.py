from src.components.data_ingesion import InitiateDataIngesion
from src.components.chart_generator import InitiateChartGenerator, InitiatePlotChart
import streamlit as st

# df = InitiateDataIngesion().get_data(data_from='local_raw_data')
# data = InitiateDataIngesion().preprocess_raw_data(raw_data=df)
# InitiateDataIngesion().insert_into_database(raw_data=df, processed_data=data)

# Header
st.subheader(':blue[______________________________________________________]')
st.title(':blue[Amazon Sales data analysis]')
st.subheader(':blue[______________________________________________________]')

# Trend selection and distribution chart generator uses InitiateChartGenerator class
try:
    col1, col2, col3 = st.columns(3)
    with col1:
        trend_selection = st.radio(
            ':blue[Select chart type to generate sales trend chart Yearly, Monthly, Combined and other charts]', (
                'Default', 'Monthly total', 'Yearly total',
                'Yearly month wise bar chart', 'Yearly month wise line chart',
                'Monthly Year wise', 'Top products'
            )
        )
    with col2:
        feature = st.radio(
            ':green[Select the column]', (
                ['Discount Amount', 'List Price', 'Sales Amount', 'Sales Amount Based on List Price',
                 'Sales Cost Amount', 'Sales Margin Amount', 'Sales Price', 'Sales Quantity'][::-1]
            )
        )
    with col3:
        counter = st.radio(
            ':red[Select calculation type]',
                ['Total', 'Average', 'Maximum', 'Minimum']
        )
    st.caption('Hover on image and click extend for full size')
    chart_fig = InitiateChartGenerator(trend_selection, feature, counter).generate_trend_chart()
    if type(chart_fig) != list:
        st.pyplot(chart_fig)

    elif type(chart_fig) == list:
        for i in chart_fig:
            st.pyplot(i)
except:
    pass

# Selection of one of the price column and plot distribution uses InitiatePlotChart class
selected = st.selectbox(
    ':blue[Select the column to generate Data distribution count plot]',
    (['Discount Amount', 'List Price', 'Sales Amount', 'Sales Amount Based on List Price', 'Sales Cost Amount',
      'Sales Margin Amount', 'Sales Price', 'Sales Quantity']))
st.caption('Hover on image and click extend for full size')
InitiatePlotChart().distribution_plot(selected)

# Select two column to compare
st.subheader(':blue[Comparison of sales amounts yearly month wise: -]')
col1, col2 = st.columns(2)
with col1:
    option1 = st.radio(
        'Select First element',
        ['Discount Amount', 'List Price', 'Sales Amount', 'Sales Amount Based on List Price', 'Sales Cost Amount',
         'Sales Margin Amount', 'Sales Price', 'Sales Quantity'][::-1])
with col2:
    option2 = st.radio(
        'Select second element',
        ['Discount Amount', 'List Price', 'Sales Amount', 'Sales Amount Based on List Price', 'Sales Cost Amount',
         'Sales Margin Amount', 'Sales Price', 'Sales Quantity'])
InitiatePlotChart().multi_features_plot(option1, option2)

