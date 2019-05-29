# coding: utf-8

"""Processor functions for Action Recognation"""

from __future__ import unicode_literals

from ...common.module import Module
from ...common.processor import Processor

import cv2
import numpy as np
import json

from ...utils import (
    ProcessingError,
)


class ActionRecognitionPROC(Processor):

    test : None

    def __init__(self):
        Processor.__init__(self)

    def __init__(self, module = None, ready = None):
        super(ActionRecognitionPROC, self).__init__(module, ready)

        self._event_ready.set()

    def run(self):
        super(ActionRecognitionPROC, self).run()
        return

    def stop(self):
        super(ActionRecognitionPROC, self).stop()
        print("[MODULE::ACTION_RECOGNITION::PROC]: stop()")
        return

    def process(self, data):
        super(ActionRecognitionPROC, self).process(data)

        result = data

        result['success'] = False
        result['message'] = 'Not implemented yet'

        self.is_busy = False

        return json.dumps(result)
