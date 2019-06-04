# coding: utf-8

"""
cyclens.modules.common
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implements an abstract class for module's processor.

This program comes with ABSOLUTELY NO WARRANTY; This is free software,
and you are welcome to redistribute it under certain conditions; See
file LICENSE, which is part of this source code package, for details.

:copyright: Copyright © 2019, The Cyclens Project
:license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals

import threading
import numpy as np


class Processor(threading.Thread):
    """An abstract class for Cyclens module processors."""

    def __init__(self, module=None, ready=None):
        threading.Thread.__init__(self)
        self.MD = module
        self._thread_lock = threading.Lock()
        self._thread_event = threading.Event()
        self._event_ready = ready
        self._event_stop = threading.Event()

        self.is_busy = False
        self.is_running = False

        self.processor_id = -1

        self.total_processed = 0
        self.process_fails = 0
        self.process_successes = 0

        self.response_times = []

    def run(self):
        self.is_running = True

    def stop(self):
        self._event_stop.set()
        self.is_running = False

    def stopped(self):
        return self._event_stop.is_set()

    def process(self, data):
        self.is_busy = True
        return None

    def is_available(self):
        return self.isAlive()

    def get_id(self):
        return self.processor_id

    def get_response_time_estimated(self):
        if len(self.response_times) == 0:
            return 0
        return round(sum(self.response_times) / len(self.response_times), 2)

    def get_response_time_std(self):
        if len(self.response_times) < 2:
            return 0
        return round(np.std(self.response_times, ddof=1), 2)

    def get_response_time_rms(self):
        if len(self.response_times) == 0:
            return 0
        return round(np.sqrt(np.mean(np.square(self.response_times))), 2)

    def get_average_crash_rate(self):
        if self.total_processed == 0:
            return 0
        return round(self.process_fails / self.total_processed * 100, 2)

    def get_total_processed(self):
        return self.total_processed

    def get_process_fails(self):
        return self.process_fails

    def get_process_successes(self):
        return self.process_successes
