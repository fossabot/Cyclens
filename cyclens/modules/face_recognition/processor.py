# coding: utf-8

"""Processor functions for Face Recognition"""

from __future__ import unicode_literals

from ...common.module import Module
from ...common.processor import Processor

import cv2
import numpy as np
import json

from ...utils import (
    ProcessingError,
)


class FaceRecognitionPROC(Processor):

    def __init__(self, module=None, ready=None):
        super(FaceRecognitionPROC, self).__init__(module, ready)
        print("[MODULE::FACE_RECOGNITION::PROC]: __init__")

        self._event_ready.set()

    def run(self):
        super(FaceRecognitionPROC, self).run()
        return

    def stop(self):
        super(FaceRecognitionPROC, self).stop()
        print("[MODULE::FACE_RECOGNITION::PROC]: stop()")
        return

    def process(self, data):
        super(FaceRecognitionPROC, self).process(data)

        result = {'module': 'face_recognition', 'success': False, 'message': 'null', 'found': 0, 'rate': 0, 'faces': []}

        if data is None:
            result['success'] = False
            result['message'] = 'There is no data to process'
            return json.dumps(result)

        image_gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)

        faces = self.MD.CASC_FACE.detectMultiScale(image_gray, scaleFactor = 1.3, minNeighbors = 5)
        result['found'] = len(faces)

        if len(faces) <= 0:
            result['success'] = False
            result['message'] = 'There is no face to process'
            return json.dumps(result)

        print("[MODULE::FACE_RECOGNITION::RESULT]=====================================================================================")
        print("Total faces found: {}".format(len(faces)))

        result['success'] = False
        result['message'] = 'Not implemented yet'

        print("===========================================================================================")

        self.is_busy = False

        return json.dumps(result)