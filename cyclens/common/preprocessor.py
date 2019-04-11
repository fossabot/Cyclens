# coding: utf-8

"""Common pre-processor class for modules."""

from __future__ import unicode_literals

from datetime import datetime

from multiprocessing import Process, Queue
import threading


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
    return datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')
