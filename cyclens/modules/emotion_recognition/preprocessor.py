# coding: utf-8

"""Pre-processor functions for Emoticon Recognation"""

from __future__ import unicode_literals

from ...common.module import Module
from ...common.processor import Processor

import cv2
import numpy as np

from ...utils import (
    PreProcessingError,
)

class EmotionRecognitionPREP(Processor):

    test : None

    def __init__(self, module=None, ready=None):
        super(EmotionRecognitionPREP, self).__init__(module, ready)
        print("[MODULE::EMOTION_RECOGNITION::PREP]: __init__")


        self._event_ready.set()

    def run(self):
        super(EmotionRecognitionPREP, self).run()
        return

    def stop(self):
        super(EmotionRecognitionPREP, self).stop()
        print("[MODULE::EMOTION_RECOGNITION::PREP]: stop()")
        return

    def predict(self, image):
        if image is None:
            return None
        image = image.reshape([-1, 48, 48, 1])
        return self.MD.model.predict(image)

    def process(self, data, ready):
        super(EmotionRecognitionPREP, self).process(data)

        if data is None:
            print("data Noneeeeeeeeeeeeeeeeeeeeeeeeeeeeeeee")
            return None

        EMOTIONS = ['angry', 'disgusted', 'fearful', 'happy', 'sad', 'surprised', 'neutral']
        cascface = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
        gray = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        faces = cascface.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)

        print("RESULT=====================================================================================")
        print("Total faces found: ")
        print(len(faces))
        if len(faces) > 0:
            for face in faces:
                (x, y, w, h) = face
                data = cv2.rectangle(data, (x, y-30), (x+w, y+h+10), (255, 0, 0), 2)
                newimg = data[y:y+h, x:x+w]
                newimg = cv2.resize(newimg, (48, 48), interpolation=cv2.INTER_CUBIC) / 255.

                #cv2.imshow("a", newimg)
                #cv2.waitKey(0)

                result = self.predict(newimg)
                if result is not None:
                    maxindex = np.argmax(result[0])
                    print("Emotion: ")
                    print(maxindex)
                    print(EMOTIONS[maxindex])
        print("===========================================================================================")

        self.is_busy = False

        ready.set()
        return "ok"
