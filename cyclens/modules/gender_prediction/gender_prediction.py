# coding: utf-8

"""
cyclens.modules.gender_prediction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implements 'GENDER PREDICTION' module

This program comes with ABSOLUTELY NO WARRANTY; This is free software,
and you are welcome to redistribute it under certain conditions; See
file LICENSE, which is part of this source code package, for details.

:copyright: Copyright © 2019, The Cyclens Project
:license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals

import threading

from keras.models import load_model
from os.path import isfile

from .processor import GenderPredictionPROC
from ...common.paths import PATH_MODEL_GENDER
from ...common.module import Module


class GenderPredictionMD(Module):

    def __init__(self, ready=None):
        super(GenderPredictionMD, self).__init__(ready)

        self.module_id = 4
        self.module_name = 'gender_prediction'

        _ready = threading.Event()

        _ready.clear()
        self.processor = GenderPredictionPROC(self, _ready)
        _ready.wait()

        #keras.backend.clear_session()

        self.CASC_GENDER = None

        self.GENDERS = {0: 'WOMAN', 1: 'MAN'}

        if isfile(PATH_MODEL_GENDER):
            self.CASC_GENDER = load_model(PATH_MODEL_GENDER, compile=False)
            self.CASC_GENDER._make_predict_function()
            self.gender_target_size = self.CASC_GENDER.input_shape[1:3]
            print("---> Gender data set Loaded!!!")
        else:
            print("---> Couldn't find Gender data set path")
            exit(1)

        if self.CASC_GENDER is None:
            print("---> Must supply GENDER classifier either through CASC_GENDER!!!")
            exit(1)

        self._event_ready.set()

    def run(self):
        super(GenderPredictionMD, self).run()
        print("[MODULE::GENDER_PREDICTION]: run()")

        self.processor.start()

    def stop(self):
        super(GenderPredictionMD, self).stop()

        self.processor.stop()

    async def do_process(self, data):
        super(GenderPredictionMD, self).do_process(data)
        return self.processor.process(data)

    def print_debug(self, data):
        super(GenderPredictionMD, self).print_debug(data)
        return

    def print_log(self, data):
        super(GenderPredictionMD, self).print_log(data)
        return
