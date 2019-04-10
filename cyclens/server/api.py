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

    def __init__(self, cyclens):
        print("[API]: __init__")
        threading.Thread.__init__(self)

        self.cyclens = cyclens

    def run(self):
        self.add_routes()
        self.start_api(debug=False, host="localhost", port=5000)
        print("[API]: run")

    def start_api(self, debug, host, port):
        print("[API]: start")
        #Tonado: non-blocking, asynchronous 
        asyncio.set_event_loop(asyncio.new_event_loop())
        http_server = HTTPServer(WSGIContainer(self.api))
        http_server.listen(port)
        IOLoop.instance().start()

    def is_running(self):
        return True

    # Test: curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@/home/dentrax/Pictures/Wallpapers/wp1.jpg" http://localhost:5000/test/demo
    # Test: curl -F "file=@/home/dentrax/Pictures/Wallpapers/wp1.jpg" http://localhost:5000/test/demo
    def add_routes(self):
        print("[API]: Add routes")

        @self.api.route('/api/v1/demo/action', methods = ['POST'])
        def route_action():
            img = self.get_img(request)
            res = self.cyclens.module_ar.do_process(img)
            return self.get_res(res)

        @self.api.route('/api/v1/demo/age', methods = ['POST'])
        def route_age():
            img = self.get_img(request)
            res = self.cyclens.module_ap.do_process(img)
            return self.get_res(res)

        @self.api.route('/api/v1/demo/emotion', methods=['POST'])
        def route_emotion():
            img = self.get_img(request)
            res = self.cyclens.module_er.do_process(img)

            return self.get_res(res)

        @self.api.route('/api/v1/demo/face', methods = ['POST'])
        def route_face():
            img = self.get_img(request)
            res = self.cyclens.module_fr.do_process(img)
            return self.get_res(res)

        @self.api.route('/api/v1/demo/gender', methods = ['POST'])
        def route_gender():
            img = self.get_img(request)
            res = self.cyclens.module_gp.do_process(img)
            return self.get_res(res)


    def get_img(self, request):
        data = request.files['file'].read()
        npimg = np.frombuffer(data, np.uint8)
        img = cv2.imdecode(npimg, cv2.IMREAD_COLOR)

        return img

    def get_res(self, res):
        resp = Response(response = res, status = 200, mimetype = "application/json")
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
