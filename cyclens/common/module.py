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
        print("[MODULE::BASE]: __init__")
        threading.Thread.__init__(self)
        self._event_ready = ready
        self._event_stop = threading.Event()
        self.process_queue = Queue()
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

    def enqueue(self, data):
        if self.process_queue.full():
            print("[MODULE::ENQUEUE]: Failed to add QUEUE -> FULL")
            return

        self.process_queue.put(data)

    def dequeue(self):
        if not self.process_queue.empty():
            return self.process_queue.get_nowait()
        return None

    def do_process(self, data):
        print("[MODULE::BASE::ON_DATA_RECEIVED]:")
        self.enqueue(data)

        return None

    def print_debug(self, data):
        return

    def print_log(self, data):
        return
