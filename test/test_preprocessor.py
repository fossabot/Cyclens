# coding: utf-8

from __future__ import unicode_literals

from cyclens.common.preprocessor import PreProcessor

from .common import *

import os
import sys
import unittest

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
