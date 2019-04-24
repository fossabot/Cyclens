#!/usr/bin/env python
# coding: utf-8

from flask import Flask, Response, render_template, jsonify, request

from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop

import asyncio

from ..common.preprocessor import get_date_now, get_date_str

from datetime import datetime

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

    def __init__(self, cyclens, ready=None):
        threading.Thread.__init__(self)

        self.cyclens = cyclens

        self.HOST = 'localhost'
        self.PORT = 5000

        self.add_routes()

        ready.set()

    def run(self):
        self.start_api(debug=False, host=self.HOST, port=self.PORT)

    def start_api(self, debug, host, port):
        #Tonado: non-blocking, asynchronous
        asyncio.set_event_loop(asyncio.new_event_loop())
        http_server = HTTPServer(WSGIContainer(self.api))
        http_server.listen(port)
        IOLoop.instance().start()

    def stop(self):
        try:
            func = request.environ.get('werkzeug.server.shutdown')
            if func is None:
                raise RuntimeError('Not running with the Werkzeug Server')
            func()
        except:
            print("API shutdown error...")

    def is_running(self):
        return True

    # Test: curl -i -X POST -H "Content-Type: multipart/form-data" -F "file=@/home/dentrax/Pictures/Wallpapers/wp1.jpg" http://localhost:5000/test/demo
    # Test: curl -F "file=@/home/dentrax/Pictures/Wallpapers/wp1.jpg" http://localhost:5000/test/demo
    def add_routes(self):


        @self.api.route('/api/v1/demo/ping', methods = ['GET'])
        def route_ping():
            result = {'type': 'ping', 'result': 'pong', 'date': 0}

            result['date'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S.%f')

            res = json.dumps(result)

            return self.get_res(res)

        @self.api.route('/api/v1/demo/status', methods = ['GET'])
        def status():

            result = {'type': 'status', 'modules': []}

            result_ar = {'id': self.cyclens.module_ar.get_id(),
                         'name': self.cyclens.module_ar.get_name(),
                         'is_available': self.cyclens.module_ar.processor.is_available(),
                         'is_running': self.cyclens.module_ar.is_running,
                         'is_processor_running': self.cyclens.module_ar.processor.is_running,
                         'total_processed': self.cyclens.module_ar.processor.get_total_processed(),
                         'process_fails': self.cyclens.module_ar.processor.get_process_fails(),
                         'process_successes': self.cyclens.module_ar.processor.get_process_successes(),
                         'average_crash_rate': self.cyclens.module_ar.processor.get_average_crash_rate(),
                         'response_time_estimated': self.cyclens.module_ar.processor.get_response_time_estimated(),
                         'response_time_std': self.cyclens.module_ar.processor.get_response_time_std(),
                         'response_time_rms': self.cyclens.module_ar.processor.get_response_time_rms()}

            result['modules'].append(result_ar)

            result_ap = {'id': self.cyclens.module_ap.get_id(),
                         'name': self.cyclens.module_ap.get_name(),
                         'is_available': self.cyclens.module_ap.processor.is_available(),
                         'is_running': self.cyclens.module_ap.is_running,
                         'is_processor_running': self.cyclens.module_ap.processor.is_running,
                         'total_processed': self.cyclens.module_ap.processor.get_total_processed(),
                         'process_fails': self.cyclens.module_ap.processor.get_process_fails(),
                         'process_successes': self.cyclens.module_ap.processor.get_process_successes(),
                         'average_crash_rate': self.cyclens.module_ap.processor.get_average_crash_rate(),
                         'response_time_estimated': self.cyclens.module_ap.processor.get_response_time_estimated(),
                         'response_time_std': self.cyclens.module_ap.processor.get_response_time_std(),
                         'response_time_rms': self.cyclens.module_ap.processor.get_response_time_rms()}

            result['modules'].append(result_ap)

            result_er = {'id': self.cyclens.module_er.get_id(),
                         'name': self.cyclens.module_er.get_name(),
                         'is_available': self.cyclens.module_er.processor.is_available(),
                         'is_running': self.cyclens.module_er.is_running,
                         'is_processor_running': self.cyclens.module_er.processor.is_running,
                         'total_processed': self.cyclens.module_er.processor.get_total_processed(),
                         'process_fails': self.cyclens.module_er.processor.get_process_fails(),
                         'process_successes': self.cyclens.module_er.processor.get_process_successes(),
                         'average_crash_rate': self.cyclens.module_er.processor.get_average_crash_rate(),
                         'response_time_estimated': self.cyclens.module_er.processor.get_response_time_estimated(),
                         'response_time_std': self.cyclens.module_er.processor.get_response_time_std(),
                         'response_time_rms': self.cyclens.module_er.processor.get_response_time_rms()}

            result['modules'].append(result_er)

            result_fr = {'id': self.cyclens.module_fr.get_id(),
                         'name': self.cyclens.module_fr.get_name(),
                         'is_available': self.cyclens.module_fr.processor.is_available(),
                         'is_running': self.cyclens.module_fr.is_running,
                         'is_processor_running': self.cyclens.module_fr.processor.is_running,
                         'total_processed': self.cyclens.module_fr.processor.get_total_processed(),
                         'process_fails': self.cyclens.module_fr.processor.get_process_fails(),
                         'process_successes': self.cyclens.module_fr.processor.get_process_successes(),
                         'average_crash_rate': self.cyclens.module_fr.processor.get_average_crash_rate(),
                         'response_time_estimated': self.cyclens.module_fr.processor.get_response_time_estimated(),
                         'response_time_std': self.cyclens.module_fr.processor.get_response_time_std(),
                         'response_time_rms': self.cyclens.module_fr.processor.get_response_time_rms()}

            result['modules'].append(result_fr)

            result_gp = {'id': self.cyclens.module_gp.get_id(),
                         'name': self.cyclens.module_gp.get_name(),
                         'is_available': self.cyclens.module_gp.processor.is_available(),
                         'is_running': self.cyclens.module_gp.is_running,
                         'is_processor_running': self.cyclens.module_gp.processor.is_running,
                         'total_processed': self.cyclens.module_gp.processor.get_total_processed(),
                         'process_fails': self.cyclens.module_gp.processor.get_process_fails(),
                         'process_successes': self.cyclens.module_gp.processor.get_process_successes(),
                         'average_crash_rate': self.cyclens.module_gp.processor.get_average_crash_rate(),
                         'response_time_estimated': self.cyclens.module_gp.processor.get_response_time_estimated(),
                         'response_time_std': self.cyclens.module_gp.processor.get_response_time_std(),
                         'response_time_rms': self.cyclens.module_gp.processor.get_response_time_rms()}

            result['modules'].append(result_gp)

            res = json.dumps(result)

            return self.get_res(res)

        @self.api.route('/api/v1/demo/single', methods = ['POST'])
        def route_single():
            ar = request.args.get('ar', default = False, type = bool)  # Action Recognition
            ap = request.args.get('ap', default = False, type = bool)  # Age Prediction
            er = request.args.get('er', default = False, type = bool)  # Emotion Recognition
            fr = request.args.get('fr', default = False, type = bool)  # Face Recognition
            gp = request.args.get('gp', default = False, type = bool)  # Gender Prediction

            date_start = get_date_now()

            img = self.get_img(request)

            result = {'success': False, 'message': 'null', 'process': {'start': get_date_str(date_start), 'end': 0, 'total': 0}, 'modules': []}

            try:
                flag = False

                if ar:
                    proc_ar = self.cyclens.module_ar.do_process(img)
                    proc_data_ar = json.loads(proc_ar)
                    result['modules'].append(proc_data_ar)
                    flag = True

                if ap:
                    proc_ap = self.cyclens.module_ap.do_process(img)
                    proc_data_ap = json.loads(proc_ap)
                    result['modules'].append(proc_data_ap)
                    flag = True

                if er:
                    proc_er = self.cyclens.module_er.do_process(img)
                    proc_data_er = json.loads(proc_er)
                    result['modules'].append(proc_data_er)
                    flag = True

                if fr:
                    proc_fr = self.cyclens.module_fr.do_process(img)
                    proc_data_fr = json.loads(proc_fr)
                    result['modules'].append(proc_data_fr)
                    flag = True

                if gp:
                    proc_gp = self.cyclens.module_gp.do_process(img)
                    proc_data_gp = json.loads(proc_gp)
                    result['modules'].append(proc_data_gp)
                    flag = True

                if flag is False:
                    result['message'] = 'No modules are selected to be processed'

                result['success'] = True
            except:
                result['success'] = False
                result['message'] = 'API TRY-EXCEPT!!!'

            date_end = get_date_now()

            ms_diff = (date_end - date_start).total_seconds() * 1000

            result['process']['end'] = get_date_str(date_end)
            result['process']['total'] = round(ms_diff, 2)

            res = json.dumps(result)

            return self.get_res(res)

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

        @self.api.route('/api/v1/demo/face_add', methods = ['POST'])
        def route_face_add():
            id = request.args.get('id', default = -1, type = int)
            name = request.args.get('name', default = "", type = str)

            date_start = get_date_now()

            img = self.get_img(request)

            result = {'success': False, 'message': 'null', 'process': {'start': get_date_str(date_start), 'end': 0, 'total': 0}, 'id': 0, 'limit': False, 'added': False}

            # Eğer parametrede 'id' verilmemişse
            if id == -1:
                res = self.cyclens.module_fr.do_face_add(img, -1)
                if res['success']:
                    folder_id = res['folder_id']
                    result['id'] = folder_id
                    result['success'] = True
                else:
                    result['success'] = False
                    result['message'] = res['message']

            # Eğer parametrede 'id' verilmişse
            elif id >= 0:
                res = self.cyclens.module_fr.do_face_add(img, id)
                if res['success']:
                    folder_id = res['folder_id']
                    face_id = res['face_id']
                    result['id'] = folder_id

                    result['limit'] = res['limit']
                    result['success'] = True

                    exist_name = self.cyclens.module_fr.do_get_name_for_face_id(face_id)

                    if exist_name is "":
                        if name is not "":
                            r = self.cyclens.module_fr.do_set_name_for_face_id(face_id)
                            result['added'] = r

                else:
                    result['success'] = False
                    result['message'] = res['message']
            else:
                result['success'] = False
                result['message'] = 'Given ID should be greater than zero'

            date_end = get_date_now()

            ms_diff = (date_end - date_start).total_seconds() * 1000

            result['process']['end'] = get_date_str(date_end)
            result['process']['total'] = round(ms_diff, 2)

            print("[MODULE::FACE_RECOGNITION::FACE_ADD::PROCESS]: [END] - Result: {}".format(result))

            res = json.dumps(result)
            return self.get_res(res)

        @self.api.route('/api/v1/demo/face_train', methods = ['GET'])
        def route_face_train():
            res = self.cyclens.module_fr.do_face_train()
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
