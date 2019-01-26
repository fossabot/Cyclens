#!/usr/bin/env python
# coding: utf-8

import multiprocessing
import threading
import time
import subprocess

from .modules import get_module
from .constants import __version__
from .server import ApiServer

from .modules.action_recognition.action_recognition import ActionRecognitionMD
from .modules.age_prediction.age_prediction import AgePredictionMD
from .modules.emotion_recognition.emotion_recognition import EmotionRecognitionMD
from .modules.face_dedection.face_dedection import FaceDedectionMD
from .modules.gender_prediction.gender_prediction import GenderPredictionMD

from .utils import (
    PreProcessingError,
    ProcessingError,
    PostProcessingError,
)

class Cyclens(object):
    """Cyclens class.


    Really...


    Available options:

    help:               Show help
    version:            Show version

    """

    params = None

    def __init__(self, params=None, auto_init=True):

        if params is None:
            params = {}

        print('[CYCLENS::__init__]')

    @classmethod
    def on_data_received(self, data):
        self.module_ar.on_data_received(data)
        self.module_ap.on_data_received(data)
        self.module_er.on_data_received(data)
        self.module_fd.on_data_received(data)
        self.module_gp.on_data_received(data)

    @classmethod
    def run(self):
        print('\n[CYCLENS::run()]: ===== INITIALIZING API =====')
        self.api = ApiServer()
        self.api.start()
        #TODO: Api nin baslamasini bekle
        #Api ye istek gidince Queue ye at
        #Ana dongude surekli queue bos mu kontrolu yap
        #Eger bos degilse on_data_received'e istegi gonder
        print('[CYCLENS::run()]: ==============================')

        print('\n[CYCLENS::run()]: ===== INITIALIZING SUB-MODULES =====')
        #self.module_x = get_module("ActionRecognition")
        self.module_ar = ActionRecognitionMD()
        self.module_ap = AgePredictionMD()
        self.module_er = EmotionRecognitionMD()
        self.module_fd = FaceDedectionMD()
        self.module_gp = GenderPredictionMD()
        print('[CYCLENS::run()]: ======================================')

        print('\n[CYCLENS::run()]: RUNNING ASYNC TORNADO WSGI SERVER')
        print('\n[CYCLENS::run()]: Waiting API requests for \'/api/test\' on port 5000 ...')

        while self.api.is_running():
            curr = self.api.get_from_queue()
            if curr is not None:
                self.on_data_received(curr)

            time.sleep(0.01)

        print('[CYCLENS::run()]: ============================================')

        print('')

    def __del__(self):
        print('[CYCLENS::__del__]')

    def __enter__(self):
        print('[CYCLENS::__enter__]')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        #raise PostProcessingError('Command returned error code %d' % 3)
        print('[CYCLENS::__exit__]')
