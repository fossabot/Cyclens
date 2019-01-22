# coding: utf-8

"""Post-processor functions for Face Dedection"""

from __future__ import unicode_literals

from ...common.module import Module
from ...common.processor import Processor

from ...utils import (
    PostProcessingError,
)

class FaceDedectionPOSP(Processor):

    test : None

    def __init__(self):
        Processor.__init__(self)
        print("[MODULE::FACE_DEDECTION::POSP]: __init__")
