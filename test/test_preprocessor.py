# coding: utf-8

"""
cyclens.test
~~~~~~~~~~~~

Implements pre-processor testing functions.

This program comes with ABSOLUTELY NO WARRANTY; This is free software,
and you are welcome to redistribute it under certain conditions; See
file LICENSE, which is part of this source code package, for details.

:copyright: Copyright © 2019, The Cyclens Project
:license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals

import sys
import unittest

from .common import *
from cyclens.common.preprocessor import PreProcessor

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPreProcessor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.processor = PreProcessor()
        cls.loaded = cls.processor.try_load()

    def test_processor_loaded(self):
        self.assertTrue(self.loaded)

    def test_cascade_not_null(self):
        self.assertIsNotNone(self.processor.CASC_FACE)

    def test_data_null_check(self):
        res = self.processor.process(None)

        self.assertFalse(res['success'])
        self.assertNotEqual(res['message'], 'null')

    def test_no_face(self):
        for face in get_imgs(PATH_FACES_0):
            res = self.processor.process(face)

            self.assertTrue(res['success'])
            self.assertEqual(res['found'], 0)
            self.assertNotEqual(res['message'], 'null')

    def test_one_face(self):
        for face in get_imgs(PATH_FACES_1):
            res = self.processor.process(face)

            self.assertTrue(res['success'])
            self.assertEqual(res['found'], 1)
            self.assertEqual(res['message'], 'null')


if __name__ == '__main__':
    TestPreProcessor.main()
