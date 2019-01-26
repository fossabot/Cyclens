# coding: utf-8

from __future__ import unicode_literals

from ...common.module import Module

from .preprocessor import AgePredictionPREP
from .processor import AgePredictionPROC
from .postprocessor import AgePredictionPOSP

class AgePredictionMD(Module):

    def __init__(self, ready=None):
        super(AgePredictionMD, self).__init__(ready)
        print("[MODULE::AGE_PREDICTION]: __init__")

        self.prep = AgePredictionPREP()
        self.proc = AgePredictionPROC()
        self.posp = AgePredictionPOSP()

        self._ready.set()

    def run(self):
        super(AgePredictionMD, self).run()
        print("[MODULE::AGE_PREDICTION]: run()")

    def on_data_received(self, data):
        super(AgePredictionMD, self).on_data_received(data)
        print("[MODULE::AGE_PREDICTION::ON_DATA_RECEIVED]:")
        print(data)

