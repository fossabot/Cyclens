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
        Processor.__init__(self)
        print("[MODULE::EMOTION_RECOGNITION::PREP]: __init__")
