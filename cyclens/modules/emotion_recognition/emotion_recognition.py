# coding: utf-8

from __future__ import unicode_literals

from ...common.module import Module

from multiprocessing import Process, Queue

from .preprocessor import EmotionRecognitionPREP
from .processor import EmotionRecognitionPROC
from .postprocessor import EmotionRecognitionPOSP

class EmotionRecognitionMD(Module):


    def __init__(self):
        super(EmotionRecognitionMD, self).__init__()
        print("[MODULE::EMOTION_RECOGNITION]: __init__")

        self.prep = EmotionRecognitionPREP()
        self.proc = EmotionRecognitionPROC()
        self.posp = EmotionRecognitionPOSP()

    def run(self):
        super(EmotionRecognitionMD, self).run()
        print("[MODULE::EMOTION_RECOGNITION]: run()")
        while True:
            print(self.dequeue())
            return
            if not self.process_queue.empty():
                item = self.process_queue.get_nowait()
                print(item)

    def on_data_received(self, data):
        super(EmotionRecognitionMD, self).on_data_received(data)
        print("[MODULE::EMOTICON_RECOGNATION::ON_DATA_RECEIVED]:")
        print(data)

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
