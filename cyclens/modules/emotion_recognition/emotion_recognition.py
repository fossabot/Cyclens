# coding: utf-8

from __future__ import unicode_literals

from ...common.module import Module

from multiprocessing import Process, Queue

from .preprocessor import EmotionRecognitionPREP
from .processor import EmotionRecognitionPROC
from .postprocessor import EmotionRecognitionPOSP

class EmotionRecognitionMD(Module):


    def __init__(self):
        Module.__init__(self)
        print("[MODULE::EMOTION_RECOGNITION]: __init__")

        self.process_queue = Queue()

        self.prep = EmotionRecognitionPREP()
        self.proc = EmotionRecognitionPROC()
        self.posp = EmotionRecognitionPOSP()


    def on_data_sent(self, data):
        print("data: " + data)
        return

    def run(self):
        print("[MODULE::EMOTION_RECOGNITION]: run()")

    def on_data_received(self, data):
        return
        #return super(self, EmotionRecognitionMD).on_data_received(data)

    def on_data_sent(self, data):
        return

    def enqueue(self, data):
        return

    def dequeue(self, data):
        return

    def post_to_preprocessor(self, data):
        return

    def post_to_processor(self, data):
        return

    def post_to_postprocessor(self, data):
        return

    def print_debug(self, data):
        return

    def print_log(self, data):
        return
