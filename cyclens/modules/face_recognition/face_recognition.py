# coding: utf-8

from __future__ import unicode_literals

from ...common.module import Module

from .preprocessor import FaceRecognitionPREP
from .processor import FaceRecognitionPROC
from .postprocessor import FaceRecognitionPOSP

class FaceRecognitionMD(Module):

    def __init__(self, ready=None):
        super(FaceRecognitionMD, self).__init__(ready)
        print("[MODULE::FACE_DEDECTION]: __init__")

        self.prep = FaceRecognitionPREP()
        self.proc = FaceRecognitionPROC()
        self.posp = FaceRecognitionPOSP()

        self._event_ready.set()

    def run(self):
        super(FaceRecognitionMD, self).run()
        print("[MODULE::FACE_RECOGNITION]: run()")

    def on_data_received(self, data):
        super(FaceRecognitionMD, self).on_data_received(data)
        print("[MODULE::FACE_RECOGNITION::ON_DATA_RECEIVED]:")
