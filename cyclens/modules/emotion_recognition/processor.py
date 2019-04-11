# coding: utf-8

"""Processor functions for Emoticon Recognition"""

from __future__ import unicode_literals

from ...common.preprocessor import div_255, set_offsets, get_date_now, get_date_str

from ...common.processor import Processor

import cv2
import numpy as np
import json


from ...utils import (
    ProcessingError,
)


# noinspection PyPackageRequirements
class EmotionRecognitionPROC(Processor):

    def __init__(self, module=None, ready=None):
        super(EmotionRecognitionPROC, self).__init__(module, ready)
        print("[MODULE::EMOTION_RECOGNITION::PROC]: __init__")

        self._event_ready.set()

    def run(self):
        super(EmotionRecognitionPROC, self).run()
        return

    def stop(self):
        super(EmotionRecognitionPROC, self).stop()
        print("[MODULE::EMOTION_RECOGNITION::PROC]: stop()")
        return

    def process(self, data):
        super(EmotionRecognitionPROC, self).process(data)

        date_start = get_date_now()

        result = {'module': 'emotion_recognition', 'success': False, 'message': 'null', 'process': {'start': get_date_str(date_start), 'end': 0, 'total': 0}, 'found': 0, 'rate': 0, 'faces': []}

        if data is None:
            result['success'] = False
            result['message'] = 'There is no data to process'
            return json.dumps(result)

        image_gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)

        faces = self.MD.CASC_FACE.detectMultiScale(image_gray, scaleFactor=1.3, minNeighbors=5)
        result['found'] = len(faces)

        if len(faces) <= 0:
            result['success'] = False
            result['message'] = 'There is no face to process'
            return json.dumps(result)

        print("[MODULE::EMOTION_RECOGNITION::RESULT]=====================================================================================")
        print("Total faces found: {}".format(len(faces)))

        total_success_count = 0

        try:

            if len(faces) > 0:
                for i, face in enumerate(faces):

                    x, y, w, h = set_offsets(face, (20, 40))

                    result_face = {'id': i, 'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h), 'result': 'null', 'success': False}

                    face_gray = image_gray[w:h, x:y]

                    try:
                        face_gray = cv2.resize(face_gray, self.MD.emotion_target_size)
                        #cv2.imshow("a", face_gray)
                        #cv2.waitKey(1000)
                        #cv2.destroyAllWindows()
                    except:
                        continue

                    face_gray = div_255(face_gray, True)

                    face_gray = np.expand_dims(face_gray, 0)
                    face_gray = np.expand_dims(face_gray, -1)

                    predict = self.MD.CASC_EMOTION.predict(face_gray)

                    if predict is not None:
                        total_success_count += 1
                        arg = np.argmax(predict)
                        text = self.MD.EMOTIONS[arg]

                        result_face['result'] = text
                        result_face['success'] = True

                        print("Index: {}, Face Position: [{}, {}], Face Size: [{}, {}], Gender: {}".format(i, x, y, w, h, text))

                    result['faces'].append(result_face)

            if total_success_count != len(faces):
                msg = 'There are {} faces but {} faces processed successfully. Please check what (tf) is going on!'.format(len(faces), total_success_count)
                result['message'] = msg
                print(msg)

            rate = len(faces) / total_success_count * 100

            result['rate'] = rate

            result['success'] = True
            self.process_successes += 1
        except:
            result['success'] = False
            self.process_fails += 1

        self.total_processed += 1

        date_end = get_date_now()

        ms_diff = (date_end - date_start).microseconds / 1000

        self.response_times.append(ms_diff)

        result['process']['end'] = get_date_str(date_end)
        result['process']['total'] = ms_diff

        print("Processing success rate: %{}".format(rate))
        print("===========================================================================================")

        self.is_busy = False

        return json.dumps(result)
