from src.components.data_ingesion import InitiateDataIngesion
from src.utils import connect_mysql, data_columns
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import altair as alt
import os
import sys


@dataclass
class ChartGeneraotorConfig:
    data, columns, _ = data_columns()


class InitiateChartGenerator:
    def __init__(self):
        self.config = ChartGeneraotorConfig
        self.data = ChartGeneraotorConfig.data
        self.columns = ChartGeneraotorConfig.columns

    def generate_trend_chart(self, selection, feature, counter):
        data = self.config.data
        global yearly_group
        if counter == 'Sum':
            yearly_group = pd.DataFrame(
                data.groupby(['Year', 'Month'], sort=False)[feature].sum()
            ).reset_index()
        elif counter == 'Average':
            yearly_group = pd.DataFrame(
                data.groupby(['Year', 'Month'], sort=False)[feature].mean()
            ).reset_index()
        elif counter == 'Maximum':
            yearly_group = pd.DataFrame(
                data.groupby(['Year', 'Month'], sort=False)[feature].max()
            ).reset_index()
        elif counter == 'Minimum':
            yearly_group = pd.DataFrame(
                data.groupby(['Year', 'Month'], sort=False)[feature].min()
            ).reset_index()

        try:
            # Monthly total sales
            if selection == 'Monthly total':
                fig, ax = plt.subplots(figsize=(20, 10))
                sns.barplot(
                    data=yearly_group, y=feature, x='Month',
                    estimator='sum', palette='bright', errorbar=None, ax=ax
                )
                ax.bar_label(ax.containers[0])
                plt.title('Sales trend Monthly total')
                plt.ylabel('Total sales')
                plt.xlabel('Month')
                logging.info(f'Generated {selection} to {feature} plot')
                st.pyplot(fig)

            # Yearly total sales
            elif selection == 'Yearly total':
                fig, ax = plt.subplots(1, 2, figsize=(20, 10))
                plt.subplot(121)
                sns.barplot(
                    data=yearly_group, y=feature, x='Year', palette='bright',
                    errorbar=None, width=0.5, estimator='sum'
                )
                plt.ticklabel_format(style='plain', axis='y')
                plt.title('Sales trend Yearly total')

                plt.subplot(122)
                plt.pie(
                    data.groupby('Year')[feature].sum(),
                    shadow=True, autopct='%1.0f%%', labels=self.data['Year'].unique()
                )
                logging.info(f'Generated {selection} to {feature} plot')
                st.pyplot(fig)

            # Bar chart
            elif selection == 'Yearly month wise bar chart':
                fig, ax = plt.subplots(figsize=(20, 10))
                sns.barplot(
                    data=yearly_group, x='Month', y=feature, hue='Year',
                    ax=ax, palette='bright', width=0.8, estimator='sum'
                )
                for i in range(len(yearly_group['Year'].unique())):
                    ax.bar_label(ax.containers[i], color='red', size=12)
                plt.ticklabel_format(style='plain', axis='y')
                plt.legend(title='Yearly month wise sales', loc='lower right')
                plt.title('Sales trend yearly month wise')
                plt.ylabel('Total sales')
                plt.xlabel('Year wise months')
                logging.info(f'Generated {selection} to {feature} plot')
                st.pyplot(fig)

            # Yearly month wise line chart
            elif selection == 'Yearly month wise line chart':
                fig, ax = plt.subplots(figsize=(20, 10))
                sns.pointplot(data=yearly_group, x='Month', y=feature, hue='Year', ax=ax, estimator='sum')
                plt.legend(title='Year wise monthly sales', loc='lower right')
                plt.legend(title='Yearly month wise sales', loc='lower right')
                plt.title('Sales trend yearly month wise')
                plt.ylabel('Total sales')
                plt.xlabel('Year wise months')
                logging.info(f'Generated {selection} to {feature} plot')
                st.pyplot(fig)

            # Monthly year wise report generator separate reports for every year
            elif selection == 'Monthly Year wise':
                path = []
                for year in yearly_group['Year'].unique():
                    current = yearly_group[yearly_group['Year'] == year]

                    fig, ax = plt.subplots(1, 2, figsize=(20, 10))

                    plt.subplot(121)
                    sns.barplot(data=current, y=feature, x='Month', estimator='sum',
                                palette='bright', errorbar=None, ax=ax[0], width=0.5)
                    for i in ax[0].containers:
                        ax[0].bar_label(i, color='blue', size=8)
                    plt.title(str(year) + ' Sales trend month wise')
                    plt.ylabel('Total sales')
                    plt.xlabel('Month')

                    plt.subplot(122)
                    plt.title(str(year) + ' Sales trend percentage month wise')
                    plt.pie(current[feature], labels=current['Month'], autopct='%1.1f%%', shadow=True)

                    st.pyplot(fig)
                logging.info(f'Generated {selection} to {feature} plot')

        except Exception as e:
            raise CustomException(e, sys)

    def univariate_plot(self, selected):
        try:
            fig, ax = plt.subplots(figsize=(20, 10))
            sns.histplot(
                data=self.data, x=selected, hue='Year', bins=5, palette='bright', kde=True, alpha=0.3, ax=ax
            )
            plt.ticklabel_format(style='plain', axis='y')
            plt.title(f'Uni variate Analysis of {selected}')
            st.pyplot(fig)
            fig, ax = plt.subplots(figsize=(20, 10))
            sns.violinplot(data=self.data, y=selected, x='Year', linewidth=2, ax=ax)
            plt.title(f'Uni variate Analysis of {selected}')
            st.pyplot(fig)

            tab1, tab2 = st.tabs(["Point plot", "Bar plot"])
            circle = alt.Chart(self.data).mark_circle().encode(x=selected, y='Month', size='Year', color='Year')
            bar = alt.Chart(self.data).mark_bar().encode(x=selected, y='Month', size='Year', color='Year')
            with tab1:
                st.altair_chart(circle, theme="streamlit", use_container_width=True)
            with tab2:
                st.altair_chart(bar, theme=None, use_container_width=True)
            logging.info('Plotted Uni variate plot')
        except Exception as e:
            raise CustomException(e, sys)

    def bivariate_plot(self, feature1, feature2):
        try:
            st.write(f':green[Total {feature1} vs Total {feature2}]')
            st.caption('Hover on image and click extend for full size or three dot to save the chart')

            circle = alt.Chart(self.data).mark_circle().encode(
                x=feature1, y=feature2, size='Year', color='Month',
                tooltip=['Year', 'Month', feature1, feature2])
            st.altair_chart(circle, use_container_width=True)

            fig, ax = plt.subplots(figsize=(20, 10))
            sns.regplot(data=self.data, x=feature1, y=feature2, ax=ax)
            plt.title(f'Relational plot of {feature1} and {feature2}')
            st.pyplot(fig)

            graph = sns.FacetGrid(self.data, col='Year', hue="Month")
            graph.map(sns.scatterplot, feature1, feature2, edgecolor="w").add_legend()
            st.pyplot(graph)
            logging.info('Plotted Bi variate plot')
        except Exception as e:
            raise CustomException(e, sys)

    def multivariate_plot(self):
        try:
            st.caption('Hover on image and click extend for full size or three dot to save the chart')
            fig = sns.pairplot(self.data[self.columns])
            st.pyplot(fig)
            st.dataframe(self.data[self.columns].describe().T)
        except Exception as e:
            raise CustomException(e, sys)

    def top_products(self):
        fig, ax = plt.subplots(figsize=(20, 15))
        df = pd.DataFrame(self.data.groupby('Item')['Sales Amount'].sum()).sort_values(
            by='Sales Amount', ascending=False)[:5]
        plt.pie(df['Sales Amount'], labels=df.index, autopct='%1.1f%%', shadow=True,
                explode=[0.1, 0.1, 0, 0, 0])
        plt.title('Top 5 products based on sales price')
        st.pyplot(fig)

        fig, ax = plt.subplots(figsize=(20, 15))
        df = pd.DataFrame(self.data.groupby('Item')['Sales Quantity'].sum()).sort_values(
            by='Sales Quantity', ascending=False)[:5]
        plt.pie(df['Sales Quantity'], labels=df.index, autopct='%1.1f%%', shadow=True,
                explode=[0.1, 0.1, 0, 0, 0])
        plt.title('Top 5 products based on sales quantity')
        st.pyplot(fig)


    def word_cloud(self):
        # Word cloud generator
        stopwords = STOPWORDS
        words = ''
        for i in self.data['Item'].unique():
            word = str(i).casefold()
            words += word

        wordcloud = WordCloud(
            width=800, height=800, background_color='white', stopwords=stopwords, min_font_size=10
        ).generate(words)

        fig, ax = plt.subplots(figsize=(5, 5))
        ax.imshow(wordcloud)
        plt.axis("off")
        plt.tight_layout(pad=0)
        st.pyplot(fig)
        return fig




