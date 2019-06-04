# coding: utf-8

"""
cyclens.modules.common
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implements an abstract class for modules.

This program comes with ABSOLUTELY NO WARRANTY; This is free software,
and you are welcome to redistribute it under certain conditions; See
file LICENSE, which is part of this source code package, for details.

:copyright: Copyright © 2019, The Cyclens Project
:license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals

import threading

from .postprocessor import PostProcessor


class Module():
    """An abstract class for Cyclens modules."""

    module_id = -1
    module_name = 'null'

    def __init__(self, ready=None):
        self._event_ready = ready
        self._event_stop = threading.Event()

        self.post_processor = PostProcessor()
        self.post_processor.try_load()

        self.is_running = False

    def run(self):
        self.is_running = True

    def stop(self):
        self._event_stop.set()
        self.is_running = False

    def stopped(self):
        return self._event_stop.is_set()

    def get_id(self):
        return self.module_id

    def get_name(self):
        return self.module_name

    def do_process(self, data):
        return None

    def print_debug(self, data):
        return

    def print_log(self, data):
        return
