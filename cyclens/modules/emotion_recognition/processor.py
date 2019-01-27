# coding: utf-8

"""Processor functions for Emoticon Recognation"""

from __future__ import unicode_literals

from ...common.module import Module
from ...common.processor import Processor

from ...utils import (
    ProcessingError,
)

import random
import sys
import cv2
import sys
import numpy as np

class EmotionRecognitionPROC(Processor):

    test : None

    def __init__(self, module=None, ready=None):
        super(EmotionRecognitionPROC, self).__init__(module, ready)
        print("[MODULE::EMOTION_RECOGNITION::PROC]: __init__")


        self._event_ready.set()

    def run(self):
        super(EmotionRecognitionPROC, self).run()


    def stop(self):
        super(EmotionRecognitionPROC, self).stop()
        print("[MODULE::EMOTION_RECOGNITION::PROC]: stop()")
        return

    def predict(self, image):
        if image is None:
            return None
        image = image.reshape([-1, 48, 48, 1])
        return self.model.predict(image)


    def process(self, data, ready):
        super(EmotionRecognitionPROC, self).process(data)

        self.is_busy = False

        ready.set()
        return "ok"
