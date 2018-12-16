#!/usr/bin/env python
# coding: utf-8

class Cyclens(object):
    """Cyclens class.


    Really...


    Available options:

    help:               Show help
    version:            Show version

    """

    params = None

    def __init__(self, params=None, auto_init=True):

        if params is None:
            params = {}

        print('init')

    def __del__(self):
        print('__del__')

    def __enter__(self):
        print('__enter__')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print('__exit__')

    def test(self):
        print('test')