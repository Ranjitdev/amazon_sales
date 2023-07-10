from src.components.data_ingesion import InitiateDataIngesion
from src.utils import connect_mysql
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import altair as alt
import os
import sys


@dataclass
class ChartGeneraotorConfig:
    data = pd.read_csv(r'artifacts/data.csv', index_col=False)


class InitiatePlotChart:
    def __init__(self):
        self.config = ChartGeneraotorConfig
        self.data = ChartGeneraotorConfig.data

    def distribution_plot(self, selected):
        try:
            col1, col2 = st.columns(2)
            with col1:
                fig, ax = plt.subplots()
                sns.histplot(
                    data=self.data, x=selected, hue='Year', bins=5, palette='bright', kde=True, alpha=0.3, ax=ax
                )
                st.pyplot(fig)
            with col2:
                fig, ax = plt.subplots()
                sns.violinplot(data=self.data, y=selected, x='Year', linewidth=2, ax=ax)
                st.pyplot(fig)
            st.text('Hover on image and click extend for full size')
            logging.info('Plotted distribution plot')
        except Exception as e:
            raise CustomException(e, sys)

    def multi_features_plot(self, feature1, feature2):
        try:
            st.write(f':green[Total {feature1} vs Total {feature2}]')
            fig = alt.Chart(self.data).mark_circle().encode(
                x=feature1, y=feature2, size='Year', color='Month',
                tooltip=['Year', 'Month', feature1, feature2])

            st.altair_chart(fig, use_container_width=True)
            logging.info('Plotted Multi feature plot')
        except Exception as e:
            raise CustomException(e, sys)


class InitiateChartGenerator:
    def __init__(self, selection):
        self.config = ChartGeneraotorConfig
        self.selection = selection

    def generate_trend_chart(self):
        try:
            data = self.config.data

            # Default word cloud generator
            if self.selection == 'Default':
                stopwords = STOPWORDS
                words = ''
                for i in data['Item'].unique():
                    word = str(i).casefold()
                    words += word

                wordcloud = WordCloud(
                    width=800, height=800,
                    background_color='white',
                    stopwords=stopwords,
                    min_font_size=10
                ).generate(words)

                fig, ax = plt.subplots(figsize=(5, 5))
                ax.imshow(wordcloud)
                plt.axis("off")
                plt.tight_layout(pad=0)
                logging.info(f'Generated {self.selection} plot')
                return fig

            # Monthly sales report generator
            elif self.selection == 'Monthly':
                fig, ax = plt.subplots(figsize=(20, 10))
                sns.barplot(
                    data=data, y='Sales Quantity', x='Month', estimator='sum', palette='bright', errorbar=None, ax=ax
                )
                ax.bar_label(ax.containers[0])
                plt.title('Sales trend month wise')
                plt.ylabel('Total sales')
                plt.xlabel('Month')
                logging.info(f'Generated {self.selection} plot')
                return fig

            # Yearly sales report generator
            elif self.selection == 'Yearly':
                fig, ax = plt.subplots(1, 2, figsize=(20, 10))
                plt.subplot(121)
                sns.barplot(
                    data=data, y='Sales Quantity', x='Year', palette='bright',
                    errorbar=None, width=0.5, estimator='sum'
                )
                plt.ticklabel_format(style='plain', axis='y')
                plt.title('Sales trend Year wise')

                plt.subplot(122)
                plt.pie(
                    data.groupby('Year')['Sales Quantity'].sum(),
                    shadow=True, autopct='%1.0f%%', labels=['2017', '2018', '2019'], explode=[0.1, 0, 0.1]
                )
                logging.info(f'Generated {self.selection} plot')
                return fig

                # All over report generator all years together Yearly month wise
            elif self.selection == 'Yearly Month wise':
                yearly_monthwise = pd.DataFrame(
                    data.groupby(['Year', 'Month'], sort=False)['Sales Quantity'].sum()
                ).reset_index()

                fig, ax = plt.subplots(figsize=(20, 10))
                sns.barplot(
                    data=yearly_monthwise, x='Month', y='Sales Quantity', hue='Year', ax=ax, palette='bright', width=0.5
                )
                for i in range(len(yearly_monthwise['Year'].unique())):
                    ax.bar_label(ax.containers[i], color='red', size=12)
                plt.legend(title='Year wise monthly sales', loc='lower right')
                plt.title('Sales trend all years month wise')
                plt.ylabel('Total sales')
                plt.xlabel('Year wise months')
                logging.info(f'Generated {self.selection} plot')
                return fig

            # Monthly year wise report generator separate reports for every year
            elif self.selection == 'Monthly Year wise':
                yearly_monthwise = pd.DataFrame(
                    data.groupby(['Year', 'Month'], sort=False)['Sales Quantity'].sum()
                ).reset_index()
                path = []
                for year in yearly_monthwise['Year'].unique():
                    current = yearly_monthwise[yearly_monthwise['Year'] == year]

                    fig, ax = plt.subplots(1, 2, figsize=(20, 10))

                    plt.subplot(121)
                    sns.barplot(data=current, y='Sales Quantity', x='Month', estimator='sum', palette='bright',
                                errorbar=None, ax=ax[0], width=0.5)
                    for i in ax[0].containers:
                        ax[0].bar_label(i, color='blue', size=8)
                    plt.title(str(year) + ' Sales trend month wise')
                    plt.ylabel('Total sales')
                    plt.xlabel('Month')

                    plt.subplot(122)
                    plt.title(str(year) + ' Sales trend percentage month wise')
                    plt.pie(current['Sales Quantity'], labels=current['Month'], autopct='%1.1f%%', shadow=True)

                    path.append(fig)
                logging.info(f'Generated {self.selection} plot')
                return path

            elif self.selection == 'Top products':
                fig, ax = plt.subplots(figsize=(20, 15))

                plt.subplot(121)
                df = pd.DataFrame(data.groupby('Item')['Sales Amount'].sum()).sort_values(by='Sales Amount',
                                                                                          ascending=False)[:5]
                plt.pie(df['Sales Amount'], labels=df.index, autopct='%1.1f%%', shadow=True,
                        explode=[0.1, 0.1, 0, 0, 0])
                plt.title('Top 5 products based on sales price')

                plt.subplot(122)
                df = pd.DataFrame(data.groupby('Item')['Sales Quantity'].sum()).sort_values(by='Sales Quantity',
                                                                                            ascending=False)[:5]
                plt.pie(df['Sales Quantity'], labels=df.index, autopct='%1.1f%%', shadow=True,
                        explode=[0.1, 0.1, 0, 0, 0])
                plt.title('Top 5 products based on sales quantity')
                return fig

        except Exception as e:
            raise CustomException(e, sys)




