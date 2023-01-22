# coding=utf-8
from setuptools import setup, find_packages

with open("README.md", "r") as fi:
    long_description = fi.read()

with open('VERSION') as fi:
    version = fi.read().strip()

with open('requirements.txt') as fi:
    requirements=fi.readlines()

setup(
    name='georgstage',
    version=version,
    download_url=f'https://github.com/skipperkongen/georgstage/archive/refs/tags/{version}.tar.gz',
    author="Pimin Konstantin Kefaloukos",
    author_email="skipperkongen@gmail.com",
    description="Hjælpeprogram til skoleskibet Georg Stage",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/skipperkongen/georgstage",
    install_requires=requirements,
    packages=find_packages('src'),
    package_dir={'': 'src'},
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
    entry_points = {
        'console_scripts': ['georgstage=georgstage.cli:main'],
    }
)
