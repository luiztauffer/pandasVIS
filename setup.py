# -*- coding: utf-8 -*-

from setuptools import setup, find_packages

# Get the long description from the README file
with open('README.md', 'r') as f:
    long_description = f.read()

requirements = ['PySide2', 'matplotlib', 'numpy', 'pandas', 'pandas-profiling',
                'plotly', 'scikit-learn', 'qtvoila', 'qtconsole']

setup_requirements = []

test_requirements = []

setup(
    author="Luiz Tauffer",
    author_email='luiz@taufferconsulting.com',
    python_requires='>=3.5',
    classifiers=[
        'Development Status :: 2 - Pre-Alpha',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: BSD License',
        'Natural Language :: English',
        'Programming Language :: Python :: 3',
        'Programming Language :: Python :: 3.5',
        'Programming Language :: Python :: 3.6',
        'Programming Language :: Python :: 3.7',
        'Programming Language :: Python :: 3.8',
    ],
    description='Tabular data exploration GUI.',
    install_requires=requirements,
    license="BSD license",
    long_description=long_description,
    long_description_content_type='text/markdown',
    include_package_data=True,
    keywords='pandasvis',
    name='pandasVis',
    packages=find_packages(include=['pandasvis', 'pandasvis.*']),
    setup_requires=setup_requirements,
    test_suite='tests',
    tests_require=test_requirements,
    url='https://github.com/luiztauffer/pandasVIS',
    version='0.1.0',
    zip_safe=False,
)
