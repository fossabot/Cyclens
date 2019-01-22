# coding: utf-8

from __future__ import unicode_literals

from ...common.module import Module

from .preprocessor import ActionRecognitionPREP
from .processor import ActionRecognitionPROC
from .postprocessor import ActionRecognitionPOSP

class ActionRecognitionMD(Module):

    def __init__(self):
        Module.__init__(self)
        print("[MODULE::ACTION_RECOGNITION]: __init__")

        self.prep = ActionRecognitionPREP()
        self.proc = ActionRecognitionPROC()
        self.posp = ActionRecognitionPOSP()

    def on_data_received(self, data):
        print("[MODULE::ACTION_RECOGNATION::ON_DATA_RECEIVED]: " + data)
        return

    def run(self):
        print("[MODULE::ACTION_RECOGNITION]: run()")
