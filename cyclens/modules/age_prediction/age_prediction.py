# coding: utf-8

from __future__ import unicode_literals

from ...common.module import Module

import threading

import cv2
from os.path import isfile

from .processor import AgePredictionPROC


class AgePredictionMD(Module):

    def __init__(self, ready=None):
        super(AgePredictionMD, self).__init__(ready)
        print("[MODULE::AGE_PREDICTION]: __init__")

        _ready = threading.Event()

        _ready.clear()
        self.processor = AgePredictionPROC(self, _ready)
        _ready.wait()

        self.CASC_FACE = None

        detection_model_path = '../data/models/detection/haarcascade_frontalface_default.xml'

        if isfile(detection_model_path):
            self.CASC_FACE = cv2.CascadeClassifier(detection_model_path)
            print("---> Face detection data set Loaded!!!")
        else:
            print("---> Couldn't find cascade model")
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
        print("[MODULE::AGE_PREDICTION::DO_PROCESS]:")

        print("[MODULE::AGE_PREDICTION::PIPELINE]: Sending to PROCESS Pipe")
        print("[MODULE::AGE_PREDICTION::PROCESS]: [START]")
        data = self.processor.process(data)
        print("[MODULE::AGE_PREDICTION::PROCESS]: [END] - Result: {}".format(data))

        return data

    def print_debug(self, data):
        super(AgePredictionMD, self).print_debug(data)
        return

    def print_log(self, data):
        super(AgePredictionMD, self).print_log(data)
        return
