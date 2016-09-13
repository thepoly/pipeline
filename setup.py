from setuptools import setup, find_packages

setup(
    name='pipeline',
    version='0.1.dev1',
    packages=['pipeline'],
    install_requires=['marshmallow', 'falcon', 'peewee']
)
