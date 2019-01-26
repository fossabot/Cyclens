# coding: utf-8

"""Post-processor functions for Emoticon Recognation"""

from __future__ import unicode_literals

from ...common.module import Module
from ...common.processor import Processor

from ...utils import (
    PostProcessingError,
)

class EmotionRecognitionPOSP(Processor):

    test : None

    def __init__(self):
        super(EmotionRecognitionPOSP, self).__init__()
        print("[MODULE::EMOTION_RECOGNITION::POSP]: __init__")

    def run(self):
        super(EmotionRecognitionPOSP, self).run()
        return

    def process(self, data, ready):
        super(EmotionRecognitionPOSP, self).process(data)


        self.is_busy = False

        ready.set()
        return 9999
