# coding: utf-8

from __future__ import unicode_literals

from .action_recognition.action_recognition import ActionRecognitionMD
from .age_prediction.age_prediction import AgePredictionMD
from .emotion_recognition.emotion_recognition import EmotionRecognitionMD
from .face_recognition.face_recognition import FaceRecognitionMD
from .gender_prediction.gender_prediction import GenderPredictionMD

_ALL_CLASSES = [
    klass
    for name, klass in globals().items()
    if name.endswith('MD') and name != 'GenericMD'
]


def get_preprocessor(key):
    return globals()[key + 'PREP']


def get_processor(key):
    return globals()[key + 'PROC']


def get_postprocessor(key):
    return globals()[key + 'POSP']


def gen_modules_classes():
    """ Return a list of supported modules. """
    return _ALL_CLASSES


def gen_modules():
    """ Return a list of an instance of every supported modules. """
    return [klass() for klass in gen_modules_classes()]


def get_module(md_name):
    """Returns the info module class with the given md_name"""
    return globals()[md_name + 'MD']
