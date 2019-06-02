# coding: utf-8

"""
cyclens.modules.action_recognition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implements processor engine for 'ACTION RECOGNITION' module

This program comes with ABSOLUTELY NO WARRANTY; This is free software,
and you are welcome to redistribute it under certain conditions; See
file LICENSE, which is part of this source code package, for details.

:copyright: Copyright © 2019, The Cyclens Project
:license: MIT, see LICENSE for more details.
"""


from __future__ import unicode_literals

from ...common.module import Module
from ...common.processor import Processor

import cv2
import numpy as np
import json

from ...utils import (
    ProcessingError,
)


class ActionRecognitionPROC(Processor):

    test : None

    def __init__(self):
        Processor.__init__(self)

    def __init__(self, module = None, ready = None):
        super(ActionRecognitionPROC, self).__init__(module, ready)

        self._event_ready.set()

    def run(self):
        super(ActionRecognitionPROC, self).run()
        return

    def stop(self):
        super(ActionRecognitionPROC, self).stop()
        print("[MODULE::ACTION_RECOGNITION::PROC]: stop()")
        return

    def process(self, data):
        super(ActionRecognitionPROC, self).process(data)

        result = data

        result['success'] = False
        result['message'] = 'Not implemented yet'

        self.is_busy = False

        return self.MD.post_processor.process(self.MD, data)
