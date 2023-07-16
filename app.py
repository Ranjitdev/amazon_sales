from src.components.data_ingesion import InitiateDataIngesion
from src.components.chart_generator import InitiateChartGenerator
from src.utils import data_columns, download, developer
import streamlit as st
import warnings
warnings.simplefilter('ignore')

_, columns, reverse_columns = data_columns()
with st.sidebar:
    my_bar = st.radio('', options=('Home', 'Sales Trend', 'Uni variate Analysis', 'Bi variate Analysis', 'Developer'))

# Dashboard
if my_bar == 'Home':
    st.subheader(':blue[___________________________________________________]')
    st.title(':blue[Amazon Sales]')
    st.subheader(':blue[___________________________________________________]')
    st.caption('New sales data entry')
    raw_data = InitiateDataIngesion().get_data(data_from='local_raw_data')
    new_data = InitiateDataIngesion().single_data_entry(old_data=raw_data)
    tab1, tab2, tab3 = st.tabs(['Upload CSV', 'Download CSV', 'Data Viewer'])
    with tab1:
        InitiateDataIngesion().mulltiple_entry(old_data=raw_data)
    with tab2:
        download(raw_data)
    with tab3:
        st.dataframe(raw_data)
    # st.caption('Top Products')
    # InitiateChartGenerator().word_cloud()
    # InitiateChartGenerator().top_products()

# Trend selection and distribution chart generator uses generate_trend_chart class
if my_bar == 'Sales Trend':
    try:
        st.subheader(':blue[______________________________________________________]')
        st.title(':blue[Sales Trend]')
        st.subheader(':blue[______________________________________________________]')
        col1, col2, col3 = st.columns(3)
        with col1:
            trend_selection = st.radio(
                ':blue[Chart Combination]', (
                    'Monthly total', 'Yearly total', 'Yearly month wise bar chart', 'Yearly month wise line chart',
                    'Monthly Year wise'
                )
            )
        with col2:
            feature = st.radio(
                ':blue[Select Parameter]', columns)
        with col3:
            counter = st.radio(':blue[Select Total of]', ['Total', 'Average', 'Maximum', 'Minimum'])

        st.caption('Hover on image and click extend for full size')
        chart_fig = InitiateChartGenerator().generate_trend_chart(trend_selection, feature, counter)
    except:
        pass

# Selection of one of the column and plot distribution uses univariate_plot class
if my_bar == 'Uni variate Analysis':
    st.subheader(':blue[______________________________________________________]')
    st.title(':blue[Uni variate Analysis]')
    st.subheader(':blue[______________________________________________________]')
    selected = st.selectbox(':blue[Select the parameter to generate data distribution plot]', columns)
    st.caption('Hover on image and click extend for full size')
    InitiateChartGenerator().univariate_plot(selected)

# Select two column to compare
if my_bar == 'Bi variate Analysis':
    st.subheader(':blue[______________________________________________________]')
    st.title(':blue[Bi variate Analysis]')
    st.subheader(':blue[______________________________________________________]')
    st.subheader(':blue[Comparison of sales amounts yearly month wise: -]')
    col1, col2 = st.columns(2)
    with col1:
        option1 = st.radio('Select First element', columns)
    with col2:
        option2 = st.radio('Select second element', reverse_columns)
    InitiateChartGenerator().bivariate_plot(option1, option2)

if my_bar == 'Developer':
    developer()
