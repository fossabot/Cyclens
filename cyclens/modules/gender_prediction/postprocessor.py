# coding: utf-8

"""Post-processor functions for Gender Prediction"""

from __future__ import unicode_literals

from ...common.module import Module
from ...common.processor import Processor

from ...utils import (
    PostProcessingError,
)

class GenderPredictionPOSP(Processor):

    test : None

    def __init__(self):
        Processor.__init__(self)
        print("[MODULE::GENDER_PREDICTION::POSP]: __init__")
