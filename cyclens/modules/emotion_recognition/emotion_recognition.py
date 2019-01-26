# coding: utf-8

from __future__ import unicode_literals

from ...common.module import Module

from multiprocessing import Process, Queue

import threading
import time

from .preprocessor import EmotionRecognitionPREP
from .processor import EmotionRecognitionPROC
from .postprocessor import EmotionRecognitionPOSP

class EmotionRecognitionMD(Module):

    def __init__(self, ready=None):
        super(EmotionRecognitionMD, self).__init__(ready)
        print("[MODULE::EMOTION_RECOGNITION]: __init__")

        self.prep = EmotionRecognitionPREP()
        self.proc = EmotionRecognitionPROC()
        self.posp = EmotionRecognitionPOSP()

        self._ready.set()

    def run(self):
        super(EmotionRecognitionMD, self).run()
        print("[MODULE::EMOTION_RECOGNITION]: run()")

        self.prep.start()
        self.proc.start()
        self.posp.start()

        while True:

            #Anti -> CPU GG WP EZ
            time.sleep(0.1)

            _ready = threading.Event()

            #1 PreProcess pipe
            if not self.prep.is_busy:
                data = self.dequeue()
                if data is not None:
                    print("[MODULE::EMOTION_RECOGNITION::PIPELINE]: Sending to PRE_PROCESS Pipe")

                    print("[MODULE::EMOTION_RECOGNITION::PRE_PROCESS]: [START] FOR DATA ---> {}".format(data))
                    _ready.clear()
                    dataPREP = self.prep.process(data, _ready)
                    _ready.wait()
                    print("[MODULE::EMOTION_RECOGNITION::PRE_PROCESS]: [END]")

                    #2 Process pipe
                    if not self.proc.is_busy:
                        if dataPREP is not None:
                            print("[MODULE::EMOTION_RECOGNITION::PIPELINE]: Sending to PROCESS Pipe")

                            print("[MODULE::EMOTION_RECOGNITION::PROCESS]: [START] FOR DATA ---> {}".format(data))
                            _ready.clear()
                            dataPROC = self.proc.process(dataPREP, _ready)
                            _ready.wait()
                            print("[MODULE::EMOTION_RECOGNITION::PROCESS]: [END]")

                            #3 PostProcess pipe
                            if not self.posp.is_busy:
                                if dataPROC is not None:
                                    print("[MODULE::EMOTION_RECOGNITION::PIPELINE]: Sending to POST_PROCESS Pipe")

                                    print("[MODULE::EMOTION_RECOGNITION::POSP_PROCESS]: [START] FOR DATA ---> {}".format(data))
                                    _ready.clear()
                                    dataPOSP = self.posp.process(dataPROC, _ready)
                                    _ready.wait()
                                    print("[MODULE::EMOTION_RECOGNITION::POSP_PROCESS]: [END]")

                                    if dataPOSP is not None:
                                        print("[MODULE::EMOTION_RECOGNITION::RESULT]: Final data {}".format(dataPOSP))

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
