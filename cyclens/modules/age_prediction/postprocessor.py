# coding: utf-8

"""Post-processor functions for Age Prediction"""

from __future__ import unicode_literals

from ...common.module import Module
from ...common.processor import Processor

from ...utils import (
    PostProcessingError,
)

class AgePredictionPOSP(Processor):

    test : None

    def __init__(self):
        Processor.__init__(self)
        print("[MODULE::AGE_PREDICTION::POSP]: __init__")
