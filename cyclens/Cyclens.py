#!/usr/bin/env python
# coding: utf-8

"""
cyclens
~~~~~~~

Implements root Cyclens class.

This program comes with ABSOLUTELY NO WARRANTY; This is free software,
and you are welcome to redistribute it under certain conditions; See
file LICENSE, which is part of this source code package, for details.

:copyright: Copyright © 2019, The Cyclens Project
:license: MIT, see LICENSE for more details.
"""

import threading
import logging
import keras
import os
import signal

from datetime import datetime

import copy
import asyncio
import nest_asyncio
import tensorflow as tf

from .server import ApiServer
from .common.preprocessor import PreProcessor, get_date_now, get_date_str
from .common.postprocessor import PostProcessor
from .modules.action_recognition.action_recognition import ActionRecognitionMD
from .modules.age_prediction.age_prediction import AgePredictionMD
from .modules.emotion_recognition.emotion_recognition import EmotionRecognitionMD
from .modules.face_recognition.face_recognition import FaceRecognitionMD
from .modules.gender_prediction.gender_prediction import GenderPredictionMD


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
        nest_asyncio.apply()

        _ready = threading.Event()

        self.pre_processor = PreProcessor()
        pre_loaded = self.pre_processor.try_load()

        if not pre_loaded:
            print('\n> PreProcessor: Unable to load cascade classifier!')
            exit(1)

        print('\n> Booting: Action Recognition')
        date_start = datetime.now()
        _ready.clear()
        self.module_ar = ActionRecognitionMD(_ready)
        _ready.wait()
        date_end = datetime.now()
        self.print_boot_time(date_start, date_end)

        print('\n> Booting: Age Prediction')
        date_start = datetime.now()
        _ready.clear()
        self.module_ap = AgePredictionMD(_ready)
        _ready.wait()
        date_end = datetime.now()
        self.print_boot_time(date_start, date_end)

        print('\n> Booting: Emotion Recognition')
        date_start = datetime.now()
        _ready.clear()
        self.module_er = EmotionRecognitionMD(_ready)
        _ready.wait()
        date_end = datetime.now()
        self.print_boot_time(date_start, date_end)

        print('\n> Booting: Face Recognition')
        date_start = datetime.now()
        _ready.clear()
        self.module_fr = FaceRecognitionMD(_ready)
        _ready.wait()
        date_end = datetime.now()
        self.print_boot_time(date_start, date_end)

        print('\n> Booting: Gender Prediction')
        date_start = datetime.now()
        _ready.clear()
        self.module_gp = GenderPredictionMD(_ready)
        _ready.wait()
        date_end = datetime.now()
        self.print_boot_time(date_start, date_end)

        print('\n[CYCLENS::run()]: ===== RUNNING MODULES =====')
        print()

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

            if data['success'] and data['found'] > 0:

                loop = asyncio.get_event_loop()

                tasks = []

                if ar is True:
                    proc_ar = loop.create_task(self.module_ar.do_process(copy.deepcopy(data)))
                    tasks.append(proc_ar)

                if ap is True:
                    proc_ap = loop.create_task(self.module_ap.do_process(copy.deepcopy(data)))
                    tasks.append(proc_ap)

                if er is True:
                    proc_er = loop.create_task(self.module_er.do_process(copy.deepcopy(data)))
                    tasks.append(proc_er)

                if fr is True:
                    proc_fr = loop.create_task(self.module_fr.do_process(copy.deepcopy(data)))
                    tasks.append(proc_fr)

                if gp is True:
                    proc_gp = loop.create_task(self.module_gp.do_process(copy.deepcopy(data)))
                    tasks.append(proc_gp)

                results, _ = loop.run_until_complete(asyncio.wait(tasks))

                for res in results:
                    r = res.result()
                    result['modules'].append(r)
                    print('[MODULE::{}::RESULT]: {}'.format(r['module'], r))

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

        print(result)

        print('[Elapsed time: {}] ============================================================================================================='.format(result['process']['total']))

        return result

    @classmethod
    def get_module_by_name(self, name):
        if name == "action_recognition":
            return self.module_ar
        elif name == "age_prediction":
            return  self.module_ap
        elif name == "emotion_recognition":
            return self.module_er
        elif name == "face_recognition":
            return self.module_fr
        elif name == "gender_prediction":
            return self.module_gp

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
