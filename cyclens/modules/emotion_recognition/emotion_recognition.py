# coding: utf-8

from __future__ import unicode_literals

from ...common.module import Module

from multiprocessing import Process, Queue

import threading
import time

from .preprocessor import EmotionRecognitionPREP
from .processor import EmotionRecognitionPROC
from .postprocessor import EmotionRecognitionPOSP

import os
import cv2
import numpy as np
import tensorflow as tf
import keras
from keras.models import load_model
from os.path import isfile, join
from os.path import dirname as up

class EmotionRecognitionMD(Module):

    def __init__(self, ready=None):
        super(EmotionRecognitionMD, self).__init__(ready)
        print("[MODULE::EMOTION_RECOGNITION]: __init__")

        _ready = threading.Event()

        _ready.clear()
        self.prep = EmotionRecognitionPREP(self, _ready)
        _ready.wait()

        _ready.clear()
        self.proc = EmotionRecognitionPROC(self, _ready)
        _ready.wait()

        _ready.clear()
        self.posp = EmotionRecognitionPOSP(self, _ready)
        _ready.wait()

        keras.backend.clear_session()

        self.CASC_FACE = None
        self.CASC_EMOTION = None

        self.EMOTIONS = ['angry', 'disgusted', 'fearful', 'happy', 'sad', 'surprised', 'neutral']

        detection_model_path = '../data/models/detection/haarcascade_frontalface_default.xml'
        emotion_model_path = '../data/models/emotion/fer2013_mini_XCEPTION.102-0.66.hdf5'

        self.emotion_labels = self.get_labels('fer2013')

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

    def get_labels(self, dataset_name):
        if dataset_name == 'fer2013':
            return {0: 'angry', 1: 'disgust', 2: 'fear', 3: 'happy', 4: 'sad', 5: 'surprise', 6: 'neutral'}
        elif dataset_name == 'imdb':
            return {0: 'woman', 1: 'man'}
        elif dataset_name == 'KDEF':
            return {0: 'AN', 1: 'DI', 2: 'AF', 3: 'HA', 4: 'SA', 5: 'SU', 6: 'NE'}
        else:
            raise Exception('Invalid dataset name')

    def run(self):
        super(EmotionRecognitionMD, self).run()
        print("[MODULE::EMOTION_RECOGNITION]: run()")

        self.prep.start()
        self.proc.start()
        self.posp.start()

        while self.is_running:

            #Anti -> CPU GG WP EZ
            time.sleep(0.1)

            _ready = threading.Event()

            #1 PreProcess pipe
            if not self.prep.is_busy:
                data = self.dequeue()
                if data is not None:
                    print("[MODULE::EMOTION_RECOGNITION::PIPELINE]: Sending to PRE_PROCESS Pipe")

                    print("[MODULE::EMOTION_RECOGNITION::PRE_PROCESS]: [START]")
                    _ready.clear()
                    dataPREP = self.prep.process(data, _ready)
                    _ready.wait()
                    print("[MODULE::EMOTION_RECOGNITION::PRE_PROCESS]: [END] - Result: {}".format(dataPREP))

                    #2 Process pipe
                    if not self.proc.is_busy:
                        if dataPREP is not None:
                            print("[MODULE::EMOTION_RECOGNITION::PIPELINE]: Sending to PROCESS Pipe")

                            print("[MODULE::EMOTION_RECOGNITION::PROCESS]: [START]")
                            _ready.clear()
                            dataPROC = self.proc.process(dataPREP, _ready)
                            _ready.wait()
                            print("[MODULE::EMOTION_RECOGNITION::PROCESS]: [END] - Result: {}".format(dataPROC))

                            #3 PostProcess pipe
                            if not self.posp.is_busy:
                                if dataPROC is not None:
                                    print("[MODULE::EMOTION_RECOGNITION::PIPELINE]: Sending to POST_PROCESS Pipe")

                                    print("[MODULE::EMOTION_RECOGNITION::POSP_PROCESS]: [START]")
                                    _ready.clear()
                                    dataPOSP = self.posp.process(dataPROC, _ready)
                                    _ready.wait()
                                    print("[MODULE::EMOTION_RECOGNITION::POSP_PROCESS]: [END] - Result: {}".format(dataPOSP))

                                    if dataPOSP is not None:
                                        print("[MODULE::EMOTION_RECOGNITION::RESULT]: Final data {}".format(dataPOSP))

    def stop(self):
        super(EmotionRecognitionMD, self).stop()

        self.prep.stop()
        self.proc.stop()
        self.posp.stop()

    def on_data_received(self, data):
        super(EmotionRecognitionMD, self).on_data_received(data)
        print("[MODULE::EMOTICON_RECOGNATION::ON_DATA_RECEIVED]:")

    def on_data_sent(self, data):
        super(EmotionRecognitionMD, self).on_data_sent(data)
        print("data: " + data)

    def post_to_preprocessor(self, data):
        return

    def post_to_processor(self, data):
        return

    def post_to_postprocessor(self, data):
        return

    def print_debug(self, data):
        super(EmotionRecognitionMD, self).print_debug(data)
        return

    def print_log(self, data):
        super(EmotionRecognitionMD, self).print_log(data)
        return
