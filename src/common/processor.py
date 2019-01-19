# coding: utf-8

"""An abstract class for processors."""

from __future__ import unicode_literals

class Processor(object):
    """An abstract class for Cyclens module processors."""

    processor_id : None

    def __init__(self):
        return

    def is_available(self):
        return

    def is_runnable(self):
        return

    def enqueue(self, info):
        return

    def dequeue(self, info):
        return

    def run(info):
        return
