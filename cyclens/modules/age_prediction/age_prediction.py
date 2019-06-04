# coding: utf-8

"""
cyclens.modules.age_prediction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implements 'AGE PREDICTION' module

This program comes with ABSOLUTELY NO WARRANTY; This is free software,
and you are welcome to redistribute it under certain conditions; See
file LICENSE, which is part of this source code package, for details.

:copyright: Copyright © 2019, The Cyclens Project
:license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals

import threading

from os.path import isfile

from .processor import AgePredictionPROC
from ...common.module import Module
from ...common.paths import PATH_MODEL_AGE
from ...common.wide_resnet import WideResNet


class AgePredictionMD(Module):

    def __init__(self, ready=None):
        super(AgePredictionMD, self).__init__(ready)

        self.module_id = 1
        self.module_name = 'age_prediction'

        _ready = threading.Event()

        _ready.clear()
        self.processor = AgePredictionPROC(self, _ready)
        _ready.wait()

        self.CASC_AGE = None

        if isfile(PATH_MODEL_AGE):
            self.face_size = 64
            self.CASC_AGE = WideResNet(64, depth = 16, k = 8)()
            self.CASC_AGE.load_weights(PATH_MODEL_AGE)
            self.CASC_AGE._make_predict_function()
            print("---> Age data set Loaded!!!")
        else:
            print("---> Couldn't find Age data set path")
            exit(1)

        if self.CASC_AGE is None:
            print("---> Must supply AGE classifier either through CASC_AGE!!!")
            exit(1)

        self._event_ready.set()

    def run(self):
        super(AgePredictionMD, self).run()
        print("[MODULE::AGE_PREDICTION]: run()")

        self.processor.start()

    def stop(self):
        super(AgePredictionMD, self).stop()

        self.processor.stop()

    async def do_process(self, data):
        super(AgePredictionMD, self).do_process(data)
        return self.processor.process(data)

    def print_debug(self, data):
        super(AgePredictionMD, self).print_debug(data)
        return

    def print_log(self, data):
        super(AgePredictionMD, self).print_log(data)
        return
