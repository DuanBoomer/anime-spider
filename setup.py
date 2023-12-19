# Automatically created by: shub deploy

from setuptools import setup, find_packages

setup(
    name         = 'project',
    version      = '3.0.9',
    packages     = find_packages(),
    entry_points = {'scrapy': ['settings = animescrapper.settings']},
)
