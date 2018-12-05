#!/usr/bin/env python
# coding: utf-8

import os.path
import warnings
import sys

try:
    from setuptools import setup, Command
    setuptools_available = True
except ImportError:
    from distutils.core import setup, Command
    setuptools_available = False


# ===============
# Functions
# ===============

# Codes...

# ===============
# Setup Info
# ===============

DESCRIPTION_SHRT = 'Human Classifier'
DESCRIPTION_LONG = 'Human Classifier'

setup(
    name='Cyclens',
    version='0.0.0',
    description=DESCRIPTION_SHRT,
    long_description=DESCRIPTION_LONG,
    author='Furkan Türkal',
    author_email='furkan.turkal@hotmail.com',
    maintainer='Metin Ur',
    maintainer_email='metin__ur.1997@hotmail.com',
    url='https://bitbucket.org/bw-cyclens/cyclens-server',
    license='Unlicense',
    packages=find_packages(exclude=('tests', 'docs'))
    classifiers=[
        'License :: Unlicensed',
        'Development Status :: 0 - Development/Init',
        'Environment :: Console',
        'Environment :: GUI Application',
        'Intended Audience :: Developers',
        'Intended Audience :: Researchers',
        'License :: Private :: Unlicensed',
        'Operating System :: MacOS :: MacOS X',
        'Operating System :: Microsoft :: Windows',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Artificial Intelligence  :: Tensorflow',
        'Topic :: Computer Vision :: Open CV',
        'Topic :: Software Development :: Final Project',
    ],
    **params
)
