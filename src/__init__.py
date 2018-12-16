#!/usr/bin/env python
# coding: utf-8

import codecs
import io
import os
import random
import sys

from .Cyclens import Cyclens

__all__ = ['main', 'Cyclens']

def main(argv=None):
    try:
        print('[PROGRAM::MAIN]: Started')
        cyclens_main(argv)
    except KeyboardInterrupt:
        sys.exit('\nERROR: Interrupted by user')



def cyclens_main(argv=None):
    print('[CYCLENS::MAIN]: Started')

    with Cyclens(None) as cyc:

        cyc.test()