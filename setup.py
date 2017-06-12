import os
from setuptools import setup, find_packages
import warnings

setup(
    name='aws-tagger',
    version='0.5.1',
    packages=find_packages(),
    include_package_data=True,
    install_requires=[
        'boto3>=1.4.4',
        'botocore>=1.5.7',
        'click>=6.6',
        'docutils>=0.13.1',
        'futures>=3.0.5',
        'jmespath>=0.9.1',
        'python-dateutil>=2.6.0',
        'retrying>=1.3.3',
        's3transfer>=0.1.10',
        'six>=1.10.0'
    ],
    entry_points={
        "console_scripts": [
            "aws-tagger=tagger.cli:cli",
        ]
    },
    namespace_packages = ['tagger'],
    author="Patrick Cullen and the WaPo platform tools team",
    author_email="opensource@washingtonpost.com",
    url="https://github.com/washingtonpost/aws-tagger",
    download_url = "https://github.com/washingtonpost/aws-tagger/tarball/v0.5.1",
    keywords = ['tag', 'tagger', 'tagging', 'aws'],
    classifiers = []
)
