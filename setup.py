from setuptools import setup, find_packages

setup(
    name='kronos_api',
    version='0.1',
    description='My API project for accessing different tools',
    author='Your Name',
    author_email='your.email@example.com',
    packages=find_packages(),
    install_requires=[
        'configparser',
        ...
    ],
)