# coding: utf-8

"""Common class for PATHs"""

from __future__ import unicode_literals

from pathlib import Path

PATH_BASE = Path(__file__).parent

PATH_MODEL_EMOTION = str((PATH_BASE / "../../data/models/emotion/fer2013_mini_XCEPTION.102-0.66.hdf5").resolve())

PATH_MODEL_GENDER = str((PATH_BASE / "../../data/models/gender/simple_CNN.81-0.96.hdf5").resolve())

PATH_MODEL_AGE = str((PATH_BASE / "../../data/models/age/weights.18-4.06.hdf5").resolve())
