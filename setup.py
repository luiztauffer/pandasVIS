# -*- coding: utf-8 -*-
from setuptools import setup, find_packages

# Get the long description from the README file
with open('README.md', 'r') as f:
    long_description = f.read()

setup(name = 'pandasVIS',
      version = '0.0.1',
      description = 'Tabular data exploration GUI.',
      long_description = long_description,
      long_description_content_type = 'text/markdown',
      author = 'Luiz Tauffer',
      email = 'luiz@taufferconsulting.com',
      packages=find_packages(),
      include_package_data = True,
      install_requires = ['pyqt', 'matplotlib', 'numpy', 'pandas', 'pandas-profiling',
                          'pyqtgraph', 'plotly', 'cufflinks', 'scikit-learn'],
      )
