from src.components.data_ingesion import InitiateDataIngesion
from src.utils import connect_mysql
from src.exception import CustomException
from src.logger import logging
from dataclasses import dataclass
from wordcloud import WordCloud, STOPWORDS
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st
import os
import sys


@dataclass
class ChartGeneraotorConfig:
    path = 'artifacts/charts'
    data = InitiateDataIngesion().get_data(data='processed')


class InitiateChartGenerator:
    def __init__(self, selection):
        self.config = ChartGeneraotorConfig
        self.selection = selection
        os.makedirs(self.config.path, exist_ok=True)

    def generate_chart(self):
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

                plt.figure(figsize=(5, 5), facecolor=None)
                plt.imshow(wordcloud)
                plt.axis("off")
                plt.tight_layout(pad=0)

                path = os.path.join(self.config.path, self.selection + '.png')
                plt.savefig(path, dpi=100)
                logging.info(str(self.selection) + ' Chart generated successfully')
                return path

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

                path = os.path.join(self.config.path, self.selection+'.png')
                plt.savefig(path, dpi=100)
                logging.info(str(self.selection) + ' Chart generated successfully')
                return path

            # Yearly sales report generator
            elif self.selection == 'Yearly':
                plt.figure(figsize=(20, 10))
                plt.subplot(121)
                sns.barplot(
                    data=data, y='Sales Quantity', x='Year', estimator='sum', palette='bright', errorbar=None, width=0.5
                )
                plt.ticklabel_format(style='plain', axis='y')
                plt.subplot(122)
                plt.pie(
                    data.groupby('Year')['Sales Quantity'].sum(),
                    shadow=True, autopct='%1.0f%%', labels=['2017', '2018', '2019'], explode=[0.1, 0, 0.1]
                )

                path = os.path.join(self.config.path, self.selection + '.png')
                plt.savefig(path, dpi=100)
                logging.info(str(self.selection) + ' Chart generated successfully')
                return path

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

                    path.append(os.path.join(self.config.path, str(year) + '.png'))
                    plt.savefig(os.path.join(self.config.path, str(year) + '.png'), dpi=100)
                    logging.info(str(year) + ' Chart generated successfully')
                return path

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

                path = os.path.join(self.config.path, 'all_years_moth_wise' + '.png')
                plt.savefig(path, dpi=100)
                logging.info(str(self.selection) + ' Chart generated successfully')
                return path

        except Exception as e:
            raise CustomException(e, sys)