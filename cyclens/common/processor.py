# coding: utf-8

"""An abstract class for processors."""

from __future__ import unicode_literals

from multiprocessing import Process, Queue
import threading

class Processor(threading.Thread):
    """An abstract class for Cyclens module processors."""

    processor_id : None

    def __init__(self, ready=None):
        print("[PROCESSOR::BASE]: __init__")
        self.process_queue = Queue()
        self._lock = threading.Lock()
        self._event = threading.Event()
        self._ready = ready
        self.is_busy = False
        threading.Thread.__init__(self)

    def run(self):
        return

    def process(self, data):
        self.is_busy = True

    def is_available(self):
        return self.is_alive()

    def enqueue(self, info):
        self._lock.acquire()
        try:
            if self.process_queue.full():
                print("[PROCESS::ENQUEUE]: Failed to add QUEUE -> FULL")
                return
            self.process_queue.put(info)
        finally:
            self._lock.release()

    def dequeue(self, info):
        self._lock.acquire()
        try:
            if not self.process_queue.empty():
                return self.process_queue.get_nowait()
        finally:
            self._lock.release()
        return None
