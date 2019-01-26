# coding: utf-8

from __future__ import unicode_literals

from ...common.module import Module

from .preprocessor import GenderPredictionPREP
from .processor import GenderPredictionPROC
from .postprocessor import GenderPredictionPOSP

class GenderPredictionMD(Module):

    def __init__(self):
        super(GenderPredictionMD, self).__init__()
        print("[MODULE::GENDER_PREDICTION]: __init__")

        self.prep = GenderPredictionPREP()
        self.proc = GenderPredictionPROC()
        self.posp = GenderPredictionPOSP()

    def run(self):
        super(GenderPredictionMD, self).run()
        print("[MODULE::GENDER_PREDICTION]: run()")

    def on_data_received(self, data):
        super(GenderPredictionMD, self).on_data_received(data)
        print("[MODULE::GENDER_PREDICTION::ON_DATA_RECEIVED]:")
        print(data)
