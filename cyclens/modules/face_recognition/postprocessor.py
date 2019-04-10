# coding: utf-8

"""Post-processor functions for Face Recognition"""

from __future__ import unicode_literals

from ...common.module import Module
from ...common.processor import Processor

from ...utils import (
    PostProcessingError,
)

class FaceRecognitionPOSP(Processor):

    test : None

    def __init__(self):
        Processor.__init__(self)
        print("[MODULE::FACE_RECOGNITION::POSP]: __init__")
