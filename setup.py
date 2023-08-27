from setuptools import setup, find_packages

setup(
    name='kronos_api',
    version='0.1',
    description='A simple API wrapper for Kronos Workforce Ready REST API methods. Built for use at KIPP SoCal in 2023.',
    author='Shane Traister',
    author_email='straister@me.com',
    packages=find_packages(),
    install_requires=[
        'configparser',
        'pandas',
        'requests',
    ],
)

