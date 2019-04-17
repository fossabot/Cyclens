# coding: utf-8

"""An abstract class for modules."""

from __future__ import unicode_literals

from multiprocessing import Process, Queue

import threading

class Module(threading.Thread):
    """An abstract class for Cyclens modules."""

    module_id = -1
    module_name = 'null'

    def __init__(self, ready=None):
        threading.Thread.__init__(self)
        self._event_ready = ready
        self._event_stop = threading.Event()
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
