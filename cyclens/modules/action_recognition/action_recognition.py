# coding: utf-8

from __future__ import unicode_literals

from ...common.module import Module

from .preprocessor import ActionRecognitionPREP
from .processor import ActionRecognitionPROC
from .postprocessor import ActionRecognitionPOSP

class ActionRecognitionMD(Module):

    def __init__(self, ready=None):
        super(ActionRecognitionMD, self).__init__(ready)
        print("[MODULE::ACTION_RECOGNITION]: __init__")

        self.prep = ActionRecognitionPREP()
        self.proc = ActionRecognitionPROC()
        self.posp = ActionRecognitionPOSP()

        self._ready.set()

    def run(self):
        super(ActionRecognitionMD, self).run()
        print("[MODULE::ACTION_RECOGNITION]: run()")

    def on_data_received(self, data):
        super(ActionRecognitionMD, self).on_data_received(data)
        print("[MODULE::ACTION_RECOGNATION::ON_DATA_RECEIVED]:")
        print(data)
