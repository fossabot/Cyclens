# coding: utf-8

from __future__ import unicode_literals

from .age_prediction import AgePredictionMD
from .emotion_recognition import EmoticonRecognitionMD
from .face_dedection import FaceDedectionMD
from .gender_prediction import GenderPredictionMD

_ALL_CLASSES = [
    klass
    for name, klass in globals().items()
    if name.endswith('MD') and name != 'GenericMD'
]

def gen_modules_classes():
    """ Return a list of supported modules. """
    return _ALL_CLASSES


def gen_modules():
    """ Return a list of an instance of every supported modules. """
    return [klass() for klass in gen_modules_classes()]


def get_info_module(md_name):
    """Returns the info module class with the given md_name"""
    return globals()[md_name + 'MD']