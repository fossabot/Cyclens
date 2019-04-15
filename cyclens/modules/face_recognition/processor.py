# coding: utf-8

"""Processor functions for Face Recognition"""

from __future__ import unicode_literals

from ...common.preprocessor import div_255, get_date_now, get_date_str, crop_face
from ...common.processor import Processor

import time
import json

import cv2
import numpy as np
import tensorflow as tf


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

        date_start = get_date_now()

        result = {'module': 'face_recognition', 'success': False, 'message': 'null', 'process': {'start': get_date_str(date_start), 'end': 0, 'total': 0}, 'found': 0, 'rate': 0, 'faces': [], 'labels': []}

        if data is None:
            result['success'] = False
            result['message'] = 'There is no data to process'
            return json.dumps(result)

        image_rgb = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)

        faces = self.MD.CASC_FACE.detectMultiScale(image_rgb, scaleFactor = 1.3, minNeighbors = 5)
        result['found'] = len(faces)

        if len(faces) <= 0:
            result['success'] = False
            result['message'] = 'There is no face to process'
            return json.dumps(result)

        print("[MODULE::FACE_RECOGNITION::RESULT]=====================================================================================")
        print("Total faces found: {}".format(len(faces)))


        # Impl: https://raw.githubusercontent.com/tensorflow/tensorflow/master/tensorflow/examples/label_image/label_image.py

        detect_threshold = 0.45
        input_height = 299
        input_width = 299
        input_mean = 0 # 0
        input_std = 255 # 255
        input_layer = 'Mul'
        output_layer = "final_result"

        input_name = "import/" + input_layer
        output_name = "import/" + output_layer

        total_success_count = 0

        try:

            if len(faces) > 0:
                for i, face in enumerate(faces):

                    # Ortalama %10 kadar düşürebiliyor, daha iyi bir face çekme algoritması?
                    face_rgb, cropped = crop_face(image_rgb, face, margin = 30, size = 128)

                    (x, y, w, h) = cropped

                    result_face = {'id': i, 'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h), 'confidence': 0, 'evaluation': 0, 'result': 'null', 'success': False}

                    # cv2.imshow("a", face_rgb)
                    # cv2.waitKey(1500)
                    # cv2.destroyAllWindows()

                    try:
                        tensor = self.MD.read_tensor_from_cv2(image_rgb, input_height = input_height, input_width = input_width, input_mean = input_mean, input_std = input_std)

                        input_operation = self.MD.INCEPTION_MODEL.get_operation_by_name(input_name)
                        output_operation = self.MD.INCEPTION_MODEL.get_operation_by_name(output_name)

                        with tf.Session(graph = self.MD.INCEPTION_MODEL) as sess:
                            time_start = time.time()
                            results = sess.run(output_operation.outputs[0], {input_operation.outputs[0]: tensor})
                            time_end = time.time()

                        time_diff = time_end - time_start
                        results = np.squeeze(results)

                        # Çıkan sonuçların hepsini tara
                        top_k = results.argsort()[-5:][::-1]
                        for i in top_k:
                            label = str(self.MD.INCEPTION_LABEL[i])
                            confidence = round(float(results[i]), 3)
                            print(label, confidence)

                        best_id = np.argmax(results)
                        best_confidence = np.max(results)
                        best_label = self.MD.INCEPTION_LABEL[best_id]

                        if best_confidence >= detect_threshold:
                            confidence = best_confidence
                            text = best_label

                            result_face['confidence'] = round(float(confidence), 3)
                            result_face['evaluation'] = round(float(time_diff), 3)
                            result_face['result'] = text
                        else:
                            confidence = 0
                            text = 'unknown'

                        result_face['result'] = text

                        total_success_count += 1

                        result_face['success'] = True

                        print("Index: {}, Face Position: [{}, {}], Face Size: [{}, {}], Label: {}, Confidence: {}, BestL: {}, BestC: {}".format(i, x, y, w, h, text, confidence, best_label, best_confidence))
                    except Exception as e:
                        result_face['result'] = str(e)
                        result_face['success'] = False

                    result['faces'].append(result_face)

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
