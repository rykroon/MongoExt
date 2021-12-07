from datetime import date
from setuptools import setup, find_packages

#python setup.py sdist
version = date.today().isoformat().replace('-', '.')

setup(
    name='mongoext',
    version=version,
    author='Ryan Kroon',
    author_email='rykroon.tech@gmail.com',
    packages=find_packages(),
    install_requires=['pymongo', 'motor']
)
