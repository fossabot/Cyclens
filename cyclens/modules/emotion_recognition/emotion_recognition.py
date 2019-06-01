# coding: utf-8

from __future__ import unicode_literals

from ...common.module import Module
from ...common.paths import PATH_MODEL_EMOTION

from .processor import EmotionRecognitionPROC

from keras.models import load_model
from os.path import isfile

import threading


class EmotionRecognitionMD(Module):

    def __init__(self, ready=None):
        super(EmotionRecognitionMD, self).__init__(ready)

        self.module_id = 2
        self.module_name = 'emotion_recognition'

        _ready = threading.Event()

        _ready.clear()
        self.processor = EmotionRecognitionPROC(self, _ready)
        _ready.wait()

        self.CASC_EMOTION = None

        self.EMOTIONS = {0: 'ANGRY', 1: 'DISGUST', 2: 'FEAR', 3: 'HAPPY', 4: 'SAD', 5: 'SURPRISE', 6: 'NEUTRAL'}

        if isfile(PATH_MODEL_EMOTION):
            self.CASC_EMOTION = load_model(PATH_MODEL_EMOTION, compile=False)
            self.CASC_EMOTION._make_predict_function()
            self.emotion_target_size = self.CASC_EMOTION.input_shape[1:3]
            print("---> Emotion data set Loaded!!!")
        else:
            print("---> Couldn't find Emotion data set path")
            exit(1)

        if self.CASC_EMOTION is None:
            print("---> Must supply EMOTION classifier either through CASC_EMOTION!!!")
            exit(1)

        self._event_ready.set()

    def run(self):
        super(EmotionRecognitionMD, self).run()
        print("[MODULE::EMOTION_RECOGNITION]: run()")

        self.processor.start()

    def stop(self):
        super(EmotionRecognitionMD, self).stop()

        self.processor.stop()

    async def do_process(self, data):
        super(EmotionRecognitionMD, self).do_process(data)
        return self.processor.process(data)

    def print_debug(self, data):
        super(EmotionRecognitionMD, self).print_debug(data)
        return

    def print_log(self, data):
        super(EmotionRecognitionMD, self).print_log(data)
        return
