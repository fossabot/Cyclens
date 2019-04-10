# coding: utf-8

from __future__ import unicode_literals

from ...common.module import Module

import threading

import cv2
from os.path import isfile

from .processor import ActionRecognitionPROC

class ActionRecognitionMD(Module):

    def __init__(self, ready=None):
        super(ActionRecognitionMD, self).__init__(ready)
        print("[MODULE::ACTION_RECOGNITION]: __init__")

        _ready = threading.Event()

        _ready.clear()
        self.processor = ActionRecognitionPROC(self, _ready)
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
        super(ActionRecognitionMD, self).run()
        print("[MODULE::ACTION_RECOGNITION]: run()")

        self.processor.start()

    def stop(self):
        super(ActionRecognitionMD, self).stop()

        self.processor.stop()

    def do_process(self, data):
        super(ActionRecognitionMD, self).do_process(data)
        print("[MODULE::ACTION_RECOGNITION::DO_PROCESS]:")

        print("[MODULE::ACTION_RECOGNITION::PIPELINE]: Sending to PROCESS Pipe")
        print("[MODULE::ACTION_RECOGNITION::PROCESS]: [START]")
        data = self.processor.process(data)
        print("[MODULE::ACTION_RECOGNITION::PROCESS]: [END] - Result: {}".format(data))

        return data

    def print_debug(self, data):
        super(ActionRecognitionMD, self).print_debug(data)
        return

    def print_log(self, data):
        super(ActionRecognitionMD, self).print_log(data)
        return
