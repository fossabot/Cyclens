# coding: utf-8

"""
cyclens.modules.emotion_recognition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implements processor engine for 'EMOTION RECOGNITION' module

This program comes with ABSOLUTELY NO WARRANTY; This is free software,
and you are welcome to redistribute it under certain conditions; See
file LICENSE, which is part of this source code package, for details.

:copyright: Copyright © 2019, The Cyclens Project
:license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals

import cv2
import numpy as np
import traceback

from ...common.processor import Processor
from ...common.preprocessor import div_255, set_offsets


# noinspection PyPackageRequirements
class EmotionRecognitionPROC(Processor):

    def __init__(self, module=None, ready=None):
        super(EmotionRecognitionPROC, self).__init__(module, ready)

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

        data['module'] = self.MD.module_name

        total_success_count = 0

        if data['found'] > 0:

            #try:

            for i, face in enumerate(data['frame_faces']):

                x, y, w, h = set_offsets(face, (20, 40))

                result_face = {'id': i, 'x': int(x), 'y': int(y), 'width': int(w), 'height': int(h), 'confidence': 0, 'result': 'null', 'success': False}

                face_gray = data['frame_gray'][w:h, x:y]

                try:
                    face_gray = cv2.resize(face_gray, self.MD.emotion_target_size)
                except:
                    continue

                face_gray = div_255(face_gray, True)

                face_gray = np.expand_dims(face_gray, 0)
                face_gray = np.expand_dims(face_gray, -1)

                predict = self.MD.CASC_EMOTION.predict(face_gray)

                if predict is not None:
                    total_success_count += 1
                    confidence = np.max(predict)
                    arg = np.argmax(predict)
                    text = self.MD.EMOTIONS[arg]

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
            #except:
            #    data['success'] = False
            #    data['message'] = 'Type: {}, Message: TRY-EXCEPT', traceback.format_exc()
            #    self.process_fails += 1

            self.total_processed += 1

        self.is_busy = False

        return self.MD.post_processor.process(self.MD, data)
