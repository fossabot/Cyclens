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
        print("[MODULE::ACTION_RECOGNITION::PROC]: __init__")

    def __init__(self, module = None, ready = None):
        super(ActionRecognitionPROC, self).__init__(module, ready)
        print("[MODULE::ACTION_RECOGNITION::PROC]: __init__")

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

        result = {'module': 'action_recognition', 'success': False, 'message': 'null', 'found': 0, 'rate': 0, 'faces': []}

        if data is None:
            result['success'] = False
            result['message'] = 'There is no data to process'
            return json.dumps(result)

        result['success'] = False
        result['message'] = 'Not implemented yet'

        self.is_busy = False

        return json.dumps(result)
