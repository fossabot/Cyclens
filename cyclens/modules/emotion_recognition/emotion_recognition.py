# coding: utf-8

from __future__ import unicode_literals

from ...common.module import Module

import threading

from .processor import EmotionRecognitionPROC

import cv2
from keras.models import load_model
from os.path import isfile


class EmotionRecognitionMD(Module):

    def __init__(self, ready=None):
        super(EmotionRecognitionMD, self).__init__(ready)

        self.module_id = 2
        self.module_name = 'emotion_recognition'

        _ready = threading.Event()

        _ready.clear()
        self.processor = EmotionRecognitionPROC(self, _ready)
        _ready.wait()

        self.CASC_FACE = None
        self.CASC_EMOTION = None

        self.EMOTIONS = {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'sad', 5: 'surprise', 6: 'neutral'}

        detection_model_path = '../data/models/detection/haarcascade_frontalface_default.xml'
        emotion_model_path = '../data/models/emotion/fer2013_mini_XCEPTION.102-0.66.hdf5'

        if isfile(detection_model_path):
            self.CASC_FACE = cv2.CascadeClassifier(detection_model_path)
            print("---> Face detection data set Loaded!!!")
        else:
            print("---> Couldn't find cascade model")
            exit(1)

        if isfile(emotion_model_path):
            self.CASC_EMOTION = load_model(emotion_model_path, compile=False)
            self.CASC_EMOTION._make_predict_function()
            self.emotion_target_size = self.CASC_EMOTION.input_shape[1:3]
            print("---> Emotion data set Loaded!!!")
        else:
            print("---> Couldn't find Emotion data set path")
            exit(1)

        self._event_ready.set()

    def run(self):
        super(EmotionRecognitionMD, self).run()
        print("[MODULE::EMOTION_RECOGNITION]: run()")

        self.processor.start()

    def stop(self):
        super(EmotionRecognitionMD, self).stop()

        self.processor.stop()

    def do_process(self, data):
        super(EmotionRecognitionMD, self).do_process(data)
        print("[MODULE::EMOTICON_RECOGNITION::DO_PROCESS]:")

        print("[MODULE::EMOTION_RECOGNITION::PIPELINE]: Sending to PROCESS Pipe")
        print("[MODULE::EMOTION_RECOGNITION::PROCESS]: [START]")
        data = self.processor.process(data)
        print("[MODULE::EMOTION_RECOGNITION::PROCESS]: [END] - Result: {}".format(data))

        return data

    def print_debug(self, data):
        super(EmotionRecognitionMD, self).print_debug(data)
        return

    def print_log(self, data):
        super(EmotionRecognitionMD, self).print_log(data)
        return
