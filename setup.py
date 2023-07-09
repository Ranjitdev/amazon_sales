from setuptools import setup, find_packages
from typing import List

Project_name = 'amazon_sales_review'
Version = '1.0.0'
Author = 'Ranjit Kundu'
Description = ''


def get_requirements() -> List[str]:
    with open('requirements.txt') as required_files:
        required_list = required_files.readlines()
        required_list = [i.replace('\n', '') for i in required_list]
        if '-e .' in required_list:
            required_list.remove('-e .')
        return required_list


setup(
    name=Project_name,
    version=Version,
    author=Author,
    description=Description,
    packages=find_packages(),
    install_requires=get_requirements()
)