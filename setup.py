#!/usr/bin/env python
# coding: utf-8

from datetime import datetime as dt

import os.path
import warnings
import sys

from src import constants

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

PROJECT_NAME = 'Cyclens'
PROJECT_PACKAGE_NAME = 'src'
PROJECT_LICENSE = 'Apache License 2.0'
PROJECT_AUTHOR = 'Furkan Türkal'
PROJECT_AUTHOR_EMAIL = 'furkan.turkal@hotmail.com'
PROJECT_MAINTAINER = 'Metin Ur'
PROJECT_MAINTAINER_EMAIL = 'metin__ur.1997@hotmail.com'
PROJECT_COPYRIGHT = ' 2018-{}'.format(dt.now().year)
PROJECT_URL = 'https://bitbucket.org/bw-src/src-server'

DESCRIPTION_SHRT = 'Human Classifier'
DESCRIPTION_LONG = 'Human Classifier for Humans'

setup(
    name=PROJECT_NAME,
    version=constants.__version__,
    description=DESCRIPTION_SHRT,
    long_description=DESCRIPTION_LONG,
    author=PROJECT_AUTHOR,
    author_email=PROJECT_AUTHOR_EMAIL,
    maintainer=PROJECT_MAINTAINER,
    maintainer_email=PROJECT_MAINTAINER_EMAIL,
    url=PROJECT_URL,
    license=PROJECT_LICENSE,
    packages=find_packages(exclude=('tests', 'docs')),
    zip_safe=False,
    test_suite='tests',
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
