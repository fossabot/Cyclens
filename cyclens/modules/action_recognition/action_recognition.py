# coding: utf-8

"""
cyclens.modules.action_recognition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implements 'ACTION RECOGNITION' module

This program comes with ABSOLUTELY NO WARRANTY; This is free software,
and you are welcome to redistribute it under certain conditions; See
file LICENSE, which is part of this source code package, for details.

:copyright: Copyright © 2019, The Cyclens Project
:license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals

import cv2
import threading

from os.path import isfile

from .processor import ActionRecognitionPROC
from ...common.module import Module


class ActionRecognitionMD(Module):

    def __init__(self, ready=None):
        super(ActionRecognitionMD, self).__init__(ready)

        self.module_id = 0
        self.module_name = 'action_recognition'

        _ready = threading.Event()

        _ready.clear()
        self.processor = ActionRecognitionPROC(self, _ready)
        _ready.wait()

        self.CASC_FACE = None

        detection_model_path = '../data/models/detection/haarcascade_frontalface_default.xml'

        if isfile(detection_model_path):
            self.CASC_FACE = cv2.CascadeClassifier(detection_model_path)
            print("---> Face detection data set Loaded!!!")
        else:
            print("---> Couldn't find cascade model")
            exit(1)

        self._event_ready.set()

    def run(self):
        super(ActionRecognitionMD, self).run()
        print("[MODULE::ACTION_RECOGNITION]: run()")

        self.processor.start()

    def stop(self):
        super(ActionRecognitionMD, self).stop()

        self.processor.stop()

    async def do_process(self, data):
        super(ActionRecognitionMD, self).do_process(data)
        self.processor.process(data)

    def print_debug(self, data):
        super(ActionRecognitionMD, self).print_debug(data)
        return

    def print_log(self, data):
        super(ActionRecognitionMD, self).print_log(data)
        return
