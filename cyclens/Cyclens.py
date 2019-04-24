#!/usr/bin/env python
# coding: utf-8

import threading
import logging
import time
import keras
import sys
import os
import signal

from datetime import datetime

import tensorflow as tf

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
        print('[CYCLENS::__init__]')

        if params is None:
            params = {}

        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        tf.get_logger().setLevel(logging.ERROR)
        tf.logging.set_verbosity(tf.logging.ERROR)

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
    def print_banner(self):
        print('''
 ██████╗██╗   ██╗ ██████╗██╗     ███████╗███╗   ██╗███████╗
██╔════╝╚██╗ ██╔╝██╔════╝██║     ██╔════╝████╗  ██║██╔════╝
██║      ╚████╔╝ ██║     ██║     █████╗  ██╔██╗ ██║███████╗
██║       ╚██╔╝  ██║     ██║     ██╔══╝  ██║╚██╗██║╚════██║
╚██████╗   ██║   ╚██████╗███████╗███████╗██║ ╚████║███████║
 ╚═════╝   ╚═╝    ╚═════╝╚══════╝╚══════╝╚═╝  ╚═══╝╚══════╝                                                  
        ''')

    @classmethod
    def print_boot_time(self, date_start, date_end):
        time_boot = round((date_end - date_start).total_seconds() * 1000, 2)
        print('---> Boot time: {} ms'.format(time_boot))

    @classmethod
    def run(self):
        self.print_banner()

        print()

        print('\n[CYCLENS::run()]: ===== INITIALIZING MODULES =====')

        keras.backend.clear_session()

        _ready = threading.Event()

        print('\n> Booting: Action Recognition')
        date_start = datetime.now()
        _ready.clear()
        self.module_ar = ActionRecognitionMD(_ready)
        self.module_ar.daemon = True
        _ready.wait()
        date_end = datetime.now()
        self.print_boot_time(date_start, date_end)

        print('\n> Booting: Age Prediction')
        date_start = datetime.now()
        _ready.clear()
        self.module_ap = AgePredictionMD(_ready)
        self.module_ap.daemon = True
        _ready.wait()
        date_end = datetime.now()
        self.print_boot_time(date_start, date_end)

        print('\n> Booting: Emotion Recognition')
        date_start = datetime.now()
        _ready.clear()
        self.module_er = EmotionRecognitionMD(_ready)
        self.module_er.daemon = True
        _ready.wait()
        date_end = datetime.now()
        self.print_boot_time(date_start, date_end)

        print('\n> Booting: Face Recognition')
        date_start = datetime.now()
        _ready.clear()
        self.module_fr = FaceRecognitionMD(_ready)
        self.module_fr.daemon = True
        _ready.wait()
        date_end = datetime.now()
        self.print_boot_time(date_start, date_end)

        print('\n> Booting: Gender Prediction')
        date_start = datetime.now()
        _ready.clear()
        self.module_gp = GenderPredictionMD(_ready)
        self.module_gp.daemon = True
        _ready.wait()
        date_end = datetime.now()
        self.print_boot_time(date_start, date_end)

        print('\n[CYCLENS::run()]: ===== RUNNING MODULES =====')
        print()

        self.module_ar.start()
        self.module_ap.start()
        self.module_er.start()
        self.module_fr.start()
        self.module_gp.start()

        print('\n[CYCLENS::run()]: ===== INITIALIZING API =====')
        print('> Booting: Flask API')
        date_start = datetime.now()
        _ready.clear()
        self.api = ApiServer(self, _ready)
        self.api.daemon = True
        _ready.wait()
        date_end = datetime.now()
        self.print_boot_time(date_start, date_end)
        self.api.start()
        print()
        print('[CYCLENS::run()]: ==============================')

        print('\n[CYCLENS::run()]: RUNNING ASYNC TORNADO WSGI SERVER')
        print('\n[CYCLENS::run()]: Waiting API requests for \'/api/v1/demo/...\' on \'{}:{}\' ...'.format(self.api.HOST, self.api.PORT))

        # API'ye istek yapıldı mı sürekli kontrol et
        try:
            signal.pause()
        except:
            pass

        # while self.api.is_running():
        # time.sleep(0.1)

        print()
        print('[CYCLENS::run()]: ==============================')
        print()

    @classmethod
    def stop(self):
        self.api.stop()

        self.module_ar.stop()
        self.module_ap.stop()
        self.module_er.stop()
        self.module_fr.stop()
        self.module_gp.stop()

    def __del__(self):
        # print('[CYCLENS::__del__]')
        # sys.exit()
        pass

    def __enter__(self):
        print('[CYCLENS::__enter__]')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print('[CYCLENS::__exit__()]: ===== SHUTTING DOWN =====')
        print()
        self.stop()
