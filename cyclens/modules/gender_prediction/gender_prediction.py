# coding: utf-8

from __future__ import unicode_literals

from ...common.module import Module

from .preprocessor import GenderPredictionPREP
from .processor import GenderPredictionPROC
from .postprocessor import GenderPredictionPOSP

class GenderPredictionMD(Module):

    def __init__(self):
        Module.__init__(self)
        print("[MODULE::GENDER_PREDICTION]: __init__")

        self.prep = GenderPredictionPREP()
        self.proc = GenderPredictionPROC()
        self.posp = GenderPredictionPOSP()

    def on_data_received(self, data):
        print("[MODULE::GENDER_PREDICTION::ON_DATA_RECEIVED]: " + data)
        return

    def run(self):
        print("[MODULE::GENDER_PREDICTION]: run()")
