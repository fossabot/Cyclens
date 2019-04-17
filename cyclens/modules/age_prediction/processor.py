# coding: utf-8

"""Processor functions for Age Prediction"""

from __future__ import unicode_literals

from ...common.module import Module
from ...common.processor import Processor

from ...common.preprocessor import div_255, get_date_now, get_date_str, crop_face

import cv2
import numpy as np
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

        date_start = get_date_now()

        result = {'module': 'age_prediction', 'success': False, 'message': 'null', 'process': {'start': get_date_str(date_start), 'end': 0, 'total': 0}, 'found': 0, 'rate': 0, 'faces': []}

        if data is None:
            result['success'] = False
            result['message'] = 'There is no data to process'
            return json.dumps(result)

        image_gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        image_rgb = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)

        faces = self.MD.CASC_FACE.detectMultiScale(image_gray, scaleFactor = 1.3, minNeighbors = 5, minSize=(self.MD.face_size, self.MD.face_size))
        result['found'] = len(faces)

        if len(faces) <= 0:
            result['success'] = False
            result['message'] = 'There is no face to process'
            return json.dumps(result)

        print("[MODULE::AGE_PREDICTION::RESULT]=====================================================================================")
        print("Total faces found: {}".format(len(faces)))

        total_success_count = 0

        try:
            if len(faces) > 0:

                face_imgs = np.empty((len(faces), self.MD.face_size, self.MD.face_size, 3))

                for i, face in enumerate(faces):

                    face_img, cropped = crop_face(image_rgb, face, margin = 40, size = self.MD.face_size)

                    # null check ve image.shape checks
                    (x, y, w, h) = cropped

                    result_face = {'id': i, 'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h), 'confidence': 0, 'result': 'null', 'success': False}
                    result['faces'].append(result_face)

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

                        for i, face in enumerate(faces):
                            total_success_count += 1

                            confidence = np.max(predicted_confidences[i])
                            age = int(predicted_ages[i])

                            #gender = "F" if predicted_genders[i][0] > 0.5 else "M"

                            result['faces'][i]['confidence'] = round(float(confidence), 2)
                            result['faces'][i]['result'] = age
                            result['faces'][i]['success'] = True

                            print("Index: {}, Face Position: [{}, {}], Face Size: [{}, {}], Gender: {}".format(i, x, y, w, h, age))

            if total_success_count != len(faces):
                msg = 'There are {} faces but {} faces processed successfully. Please check what (tf) is going on!'.format(len(faces), total_success_count)
                result['message'] = msg
                print(msg)

            rate = len(faces) / total_success_count * 100

            print("Processing success rate: %{}".format(rate))

            result['rate'] = rate
            result['success'] = True
            self.process_successes += 1
        except:
            result['success'] = False
            self.process_fails += 1

        self.total_processed += 1

        date_end = get_date_now()

        ms_diff = (date_end - date_start).total_seconds() * 1000

        self.response_times.append(ms_diff)

        result['process']['end'] = get_date_str(date_end)
        result['process']['total'] = round(ms_diff, 2)

        print("===========================================================================================")

        self.is_busy = False

        return json.dumps(result)
