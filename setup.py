#!/usr/bin/env python
# coding: utf-8

""" [Cyclens setup file]

Examples:

        Linux::

        python setup.py install

"""

from datetime import datetime as dt

import os.path
import warnings
import sys

from cyclens import constants

try:
    from setuptools import setup, find_packages, Command
    setuptools_available = True
except ImportError:
    from distutils.core import setup, Command
    setuptools_available = False

from .cyclens import (
    __version__,
    __appname__,
    __license__,
    __url__,
    __author__,
    __authormail__,
    __maintainer__,
    __maintainermail__,
    __description__,
    __descriptionfull__,
    __copyright__,
    __licensefull__,
)

with open("README.md", "r") as readme_file:
    readme = readme_file.read()

requirements = ["numpy>=1.16.2"]

setup(
    version         = __version__,
    name            = __appname__,
    license         = __license__,
    url             = __url__,
    author          = __author__,
    author_email    = __authormail__,
    maintainer      = __maintainer__,
    maintainer_email= __maintainermail__,
    long_description= readme,
    long_description_content_type = "text/markdown",
    packages        = find_packages(),
    install_requires= requirements,
    zip_safe        = False,
    test_suite      = 'test',
    classifiers     = [
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
)
