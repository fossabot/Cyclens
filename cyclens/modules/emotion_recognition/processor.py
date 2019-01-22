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
        Processor.__init__(self)
        print("[MODULE::EMOTION_RECOGNITION::PROC]: __init__")
