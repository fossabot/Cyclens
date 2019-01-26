# coding: utf-8

"""Pre-processor functions for Emoticon Recognation"""

from __future__ import unicode_literals

from ...common.module import Module
from ...common.processor import Processor

from ...utils import (
    PreProcessingError,
)

class EmotionRecognitionPREP(Processor):

    test : None

    def __init__(self):
        super(EmotionRecognitionPREP, self).__init__()
        print("[MODULE::EMOTION_RECOGNITION::PREP]: __init__")

    def run(self):
        super(EmotionRecognitionPREP, self).run()
        return

    def process(self, data, ready):
        super(EmotionRecognitionPREP, self).process(data)


        self.is_busy = False

        ready.set()
        return 55555
