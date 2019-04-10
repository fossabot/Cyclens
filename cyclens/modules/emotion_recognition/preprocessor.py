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


# noinspection PyPackageRequirements
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

    def preprocess_input(self, x, v2=True):
        x = x.astype('float32')
        x = x / 255.0
        if v2:
            x = x - 0.5
            x = x * 2.0
        return x

    def apply_offsets(self, face, offsets):
        x, y, width, height = face
        x_off, y_off = offsets
        return (x - x_off, x + width + x_off, y - y_off, y + height + y_off)

    def process(self, data, ready):
        super(EmotionRecognitionPREP, self).process(data)

        if data is None:
            print("There is no data to process!!!")
            return None

        emotion_offsets = (20, 40)
        gray_image = cv2.cvtColor(data, cv2.COLOR_BGR2GRAY)
        faces = self.MD.CASC_FACE.detectMultiScale(gray_image, scaleFactor=1.3, minNeighbors=5)

        print("RESULT=====================================================================================")
        print("Total faces found: ")
        print(len(faces))

        process_index = 0

        if len(faces) > 0:
            for face in faces:
                #(x, y, w, h) = face
                x, y, w, h = self.apply_offsets(face, emotion_offsets)
                gray_face = gray_image[w:h, x:y]

                try:
                    gray_face = cv2.resize(gray_face, (self.MD.emotion_target_size))
                    #cv2.imshow("a", gray_face)
                    #cv2.waitKey(1000)
                    #cv2.destroyAllWindows()
                except:
                    continue

                gray_face = self.preprocess_input(gray_face, True)
                gray_face = np.expand_dims(gray_face, 0)
                gray_face = np.expand_dims(gray_face, -1)
                result = self.MD.emotion_classifier.predict(gray_face)

                if result is not None:
                    process_index += 1
                    emotion_label_arg = np.argmax(result)
                    emotion_text = self.MD.emotion_labels[emotion_label_arg]
                    print("Emotion:")
                    print(emotion_text)

        if process_index != len(faces):
            print('There are {} face but {} face processed successfully. Please check what (tf) is going on!'.format(len(faces), process_index))

        print("===========================================================================================")

        self.is_busy = False

        ready.set()
        return "ok"
