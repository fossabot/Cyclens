# coding: utf-8

"""
cyclens.modules.common
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implements common pre-processor class for modules.

This program comes with ABSOLUTELY NO WARRANTY; This is free software,
and you are welcome to redistribute it under certain conditions; See
file LICENSE, which is part of this source code package, for details.

:copyright: Copyright © 2019, The Cyclens Project
:license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals

import cv2
import numpy as np

from os.path import isfile
from datetime import datetime
from pathlib import Path

base_path = Path(__file__).parent.parent


class PreProcessor:

    def __init__(self):
        self.detection_model_path = str((base_path / "../data/models/detection/haarcascade_frontalface_default.xml").resolve())
        self.CASC_FACE = None

    def try_load(self):
        if isfile(self.detection_model_path):
            try:
                self.CASC_FACE = cv2.CascadeClassifier(self.detection_model_path)
                return True
            except:
                return False
        return False

    def process(self, data):
        result = {'success': True, 'module': '', 'message': 'null', 'process': {'start': 0, 'end': 0, 'total': 0}, 'found': 0, 'rate': 0, 'faces': [], 'frame_faces': None, 'frame_gray': None, 'frame_rgb': None}

        result['process']['start'] = datetime.now()

        if data is None:
            result['success'] = False
            result['message'] = 'There is no data to process'
            return result

        frame = cv2.resize(data, (0, 0), fx = 0.25, fy = 0.25)

        h, w = frame.shape[:2]

        if h <= 0 or w <= 0:
            result['success'] = False
            result['message'] = 'There is no frame to process'
            return result

        image_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        image_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        result['frame_gray'] = image_gray
        result['frame_rgb'] = image_rgb

        result['frame_faces'] = self.CASC_FACE.detectMultiScale(image_gray, scaleFactor = 1.3, minNeighbors = 5)

        result['found'] = len(result['frame_faces'])

        if len(result['frame_faces']) <= 0:
            result['success'] = False
            result['message'] = 'There is no face to process'
            return result

        return result


def div_255(x, v2 = True):
    x = x.astype('float32')
    x = x / 255.0
    if v2:
        x = x - 0.5
        x = x * 2.0
    return x


def set_offsets(face, offsets):
    x, y, width, height = face
    x_off, y_off = offsets
    return x - x_off, x + width + x_off, y - y_off, y + height + y_off


def get_date_now():
    return datetime.now()


def get_date_str(date):
    return date.strftime('%Y-%m-%dT%H:%M:%S.%f')


def crop_face(imgarray, section, margin = 40, size = 64):
    """
    :param imgarray: full image
    :param section: face detected area (x, y, w, h)
    :param margin: add some margin to the face detected area to include a full head
    :param size: the result image resolution with be (size x size)
    :return: resized image in numpy array with shape (size x size x 3)
    """
    img_h, img_w, _ = imgarray.shape
    if section is None:
        section = [0, 0, img_w, img_h]
    (x, y, w, h) = section
    margin = int(min(w, h) * margin / 100)
    x_a = x - margin
    y_a = y - margin
    x_b = x + w + margin
    y_b = y + h + margin
    if x_a < 0:
        x_b = min(x_b - x_a, img_w - 1)
        x_a = 0
    if y_a < 0:
        y_b = min(y_b - y_a, img_h - 1)
        y_a = 0
    if x_b > img_w:
        x_a = max(x_a - (x_b - img_w), 0)
        x_b = img_w
    if y_b > img_h:
        y_a = max(y_a - (y_b - img_h), 0)
        y_b = img_h
    cropped = imgarray[y_a: y_b, x_a: x_b]
    resized_img = cv2.resize(cropped, (size, size), interpolation = cv2.INTER_AREA)
    resized_img = np.array(resized_img)
    return resized_img, (x_a, y_a, x_b - x_a, y_b - y_a)
