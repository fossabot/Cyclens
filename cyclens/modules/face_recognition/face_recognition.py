# coding: utf-8

from __future__ import unicode_literals

from ...common.module import Module

import threading

import cv2
from os.path import isfile

from .processor import FaceRecognitionPROC


class FaceRecognitionMD(Module):

    def __init__(self, ready=None):
        super(FaceRecognitionMD, self).__init__(ready)
        print("[MODULE::FACE_RECOGNITION]: __init__")

        _ready = threading.Event()

        _ready.clear()
        self.processor = FaceRecognitionPROC(self, _ready)
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
        super(FaceRecognitionMD, self).run()
        print("[MODULE::FACE_RECOGNITION]: run()")

        self.processor.start()

    def stop(self):
        super(FaceRecognitionMD, self).stop()

        self.processor.stop()

    def do_process(self, data):
        super(FaceRecognitionMD, self).do_process(data)
        print("[MODULE::FACE_RECOGNITION::DO_PROCESS]:")

        print("[MODULE::FACE_RECOGNITION::PIPELINE]: Sending to PROCESS Pipe")
        print("[MODULE::FACE_RECOGNITION::PROCESS]: [START]")
        data = self.processor.process(data)
        print("[MODULE::FACE_RECOGNITION::PROCESS]: [END] - Result: {}".format(data))

        return data

    def print_debug(self, data):
        super(FaceRecognitionMD, self).print_debug(data)
        return

    def print_log(self, data):
        super(FaceRecognitionMD, self).print_log(data)
        return
