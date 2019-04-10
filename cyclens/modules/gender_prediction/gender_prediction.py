# coding: utf-8

from __future__ import unicode_literals

from ...common.module import Module

import threading
import time

from .processor import GenderPredictionPROC

import cv2
import keras
from keras.models import load_model
from os.path import isfile


class GenderPredictionMD(Module):

    def __init__(self, ready=None):
        super(GenderPredictionMD, self).__init__(ready)
        print("[MODULE::GENDER_PREDICTION]: __init__")

        _ready = threading.Event()

        _ready.clear()
        self.processor = GenderPredictionPROC(self, _ready)
        _ready.wait()

        #keras.backend.clear_session()

        self.CASC_FACE = None
        self.CASC_GENDER = None

        self.GENDERS = {0: 'WOMAN', 1: 'MAN'}

        detection_model_path = '../data/models/detection/haarcascade_frontalface_default.xml'
        gender_model_path = '../data/models/gender/simple_CNN.81-0.96.hdf5'

        if isfile(detection_model_path):
            self.CASC_FACE = cv2.CascadeClassifier(detection_model_path)
            print("---> Face detection data set Loaded!!!")
        else:
            print("---> Couldn't find cascade model")
            exit(1)

        if isfile(gender_model_path):
            self.CASC_GENDER = load_model(gender_model_path, compile=False)
            self.CASC_GENDER._make_predict_function()
            self.gender_target_size = self.CASC_GENDER.input_shape[1:3]
            print("---> Gender data set Loaded!!!")
        else:
            print("---> Couldn't find Gender data set path")
            exit(1)

        self._event_ready.set()

    def run(self):
        super(GenderPredictionMD, self).run()
        print("[MODULE::GENDER_PREDICTION]: run()")

        self.processor.start()

    def stop(self):
        super(GenderPredictionMD, self).stop()

        self.processor.stop()

    def do_process(self, data):
        super(GenderPredictionMD, self).do_process(data)
        print("[MODULE::GENDER_PREDICTION::DO_PROCESS]:")

        print("[MODULE::GENDER_PREDICTION::PIPELINE]: Sending to PROCESS Pipe")
        print("[MODULE::GENDER_PREDICTION::PROCESS]: [START]")
        data = self.processor.process(data)
        print("[MODULE::GENDER_PREDICTION::PROCESS]: [END] - Result: {}".format(data))

        return data

    def print_debug(self, data):
        super(GenderPredictionMD, self).print_debug(data)
        return

    def print_log(self, data):
        super(GenderPredictionMD, self).print_log(data)
        return
