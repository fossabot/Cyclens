# coding: utf-8

"""Processor functions for Age Prediction"""

from __future__ import unicode_literals

from ...common.module import Module
from ...common.processor import Processor

from ...utils import (
    ProcessingError,
)

class AgePredictionPROC(Processor):

    test : None

    def __init__(self):
        Processor.__init__(self)
        print("[MODULE::AGE_PREDICTION::PROC]: __init__")
