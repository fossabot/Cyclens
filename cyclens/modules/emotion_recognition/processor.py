# coding: utf-8

"""Processor functions for Emoticon Recognation"""

from __future__ import unicode_literals

from ...common.module import Module
from ...common.processor import Processor

from ...utils import (
    ProcessingError,
)

class EmotionRecognitionPROC(Processor):

    test : None

    def __init__(self):
        super(EmotionRecognitionPROC, self).__init__()
        print("[MODULE::EMOTION_RECOGNITION::PROC]: __init__")

    def run(self):
        super(EmotionRecognitionPROC, self).run()
        return

    def process(self, data, ready):
        super(EmotionRecognitionPROC, self).process(data)


        self.is_busy = False

        ready.set()
        return 8977
