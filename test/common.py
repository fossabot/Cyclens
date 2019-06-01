# coding: utf-8

"""Common class for testing purposes."""

from __future__ import unicode_literals

from pathlib import Path
from PIL import Image
from datetime import datetime

import cv2
import os

import numpy as np

IMG_EXTS = [".jpg", ".jpeg", ".png", ".gif"]

PATH_BASE = Path(__file__).parent

PATH_FACES_0 = str((PATH_BASE / "./images/faces/0").resolve())
PATH_FACES_1 = str((PATH_BASE / "./images/faces/1").resolve())
PATH_FACES_2 = str((PATH_BASE / "./images/faces/2").resolve())
PATH_FACES_3 = str((PATH_BASE / "./images/faces/3").resolve())

SAMPLE_RESULT = {'success': True, 'module': '', 'message': 'null', 'process': {'start': datetime.now(), 'end': 0, 'total': 0}, 'found': 0, 'rate': 0, 'faces': [], 'frame_faces': None, 'frame_gray': None, 'frame_rgb': None}

SAMPLE_MODULE_TESTS = [{'image': str((PATH_BASE / "./images/faces/1/0.jpg").resolve()), 'er': 'ANGRY', 'gp': 'MAN', 'ap': 30}]


def get_img(file):
    return cv2.imread(file, cv2.COLOR_BGR2RGB)


def get_imgs(path):
    imgs = []

    for f in os.listdir(path):
        ext = os.path.splitext(f)[1]

        if ext.lower() not in IMG_EXTS:
            continue

        imgs.append(cv2.imread(os.path.join(path, f), cv2.COLOR_BGR2RGB))

    return imgs
