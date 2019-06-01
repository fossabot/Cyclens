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
import json
import copy

from .common.preprocessor import PreProcessor, get_date_now, get_date_str
from .common.postprocessor import PostProcessor
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

        os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
        tf.get_logger().setLevel(logging.ERROR)
        tf.logging.set_verbosity(tf.logging.ERROR)

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

        self.pre_processor = PreProcessor()
        pre_loaded = self.pre_processor.try_load()

        if not pre_loaded:
            print('\n> PreProcessor: Unable to load cascade classifier!')
            exit(1)

        self.post_processor = PostProcessor()
        self.post_processor.try_load()

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
    def process(self, img, ar, ap, er, fr, gp):

        date_start = get_date_now()

        result = {'success': True, 'message': 'null', 'process': {'start': get_date_str(date_start), 'end': 0, 'total': 0}, 'modules': []}

        print('\n[API Request at: {}] ======================================================================================'.format(get_date_str(date_start)))

        if ar is False and ap is False and er is False and fr is False and gp is False:

            result['success'] = False
            result['message'] = 'No modules are selected to be processed'

        else:

            # try:

            data = self.pre_processor.process(img)

            if data['success'] is True and data['found'] > 0:

                if ar is True:
                    data['module'] = 'action_recognition'

                    proc_ar = self.module_ar.do_process(copy.deepcopy(data))
                    proc_ar_post = self.post_processor.process(self.module_ar, proc_ar)
                    proc_data_ar = json.loads(proc_ar_post)

                    result['modules'].append(proc_data_ar)

                    print('[MODULE::ACTION_RECOGNITION::RESULT]: {}'.format(proc_data_ar))

                if ap is True:
                    data['module'] = 'age_prediction'

                    proc_ap = self.module_ap.do_process(copy.deepcopy(data))
                    proc_ap_post = self.post_processor.process(self.module_ap, proc_ap)
                    proc_data_ap = json.loads(proc_ap_post)

                    result['modules'].append(proc_data_ap)

                    print('[MODULE::AGE_PREDICTION::RESULT]: {}'.format(proc_data_ap))

                if er is True:
                    data['module'] = 'emotion_recognition'

                    proc_er = self.module_er.do_process(copy.deepcopy(data))
                    proc_er_post = self.post_processor.process(self.module_er, proc_er)
                    proc_data_er = json.loads(proc_er_post)

                    result['modules'].append(proc_data_er)

                    print('[MODULE::EMOTION_RECOGNITION::RESULT]: {}'.format(proc_data_er))

                if fr is True:
                    data['module'] = 'face_recognition'

                    proc_fr = self.module_fr.do_process(copy.deepcopy(data))
                    proc_fr_post = self.post_processor.process(self.module_fr, proc_fr)
                    proc_data_fr = json.loads(proc_fr_post)

                    result['modules'].append(proc_data_fr)

                    print('[MODULE::FACE_RECOGNITION::RESULT]: {}'.format(proc_data_fr))

                if gp is True:
                    data['module'] = 'gender_prediction'

                    proc_gp = self.module_gp.do_process(copy.deepcopy(data))
                    proc_gp_post = self.post_processor.process(self.module_gp, proc_gp)
                    proc_data_gp = json.loads(proc_gp_post)

                    result['modules'].append(proc_data_gp)

                    print('[MODULE::GENDER_PREDICTION::RESULT]: {}'.format(proc_data_gp))

            else:
                result['success'] = data['success']
                result['message'] = data['message']

            # except:
            #    result['success'] = False
            #    result['message'] = 'API TRY-EXCEPT!!!'

        date_end = get_date_now()

        ms_diff = (date_end - date_start).total_seconds() * 1000

        result['process']['end'] = get_date_str(date_end)
        result['process']['total'] = round(ms_diff, 2)

        print('[Elapsed time: {}] ============================================================================================================='.format(result['process']['total']))

        return result

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
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        print('[CYCLENS::__exit__()]: ===== SHUTTING DOWN =====')
        print()
        self.stop()
