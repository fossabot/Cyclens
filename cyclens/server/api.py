#!/usr/bin/env python
# coding: utf-8

"""
cyclens.server.api
~~~~~~~~~~~~~~~~~~

Implements Flask API with Tornado HTTPServer, WSGIContainer and IOLoop support.

This program comes with ABSOLUTELY NO WARRANTY; This is free software,
and you are welcome to redistribute it under certain conditions; See
file LICENSE, which is part of this source code package, for details.

:copyright: Copyright © 2019, The Cyclens Project
:license: MIT, see LICENSE for more details.
"""

from flask import Flask, Response, request

import cv2
import json
import asyncio
import threading
import numpy as np

from datetime import datetime
from matplotlib import pyplot as plt
from tornado.wsgi import WSGIContainer
from tornado.httpserver import HTTPServer
from tornado.ioloop import IOLoop


from ..common.preprocessor import get_date_now, get_date_str
from ..common.api import load_image_file

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
        def route_status():

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


        # NOT
        # - Yüzleri realtime olarak dosyalara koymak yerine, encoding'i alıp DB'ye koymak?
        # - Her modül CPU da ayrı bir Core üzerinde çalışsın?
        # - FR modülü için GPU destekli multiprocess özelliği?
        # - Yüzleri en baştan eğitmek yerine, her yüz eklemesi bitince kendi içinde train edilsin, diğer train dosyaları ile birleşsin eğer gerekiyorsa?
        # - Yüz resmini dosyaya kaydetmek yerine, dosyaya yüzün encoding'i kaydetmek?

        @self.api.route('/api/v1/demo/benchmark', methods = ['GET'])
        def route_benchmark():
            date_start = get_date_now()

            result = {'success': False, 'message': 'null', 'process': {'start': get_date_str(date_start), 'end': 0, 'total': 0}, 'round': 0, 'modules': []}

            imgs = [load_image_file('../test/images/benchmark/bruteforce_0.jpg'), load_image_file('../test/images/benchmark/bruteforce_1.jpeg'), load_image_file('../test/images/benchmark/bruteforce_2.jpeg')]

            TOTAL = 10

            result['round'] = TOTAL

            result = self.do_benchmark('age_prediction', imgs, result)
            result = self.do_benchmark('emotion_recognition', imgs, result)
            result = self.do_benchmark('face_recognition', imgs, result)
            result = self.do_benchmark('gender_prediction', imgs, result)

            date_end = get_date_now()
            ms_diff = (date_end - date_start).total_seconds() * 1000

            result['process']['end'] = get_date_str(date_end)
            result['process']['total'] = round(ms_diff, 2)

            res = json.dumps(result)

            return self.get_res(res)

        @self.api.route('/api/v1/demo/benchmark_single', methods = ['GET'])
        def route_benchmark_single():
            date_start = get_date_now()

            result = {'success': True, 'message': 'null', 'process': {'start': get_date_str(date_start), 'end': 0, 'total': 0}, 'round': 0, 'modules': []}

            imgs = [load_image_file('../test/images/benchmark/bruteforce_0.jpg'), load_image_file('../test/images/benchmark/bruteforce_1.jpeg'), load_image_file('../test/images/benchmark/bruteforce_2.jpeg')]

            TOTAL = 10

            result['round'] = TOTAL

            vals = {'success': True, 'face_processed': 0, 'ms_processed': 0}

            modules = {'age_prediction': vals, 'emotion_recognition': vals, 'face_recognition': vals, 'gender_prediction': vals}

            procs = {}

            for i in range(TOTAL):

                for j in range(0, len(imgs)):

                    proc = self.cyclens.process(imgs[j], False, True, True, True, True)

                    for res in proc['modules']:
                        name = res['module']
                        procs[name] = res['module']

                        faces = len(res['faces'])
                        ms = res['process']['total']
                        success = res['success']

                        modules[name]['face_processed'] += faces
                        modules[name]['ms_processed'] += ms
                        modules[name]['success'] = modules[name]['success'] and success

            date_end = get_date_now()

            for key, val in modules.items():
                module = {'module': key, 'success': True, 'FACES': 0, 'FPS': 0, 'MS': 0, 'MS_EST': 0, 'MS_STD': 0, 'MS_RMS': 0}

                success = modules[key]['success']

                face_processed = modules[key]['face_processed']
                ms_processed = modules[key]['ms_processed']

                if not success:
                    module['message'] = modules[key]['message']
                    continue

                if face_processed is not 0:
                    module['FACES'] = face_processed
                    module['FPS'] = round(1000 * face_processed / ms_processed, 2)
                    module['MS'] = round((date_end - date_start).total_seconds() * 1000)

                    mod = self.cyclens.get_module_by_name(procs[key])

                    module['MS_EST'] = mod.processor.get_response_time_estimated()
                    module['MS_STD'] = mod.processor.get_response_time_std()
                    module['MS_RMS'] = mod.processor.get_response_time_rms()
                else:
                    module['success'] = False
                    module['message'] = 'No faces to process'

                result['modules'].append(module)
                result['success'] = result['success'] and module['success']

            ms_diff = (date_end - date_start).total_seconds() * 1000

            result['process']['end'] = get_date_str(date_end)
            result['process']['total'] = round(ms_diff, 2)

            res = json.dumps(result)

            return self.get_res(res), 200

        @self.api.route('/api/v1/demo/single', methods = ['POST'])
        def route_single():
            ar = request.args.get('ar', type = bool) and request.values['ar'] == "true"  # Action Recognition
            ap = request.args.get('ap', type = bool) and request.values['ap'] == "true"  # Age Prediction
            er = request.args.get('er', type = bool) and request.values['er'] == "true"  # Emotion Recognition
            fr = request.args.get('fr', type = bool) and request.values['fr'] == "true"  # Face Recognition
            gp = request.args.get('gp', type = bool) and request.values['gp'] == "true"  # Gender Prediction

            img = self.get_img(request)

            if img is None:
                print(img)
                result = {'success': False, 'message': 'There is no image to process'}
                res = json.dumps(result)
                return self.get_res(res), 400

            result = self.cyclens.process(img, ar, ap, er, fr, gp)

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

            img = self.get_img(request)

            result = {'success': False, 'message': 'null', 'process': {'start': 0, 'end': 0, 'total': 0}, 'id': 0, 'limit': False, 'added': False}

            result = self.do_faceadd(img, id, name, result)

            print("[MODULE::FACE_RECOGNITION::FACE_ADD::PROCESS]: [END] - Requested: '{}', Result: {}".format(name, result))

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

    def do_benchmark(self, module_name, imgs, result):
        date_start = get_date_now()

        module = {'module': module_name, 'success': True, 'FACES': 0, 'FPS': 0, 'MS': 0, 'MS_EST': 0, 'MS_STD': 0, 'MS_RMS': 0}

        total_face_processed = 0
        total_ms_processed = 0

        if module_name == "age_prediction":
            mod = self.cyclens.module_ap
        elif module_name == "emotion_recognition":
            mod = self.cyclens.module_er
        elif module_name == "face_recognition":
            mod = self.cyclens.module_fr
        elif module_name == "gender_prediction":
            mod = self.cyclens.module_gp
        else:
            raise Exception('Unexpected module name: {}', module_name)

        for i in range(result['round']):

            for j in range(0, len(imgs)):

                proc = mod.do_process(imgs[j])

                proc_data = json.loads(proc)

                module['success'] = module['success'] and proc_data['success']

                total_face_processed += len(proc_data['faces'])
                total_ms_processed += proc_data['process']['total']

        date_end = get_date_now()

        if total_face_processed is not 0:
            module['FACES'] = total_face_processed
            module['FPS'] = round(1000 * total_face_processed / total_ms_processed, 2)
            module['MS'] = round((date_end - date_start).total_seconds() * 1000)
            module['MS_EST'] = mod.processor.get_response_time_estimated()
            module['MS_STD'] = mod.processor.get_response_time_std()
            module['MS_RMS'] = mod.processor.get_response_time_rms()
        else:
            module['success'] = False

        result['modules'].append(module)
        result['success'] = result['success'] and module['success']

        return result

    def do_faceadd(self, img, id, name, result):
        date_start = get_date_now()

        result['process']['start'] = get_date_str(date_start)

        # Eğer parametrede 'id' verilmemişse
        if id == -1:
            res = self.cyclens.module_fr.do_face_add_solr(img, name)
            if res['success']:
                folder_id = res['folder_id']
                result['id'] = folder_id
                result['success'] = True
            else:
                result['success'] = False
                result['message'] = res['message']

        # Eğer parametrede 'id' verilmişse
        elif id >= 0:
            res = self.cyclens.module_fr.do_face_add_solr(img, name)
            if res['success']:
                folder_id = res['folder_id']
                face_id = res['face_id']
                result['id'] = folder_id

                result['limit'] = res['limit']
                result['success'] = True

                exist_name = self.cyclens.module_fr.do_get_name_for_face_id(face_id)

                if exist_name == "unknown":
                    if name != "":
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

        return result

    def get_img(self, request):
        data = request.files['file'].read()

        npimg = np.frombuffer(data, np.uint8)

        if len(npimg) <= 0:
            return None

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
