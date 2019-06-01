# coding: utf-8

"""Processor functions for Gender Prediction"""

from __future__ import unicode_literals

from ...common.preprocessor import div_255, set_offsets, get_date_now, get_date_str
from ...common.processor import Processor

import cv2
import numpy as np
import traceback
import sys
import json

from ...utils import (
    ProcessingError,
)


class GenderPredictionPROC(Processor):

    def __init__(self, module=None, ready=None):
        super(GenderPredictionPROC, self).__init__(module, ready)

        self._event_ready.set()

    def run(self):
        super(GenderPredictionPROC, self).run()
        return

    def stop(self):
        super(GenderPredictionPROC, self).stop()
        print("[MODULE::GENDER_PREDICTION::PROC]: stop()")
        return

    def process(self, data):
        super(GenderPredictionPROC, self).process(data)

        data['module'] = self.MD.module_name

        total_success_count = 0

        if data['found'] > 0:

            try:
                for i, face in enumerate(data['frame_faces']):

                    x, y, w, h = set_offsets(face, (30, 60))

                    result_face = {'id': i, 'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h), 'confidence': 0, 'result': 'null', 'success': False}

                    face_rgb = data['frame_rgb'][w:h, x:y]

                    try:
                        face_rgb = cv2.resize(face_rgb, self.MD.gender_target_size)
                        # cv2.imshow("a", face_gray)
                        # cv2.waitKey(1000)
                        # cv2.destroyAllWindows()
                    except:
                        continue

                    face_rgb = np.expand_dims(face_rgb, 0)
                    face_rgb = div_255(face_rgb, False)

                    predict = self.MD.CASC_GENDER.predict(face_rgb)

                    if predict is not None:
                        total_success_count += 1
                        confidence = np.max(predict)
                        arg = np.argmax(predict)
                        text = self.MD.GENDERS[arg]

                        result_face['confidence'] = round(float(confidence), 2)
                        result_face['result'] = text
                        result_face['success'] = True

                    data['faces'].append(result_face)

                if total_success_count != data['found']:
                    msg = 'There are {} faces but {} faces processed successfully. Please check what (tf) is going on!'.format(data['found'], total_success_count)
                    data['message'] = msg

                if total_success_count > 0:
                    rate = data['found'] / total_success_count * 100
                    data['rate'] = rate
                else:
                    data['rate'] = 0

                data['success'] = True
                self.process_successes += 1

            except:
                data['success'] = False
                data['message'] = 'Type: {}, Message: TRY-EXCEPT', traceback.format_exc()
                self.process_fails += 1

            self.total_processed += 1

        self.is_busy = False

        return self.MD.post_processor.process(self.MD, data)
