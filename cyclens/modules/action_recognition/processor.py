# coding: utf-8

"""Processor functions for Action Recognation"""

from __future__ import unicode_literals

from ...common.module import Module
from ...common.processor import Processor

from ...utils import (
    ProcessingError,
)

class ActionRecognitionPROC(Processor):

    test : None

    def __init__(self):
        Processor.__init__(self)
        print("[MODULE::ACTION_RECOGNITION::PROC]: __init__")