# coding: utf-8

"""Processor functions for Face Recognition"""

from __future__ import unicode_literals

from ...common.module import Module
from ...common.processor import Processor

from ...utils import (
    ProcessingError,
)

class FaceRecognitionPROC(Processor):

    test : None

    def __init__(self):
        Processor.__init__(self)
        print("[MODULE::FACE_RECOGNITION::PROC]: __init__")
