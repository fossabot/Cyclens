# coding: utf-8

"""Pre-processor functions for Face Dedection"""

from __future__ import unicode_literals

from ...common.module import Module
from ...common.processor import Processor

from ...utils import (
    PreProcessingError,
)

class FaceDedectionPREP(Processor):

    test : None

    def __init__(self):
        Processor.__init__(self)
        print("[MODULE::FACE_DEDECTION::PREP]: __init__")
