# coding: utf-8

"""Processor functions for Face Dedection"""

from __future__ import unicode_literals

from ...common.module import Module
from ...common.processor import Processor

from ...utils import (
    ProcessingError,
)

class FaceDedectionPROC(Processor):

    test : None

    def __init__(self):
        Processor.__init__(self)
        print("[MODULE::FACE_DEDECTION::PROC]: __init__")
