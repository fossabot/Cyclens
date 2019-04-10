# coding: utf-8

"""An abstract class for processors."""

from __future__ import unicode_literals

from multiprocessing import Process, Queue
import threading

class Processor(threading.Thread):
    """An abstract class for Cyclens module processors."""

    processor_id : None

    def __init__(self, module=None, ready=None):
        print("[PROCESSOR::BASE]: __init__")
        threading.Thread.__init__(self)
        self.MD = module
        self.process_queue = Queue()
        self._thread_lock = threading.Lock()
        self._thread_event = threading.Event()
        self._event_ready = ready
        self._event_stop = threading.Event()
        self.is_busy = False
        self.is_running = False

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
        return self.is_alive()

    def enqueue(self, info):
        self._thread_lock.acquire()
        try:
            if self.process_queue.full():
                print("[PROCESS::ENQUEUE]: Failed to add QUEUE -> FULL")
                return
            self.process_queue.put(info)
        finally:
            self._thread_lock.release()

    def dequeue(self, info):
        self._thread_lock.acquire()
        try:
            if not self.process_queue.empty():
                return self.process_queue.get_nowait()
        finally:
            self._thread_lock.release()
        return None
