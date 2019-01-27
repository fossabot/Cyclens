#!/usr/bin/env python
# coding: utf-8

from flask import Flask, Response, render_template, jsonify, request

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

import asyncio

import json
import numpy as np
import cv2
from matplotlib import pyplot as plt

import threading
from multiprocessing import Process, Queue


headerJSON = {'Content-Type': 'application/json'}
headerJPEG = {'Content-Type': 'image/jpeg'}

global stream

class ApiServer(threading.Thread):

    api = Flask(__name__)

    request_queue = None

    def __init__(self):
        print("[API]: __init__")
        threading.Thread.__init__(self)
        self.request_queue = Queue()

    def run(self):
        self.add_routes()
        self.start_api(debug=False, host="localhost", port=5000)
        print("[API]: run")

    def add_to_queue(self, request):
        if self.request_queue.full():
            print("[API::ADD_TO_QUEUE]: Failed to add QUEUE -> FULL")
            return

        self.request_queue.put(request)

    def get_from_queue(self):
        if self.request_queue.empty():
            return None

        return self.request_queue.get()

    def start_api(self, debug, host, port):
        print("[API]: start")
        #Tonado: non-blocking, asynchronous 
        asyncio.set_event_loop(asyncio.new_event_loop())
        http_server = HTTPServer(WSGIContainer(self.api))
        http_server.listen(port)
        IOLoop.instance().start()
        #self.api.run(debug=debug, host=host, port=port)

    def is_running(self):
        #TODO: Make real return pls
        return True

    # Test: curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@/home/dentrax/Pictures/Wallpapers/wp1.jpg" http://localhost:5000/test/demo
    # Test: curl -F "file=@/home/dentrax/Pictures/Wallpapers/wp1.jpg" http://localhost:5000/test/demo
    def add_routes(self):
        print("[API]: Add routes")

        @self.api.route('/api/v1/demo', methods=['POST'])
        def some_route():
            data = request.files['file'].read()
            npimg = np.frombuffer(data, np.uint8)
            img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)
            self.add_to_queue(img)

            resp = Response(response="OK", status=200, mimetype="application/json")
            resp.headers['Content-Type'] = 'application/json; charset=utf-8'
            resp.headers['Access-Control-Allow-Origin'] = '*'

            return resp

    @api.route('/api/example', methods=['POST'])
    def demo():
        print(request.files)
        data = request.files['file'].read()

        print('FILE')

        npimg = np.frombuffer(data, np.uint8)


        # PRE-PROCESSOR
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        small = cv2.resize(img, (0, 0), fx=0.3, fy=0.3)

        edges = cv2.Canny(small, 100, 200)

        cv2.imshow('HSV image', edges)
        cv2.waitKey(0)

        # PROCESSOR
        # calcHist([img], [0], None, [256], [0, 256])

        color = ('b', 'g', 'r')
        for i, col in enumerate(color):
            histr = cv2.calcHist([img], [i], None, [256], [0, 256])
            plt.plot(histr, color=col)

        plt.xlim([0, 256])
        #plt.hist(img.ravel(), 256, [0, 256])
        #plt.show()

        # ...

        # POST-PROCESSOR
        result = {'result': 'size={}x{}'.format(img.shape[1], img.shape[0])}

        response_pickled = json.dumps({'data': result}, cls=NumpyEncoder)

        resp = Response(response=response_pickled, status=200, mimetype="application/json")
        resp.headers['Content-Type'] = 'application/json; charset=utf-8'
        resp.headers['Access-Control-Allow-Origin'] = '*'

        return resp

class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)
