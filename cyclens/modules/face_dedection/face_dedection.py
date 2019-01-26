# coding: utf-8

from __future__ import unicode_literals

from ...common.module import Module

from .preprocessor import FaceDedectionPREP
from .processor import FaceDedectionPROC
from .postprocessor import FaceDedectionPOSP

class FaceDedectionMD(Module):

    def __init__(self):
        super(FaceDedectionMD, self).__init__()
        print("[MODULE::FACE_DEDECTION]: __init__")

        self.prep = FaceDedectionPREP()
        self.proc = FaceDedectionPROC()
        self.posp = FaceDedectionPOSP()

    def run(self):
        super(FaceDedectionMD, self).run()
        print("[MODULE::FACE_DEDECTION]: run()")

    def on_data_received(self, data):
        super(FaceDedectionMD, self).on_data_received(data)
        print("[MODULE::FACE_DEDECTION::ON_DATA_RECEIVED]:")
        print(data)
