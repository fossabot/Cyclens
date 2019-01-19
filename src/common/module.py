# coding: utf-8

"""An abstract class for modules."""

from __future__ import unicode_literals

class Module(object):
    """An abstract class for Cyclens modules."""

    module_id : None

    def on_data_received(self, data):
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
