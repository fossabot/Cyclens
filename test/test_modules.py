# coding: utf-8

from __future__ import unicode_literals

from cyclens.common.preprocessor import PreProcessor
from cyclens.common.postprocessor import PostProcessor

from cyclens.modules.age_prediction.age_prediction import AgePredictionMD
from cyclens.modules.emotion_recognition.emotion_recognition import EmotionRecognitionMD
from cyclens.modules.face_recognition.face_recognition import FaceRecognitionMD
from cyclens.modules.gender_prediction.gender_prediction import GenderPredictionMD

from .common import *

import os
import sys
import logging
import unittest
import threading

import tensorflow as tf

sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


class TestModuleER(unittest.TestCase):

    def setUp(self):
        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        tf.get_logger().setLevel(logging.ERROR)
        tf.logging.set_verbosity(tf.logging.ERROR)

        _ready = threading.Event()

        self.pre_processor = PreProcessor()
        self.loaded = self.pre_processor.try_load()
        self.post_processor = PostProcessor()
        self.loaded = self.post_processor.try_load()

        _ready.clear()
        self.module_ap = AgePredictionMD(_ready)
        _ready.wait()

        _ready.clear()
        self.module_er = EmotionRecognitionMD(_ready)
        _ready.wait()

        _ready.clear()
        self.module_gp = GenderPredictionMD(_ready)
        _ready.wait()

    def test_module_ap_cascade_not_null(self):
        self.assertIsNotNone(self.module_ap.CASC_AGE)

    def test_module_er_cascade_not_null(self):
        self.assertIsNotNone(self.module_er.CASC_EMOTION)

    def test_module_gp_cascade_not_null(self):
        self.assertIsNotNone(self.module_gp.CASC_GENDER)

    def test_module_er_emotion_count(self):
        self.assertEqual(len(self.module_er.EMOTIONS), 7)

    def test_module_gp_gender_count(self):
        self.assertEqual(len(self.module_gp.GENDERS), 2)

    def test_module_ap(self):
        for sample in SAMPLE_MODULE_TESTS:
            face = get_img(sample['image'])
            result = sample['ap']

            pre = self.pre_processor.process(face)

            self.assertEqual(pre['message'], 'null')
            self.assertEqual(pre['found'], 1)
            self.assertTrue(pre['success'])

            res = self.module_ap.do_process(pre)

            self.assertEqual(pre['message'], 'null')
            self.assertEqual(res['found'], 1)
            self.assertTrue(res['success'])

            self.assertEqual(res['faces'][0]['ap'], result)

    def test_module_er(self):
        for sample in SAMPLE_MODULE_TESTS:
            face = get_img(sample['image'])
            result = sample['er']

            pre = self.pre_processor.process(face)

            self.assertEqual(pre['message'], 'null')
            self.assertEqual(pre['found'], 1)
            self.assertTrue(pre['success'])

            res = self.module_er.do_process(pre)

            self.assertEqual(pre['message'], 'null')
            self.assertEqual(res['found'], 1)
            self.assertTrue(res['success'])

            self.assertEqual(res['faces'][0]['er'], result)

    def test_module_gp(self):
        for sample in SAMPLE_MODULE_TESTS:
            face = get_img(sample['image'])
            result = sample['gp']

            pre = self.pre_processor.process(face)

            self.assertEqual(pre['message'], 'null')
            self.assertEqual(pre['found'], 1)
            self.assertTrue(pre['success'])

            res = self.module_gp.do_process(pre)

            self.assertEqual(pre['message'], 'null')
            self.assertEqual(res['found'], 1)
            self.assertTrue(res['success'])

            self.assertEqual(res['faces'][0]['gp'], result)


if __name__ == '__main__':
    TestModuleER.main()
