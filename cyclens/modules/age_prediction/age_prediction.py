# coding: utf-8

from __future__ import unicode_literals

from ...common.module import Module

from .preprocessor import AgePredictionPREP
from .processor import AgePredictionPROC
from .postprocessor import AgePredictionPOSP

class AgePredictionMD(Module):

    def __init__(self):
        Module.__init__(self)
        print("[MODULE::AGE_PREDICTION]: __init__")

        self.prep = AgePredictionPREP()
        self.proc = AgePredictionPROC()
        self.posp = AgePredictionPOSP()

    def on_data_received(self, data):
        print("[MODULE::AGE_PREDICTION::ON_DATA_RECEIVED]: " + data)
        return

    def run(self):
        print("[MODULE::AGE_PREDICTION]: run()")
