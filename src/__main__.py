#!/usr/bin/env python
# coding: utf-8

from __future__ import unicode_literals

# Execute with
# $ python -m src

import sys

if __package__ is None and not hasattr(sys, 'frozen'):
    # direct call of __main__.py
    import os.path
    path = os.path.realpath(os.path.abspath(__file__))
    sys.path.insert(0, os.path.dirname(os.path.dirname(path)))

import src

if __name__ == '__main__':
    src.main()
