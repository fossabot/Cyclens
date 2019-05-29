# coding: utf-8

from __future__ import unicode_literals

from ...common.module import Module
from ...common.wide_resnet import WideResNet

import threading

import cv2
from os.path import isfile

from .processor import AgePredictionPROC


class AgePredictionMD(Module):

    def __init__(self, ready=None):
        super(AgePredictionMD, self).__init__(ready)

        self.module_id = 1
        self.module_name = 'age_prediction'

        _ready = threading.Event()

        _ready.clear()
        self.processor = AgePredictionPROC(self, _ready)
        _ready.wait()

        self.CASC_FACE = None
        self.CASC_AGE = None

        detection_model_path = '../data/models/detection/haarcascade_frontalface_default.xml'
        age_model_path = '../data/models/age/weights.18-4.06.hdf5'

        if isfile(detection_model_path):
            self.CASC_FACE = cv2.CascadeClassifier(detection_model_path)
            print("---> Face detection data set Loaded!!!")
        else:
            print("---> Couldn't find cascade model")
            exit(1)

        if isfile(age_model_path):
            self.face_size = 64
            self.CASC_AGE = WideResNet(64, depth = 16, k = 8)()
            self.CASC_AGE.load_weights(age_model_path)
            self.CASC_AGE._make_predict_function()
            print("---> Age data set Loaded!!!")
        else:
            print("---> Couldn't find Age data set path")
            exit(1)

        if self.CASC_AGE is None:
            print("---> Must supply AGE classifier either through CASC_AGE!!!")
            exit(1)

        self._event_ready.set()

    def run(self):
        super(AgePredictionMD, self).run()
        print("[MODULE::AGE_PREDICTION]: run()")

        self.processor.start()

    def stop(self):
        super(AgePredictionMD, self).stop()

        self.processor.stop()

    def do_process(self, data):
        super(AgePredictionMD, self).do_process(data)
        return self.processor.process(data)

    def print_debug(self, data):
        super(AgePredictionMD, self).print_debug(data)
        return

    def print_log(self, data):
        super(AgePredictionMD, self).print_log(data)
        return
