# coding: utf-8

from __future__ import unicode_literals

from cyclens.common.postprocessor import PostProcessor

from .common import *

import os
import sys
import unittest
import copy

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestPostProcessor(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        cls.processor = PostProcessor()
        cls.loaded = cls.processor.try_load()

    def test_processor_loaded(self):
        self.assertTrue(self.loaded)

    def test_module_null_check(self):
        res = self.processor.process(None, copy.deepcopy(SAMPLE_RESULT))

        self.assertFalse(res['success'])
        self.assertNotEqual(res['message'], 'null')

    def test_data_null_check(self):
        res = self.processor.process('test', None)

        self.assertFalse(res['success'])
        self.assertNotEqual(res['message'], 'null')

    def test_remove_unused(self):
        res = self.processor.process('test', copy.deepcopy(SAMPLE_RESULT))

        self.assertFalse('frame_faces' in res)
        self.assertFalse('frame_gray' in res)
        self.assertFalse('frame_rgb' in res)


if __name__ == '__main__':
    TestPostProcessor.main()
