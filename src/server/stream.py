# coding: utf-8

import threading
import cv2

class RealtimeStream(threading.Thread):

    def __init__(self, name, camera):
        threading.Thread.__init__(self)
        self.name = name
        self.isRunning = True
        self.frame = None

    def run(self):
        while self.isRunning:
            ret, frame = self.frame
            if ret:
                cv2.imshow('Test', frame)

    def stop(self):
        self.isRunning = False
