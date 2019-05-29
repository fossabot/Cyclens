#!/usr/bin/env python
# coding: utf-8

import codecs
import io
import os
import random
import sys

from .info import (
    __appname__,
    __version__,
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

from .Cyclens import Cyclens

__all__ = ['main', 'Cyclens']

def main(argv=None):
    cyclens_main(argv)



def cyclens_main(argv=None):
    with Cyclens(None) as cyc:

        cyc.run()
