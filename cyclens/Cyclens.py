#!/usr/bin/env python
# coding: utf-8

import threading
import time
import keras
import sys

from .modules import get_module
from .constants import __version__
from .server import ApiServer

from .modules.action_recognition.action_recognition import ActionRecognitionMD
from .modules.age_prediction.age_prediction import AgePredictionMD
from .modules.emotion_recognition.emotion_recognition import EmotionRecognitionMD
from .modules.face_recognition.face_recognition import FaceRecognitionMD
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

    # Her modülün içerisindeki fonksiyon çağırılır ve parametre olarak API request gönderilir
    # TODO: Burası Async olacak?
    @classmethod
    def on_data_received(self, data):
        self.module_ar.on_data_received(data)
        self.module_ap.on_data_received(data)
        self.module_er.on_data_received(data)
        self.module_fr.on_data_received(data)
        self.module_gp.on_data_received(data)

    @classmethod
    def run(self):
        print('\n[CYCLENS::run()]: ===== INITIALIZING API =====')
        self.api = ApiServer(self)
        self.api.start()
        print('[CYCLENS::run()]: ==============================')

        print('\n[CYCLENS::run()]: ===== INITIALIZING SUB-MODULES =====')

        keras.backend.clear_session()

        _ready = threading.Event()

        _ready.clear()
        self.module_ar = ActionRecognitionMD(_ready)
        _ready.wait()

        _ready.clear()
        self.module_ap = AgePredictionMD(_ready)
        _ready.wait()

        _ready.clear()
        self.module_er = EmotionRecognitionMD(_ready)
        _ready.wait()

        _ready.clear()
        self.module_fr = FaceRecognitionMD(_ready)
        _ready.wait()

        _ready.clear()
        self.module_gp = GenderPredictionMD(_ready)
        _ready.wait()

        print('[CYCLENS::run()]: ======================================')

        print('\n[CYCLENS::run()]: ===== RUNNING SUB-MODULES =====')
        self.module_ar.start()
        self.module_ap.start()
        self.module_er.start()
        self.module_fr.start()
        self.module_gp.start()
        print('[CYCLENS::run()]: =================================')

        print('\n[CYCLENS::run()]: RUNNING ASYNC TORNADO WSGI SERVER')
        print('\n[CYCLENS::run()]: Waiting API requests for \'/api/v1/demo\' on port 5000 ...')

        # API'ye istek yapıldı mı sürekli kontrol et
        # eğer yapılmış ise 'on_data_received' fonksiyonunu çalıştır
        while self.api.is_running():
            time.sleep(0.01)

        print('[CYCLENS::run()]: ============================================')

        print('')

    @classmethod
    def stop(self):
        self.module_ar.stop()
        self.module_ap.stop()
        self.module_er.stop()
        self.module_fr.stop()
        self.module_gp.stop()

    def __del__(self):
        print('[CYCLENS::__del__]')
        sys.exit()

    def __enter__(self):
        print('[CYCLENS::__enter__]')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print('[CYCLENS::__exit__]')
        self.stop()
