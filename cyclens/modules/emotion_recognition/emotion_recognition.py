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
import numpy as np
import tflearn
import tensorflow as tf
from tflearn.layers.core import input_data, dropout, fully_connected, flatten
from tflearn.layers.conv import conv_2d, max_pool_2d, avg_pool_2d
from tflearn.layers.merge_ops import merge
from tflearn.layers.normalization import local_response_normalization
from tflearn.layers.estimator import regression
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

        self.target_classes = ['angry', 'disgusted', 'fearful', 'happy', 'sad', 'surprised', 'neutral']

        self.network = input_data(shape=[None, 48, 48, 1])
        self.network = conv_2d(self.network, 64, 5, activation='relu')
        self.network = max_pool_2d(self.network, 3, strides=2)
        self.network = conv_2d(self.network, 64, 5, activation='relu')
        self.network = max_pool_2d(self.network, 3, strides=2)
        self.network = conv_2d(self.network, 128, 4, activation='relu')
        self.network = dropout(self.network, 0.3)
        self.network = fully_connected(self.network, 3072, activation = 'relu')
        self.network = fully_connected(self.network, len(self.target_classes), activation='softmax')
        self.network = regression(self.network, optimizer='momentum', metric='accuracy', loss='categorical_crossentropy')
        self.model = tflearn.DNN(self.network, checkpoint_path='model_1_atul', max_checkpoints=1, tensorboard_verbose=2)

        os.chdir("data/models/")
        if isfile("model_1_atul.tflearn.meta"):
            self.model.load("model_1_atul.tflearn")
        else:
            print("---> Couldn't find model")

        self._event_ready.set()

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
