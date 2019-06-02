# coding: utf-8

"""
cyclens.modules.age_prediction
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implements processor engine for 'AGE PREDICTION' module

This program comes with ABSOLUTELY NO WARRANTY; This is free software,
and you are welcome to redistribute it under certain conditions; See
file LICENSE, which is part of this source code package, for details.

:copyright: Copyright © 2019, The Cyclens Project
:license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals

from ...common.module import Module
from ...common.processor import Processor

from ...common.preprocessor import div_255, get_date_now, get_date_str, crop_face

import cv2
import numpy as np
import sys
import traceback
import json

from ...utils import (
    ProcessingError,
)


class AgePredictionPROC(Processor):

    def __init__(self, module=None, ready=None):
        super(AgePredictionPROC, self).__init__(module, ready)

        self.processor_id = 1
        self.processor_name = 'age_prediction'

        self._event_ready.set()

    def run(self):
        super(AgePredictionPROC, self).run()
        return

    def stop(self):
        super(AgePredictionPROC, self).stop()
        print("[MODULE::AGE_PREDICTION::PROC]: stop()")
        return

    def process(self, data):
        super(AgePredictionPROC, self).process(data)

        data['module'] = self.MD.module_name

        total_success_count = 0

        if data['found'] > 0:

            try:
                face_imgs = np.empty((data['found'], self.MD.face_size, self.MD.face_size, 3))

                for i, face in enumerate(data['frame_faces']):

                    face_img, cropped = crop_face(data['frame_rgb'], face, margin = 40, size = self.MD.face_size)

                    # null check ve image.shape checks
                    (x, y, w, h) = cropped

                    result_face = {'id': i, 'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h), 'confidence': 0, 'result': 'null', 'success': False}
                    data['faces'].append(result_face)

                    # print(type(face_img)) # numpy.ndarray
                    # print(type(cropped)) # tuple

                    face_imgs[i, :, :, :] = face_img

                if len(face_imgs) > 0:

                    predict = self.MD.CASC_AGE.predict(face_imgs)

                    if predict is not None:

                        predicted_genders = predict[0]
                        ages = np.arange(0, 101).reshape(101, 1)
                        predicted_ages = predict[1].dot(ages).flatten()
                        predicted_confidences = predict[1]

                        for i, face in enumerate(data['faces']):
                            total_success_count += 1

                            confidence = np.max(predicted_confidences[i])
                            age = int(predicted_ages[i])

                            #gender = "F" if predicted_genders[i][0] > 0.5 else "M"

                            data['faces'][i]['confidence'] = round(float(confidence), 2)
                            data['faces'][i]['result'] = age
                            data['faces'][i]['success'] = True

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
