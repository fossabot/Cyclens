# coding: utf-8

"""An abstract class for modules."""

from __future__ import unicode_literals

from multiprocessing import Process, Queue

class Module(object):
    """An abstract class for Cyclens modules."""

    module_id : None

    def __init__(self):
        print("[MODULE::BASE]: __init__")
        self.process_queue = Queue()

    def on_data_received(self, data):
        print("[MODULE::EMOTICON_RECOGNATION::ON_DATA_RECEIVED]: " + data)
        self.process_queue.put(data)
        return
        return

    def on_data_sent(self, data):
        return

    def enqueue(self, data):
        return

    def dequeue(self, data):
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
