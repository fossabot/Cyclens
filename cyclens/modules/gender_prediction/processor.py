# coding: utf-8

"""Processor functions for Gender Prediction"""

from __future__ import unicode_literals

from ...common.module import Module
from ...common.processor import Processor

from ...utils import (
    ProcessingError,
)

class GenderPredictionPROC(Processor):

    test : None

    def __init__(self):
        Processor.__init__(self)
        print("[MODULE::GENDER_PREDICTION::PROC]: __init__")
