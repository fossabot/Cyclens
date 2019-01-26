# coding: utf-8

"""An abstract class for modules."""

from __future__ import unicode_literals

from multiprocessing import Process, Queue

import threading

class Module(threading.Thread):
    """An abstract class for Cyclens modules."""

    module_id : None

    def __init__(self):
        print("[MODULE::BASE]: __init__")
        threading.Thread.__init__(self)
        self.process_queue = Queue()

    def run(self):
        return

    def enqueue(self, data):
        if self.process_queue.full():
            print("[MODULE::ENQUEUE]: Failed to add QUEUE -> FULL")
            return

        self.process_queue.put(data)

    def dequeue(self, data):
        if not self.process_queue.empty():
            return self.process_queue.get_nowait()

        return None

    def on_data_received(self, data):
        print("[MODULE::BASE::ON_DATA_RECEIVED]:")
        self.enqueue(data)

    def on_data_sent(self, data):
        return

    def post_to_preprocessor(self, data):
        return

    def post_to_processor(self, data):
        return

    def post_to_postprocessor(self, data):
        return

    def print_debug(self, data):
        return

    def print_log(self, data):
        return
