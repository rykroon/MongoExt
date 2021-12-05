from setuptools import setup, find_packages

setup(
    name='mongoext',
    version='1.0.0',
    author='Ryan Kroon',
    author_email='rykroon.tech@gmail.com',
    packages=find_packages(),
    install_requires=['pymongo', 'motor']
)
