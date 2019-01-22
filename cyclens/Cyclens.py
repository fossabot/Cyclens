#!/usr/bin/env python
# coding: utf-8

import multiprocessing
import threading
import subprocess

from .modules import get_module
from .constants import __version__

from .server import api

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

    module_ar = None
    module_ap = None
    module_er = None
    module_fd = None
    module_gp = None

    def __init__(self, params=None, auto_init=True):

        if params is None:
            params = {}

        print('[CYCLENS::__init__]')

    @classmethod
    def on_data_received(self, data):
        self.module_ar.on_data_received(self, data)
        self.module_ap.on_data_received(self, data)
        self.module_er.on_data_received(self, data)
        self.module_fd.on_data_received(self, data)
        self.module_gp.on_data_received(self, data)
        return

    @classmethod
    def run(self):
        print('\n[CYCLENS::run()]: ===== INITIALIZING SUB-MODULES =====')
        self.module_ar = get_module("ActionRecognition")
        self.module_ap = get_module("AgePrediction")
        self.module_er = get_module("EmotionRecognition")
        self.module_fd = get_module("FaceDedection")
        self.module_gp = get_module("GenderPrediction")

        self.module_ar.__init__(self)
        self.module_ap.__init__(self)
        self.module_er.__init__(self)
        self.module_fd.__init__(self)
        self.module_gp.__init__(self)

        print('[CYCLENS::run()]: ====================================')

        print('\n[CYCLENS::run()]: ===== RUNNING SERVERS AS SUB-PROCESSES =====')
        tAR = threading.Thread(name='[CYCLENS::AR]', target=self.module_ar.run(self))
        tAP = threading.Thread(name='[CYCLENS::AP]', target=self.module_ap.run(self))
        tER = threading.Thread(name='[CYCLENS::ER]', target=self.module_er.run(self))
        tFD = threading.Thread(name='[CYCLENS::FD]', target=self.module_fd.run(self))
        tGP = threading.Thread(name='[CYCLENS::GP]', target=self.module_gp.run(self))

        tAR.start()
        tAP.start()
        tER.start()
        tFD.start()
        tGP.start()

        print('[CYCLENS::run()]: ============================================')

        print('\n[CYCLENS::run()]: ===== SENDING DATA TO MODULES FOR PROCESS =====')

        self.on_data_received("example_data_to_async_process")

        print('[CYCLENS::run()]: ===============================================')
        print('')

    def __del__(self):
        print('[CYCLENS::__del__]')

    def __enter__(self):
        print('[CYCLENS::__enter__]')
        return self

    def __exit__(self, exc_type, exc_value, traceback):
        #raise PostProcessingError('Command returned error code %d' % 3)
        print('[CYCLENS::__exit__]')
