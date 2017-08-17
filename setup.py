from __future__ import (absolute_import, division, print_function)

import os

from setuptools import setup, find_packages

rootpath = os.path.abspath(os.path.dirname(__file__))


def extract_version():
    version = None
    fname = os.path.join(rootpath, 'pygdp', '__init__.py')
    with open(fname) as f:
        for line in f:
            if (line.startswith('__version__')):
                _, version = line.split('=')
                version = version.strip()[1:-1]  # Remove quotation characters
                break
    return version


setup(
    name='pyGDP',
    version=extract_version(),
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
