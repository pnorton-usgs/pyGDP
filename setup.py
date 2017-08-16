from __future__ import (absolute_import, division, print_function)

import os

from pyGDP import __version__

from setuptools import setup, find_packages

rootpath = os.path.abspath(os.path.dirname(__file__))


setup(
    name='pyGDP',
    version=__version__,
    description='Interface to the USGS GeoData Portal',
    long_description=open('README.md').read(),
    license='Public Domain',
    maintainer='Jordan Read',  # Originally Xao Yang
    maintainer_email='jread@usgs.gov',
    py_modules=['pyGDP','GDP_XML_Generator'],
    packages=find_packages(),
    url='https://github.com/USGS-CIDA/pyGDP',
    test_suite='tests',
)
