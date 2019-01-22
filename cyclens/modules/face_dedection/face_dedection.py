# coding: utf-8

from __future__ import unicode_literals

from ...common.module import Module

from .preprocessor import FaceDedectionPREP
from .processor import FaceDedectionPROC
from .postprocessor import FaceDedectionPOSP

class FaceDedectionMD(Module):

    def __init__(self):
        Module.__init__(self)
        print("[MODULE::FACE_DEDECTION]: __init__")

        self.prep = FaceDedectionPREP()
        self.proc = FaceDedectionPROC()
        self.posp = FaceDedectionPOSP()

    def on_data_received(self, data):
        print("[MODULE::FACE_DEDECTION::ON_DATA_RECEIVED]: " + data)
        return

    def run(self):
        print("[MODULE::FACE_DEDECTION]: run()")
