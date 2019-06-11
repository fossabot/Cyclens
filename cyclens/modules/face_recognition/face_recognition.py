# coding: utf-8

"""
cyclens.modules.face_recognition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implements 'FACE RECOGNITION' module

This program comes with ABSOLUTELY NO WARRANTY; This is free software,
and you are welcome to redistribute it under certain conditions; See
file LICENSE, which is part of this source code package, for details.

:copyright: Copyright © 2019, The Cyclens Project
:license: MIT, see LICENSE for more details.
"""


from __future__ import unicode_literals



import threading

import numpy as np
import tensorflow as tf

import cv2
import os
import json
import pickle
import pysolr
import math
import re
import threading
import urllib.request
import urllib.error

from os.path import isfile
from sklearn import neighbors

from .processor import FaceRecognitionPROC

from ...common.module import Module
from ...common.path_system import create_folder_root, create_folder_id, check_folder_root, get_latest_folder_id, get_latest_face_id_from_folder_id, get_folder_count
from ...common.api import load_image_file, face_locations, face_encodings
from ...constants import SOLR_URL


class FaceRecognitionMD(Module):

    SOLR_VALUE_PREFIX = 'v_'

    def __init__(self, ready=None):
        super(FaceRecognitionMD, self).__init__(ready)

        self.module_id = 3
        self.module_name = 'face_recognition'

        _ready = threading.Event()

        _ready.clear()
        self.processor = FaceRecognitionPROC(self, _ready)
        _ready.wait()

        self.DIR_STORE = '/tmp/cyclens/face-recognition/'
        self.DIR_MODEL_SAVE_PATH = '/tmp/cyclens/data/'
        self.DIR_KNN_MODEL = '/tmp/cyclens/data/trained_knn_model.clf'

        self.CASC_FACE = None
        self.KNN_CLF = None
        self.INCEPTION_LABEL = None

        # KNN modeli yükleniyor mu
        self.is_model_loading = False

        # KNN modeli doğru bir şekilde yüklenmiş mi
        self.is_model_loaded = False

        detection_model_path = '../data/models/detection/haarcascade_frontalface_default.xml'
        knn_model_path = '../data/models/face/trained_knn_model.clf'

        # TODO: if server down and 400 code handling
        self.SOLR = pysolr.Solr(SOLR_URL, always_commit=True, timeout=1)

        ping_url = '{}/admin/ping'.format(SOLR_URL)

        try:
            ping = urllib.request.urlopen(ping_url).read()

            ping_res = json.loads(ping)

            if ping_res['status'] == 'OK':
                print("---> Solr service is working!!!")
            else:
                print("---> Couldn't ping to the Solr service")
                exit(1)

        except urllib.error.HTTPError as e:
            print('Solr::HTTPError: {}'.format(e.code))
            exit(1)
        except urllib.error.URLError as e:
            print('Solr::URLError: {}'.format(e.reason))
            exit(1)

        self.SOLR_QUERY_DIST = 'dist(2,'
        for i in range(0, 128):
            self.SOLR_QUERY_DIST += 'v_{},'.format(str(i))

        if not check_folder_root(self.DIR_STORE):
            if create_folder_root(self.DIR_STORE):
                print("---> Face recognition data path created!!!")
            else:
                print("---> Couldn't create face recognition root path")
                exit(1)
        else:
            last = get_latest_folder_id(self.DIR_STORE)
            count = get_folder_count(self.DIR_STORE)
            print("---> Total Folder Count: {}, Latest Folder ID: {}".format(count, last))
            print("---> Face recognition data path exist!!!")

        if not check_folder_root(self.DIR_MODEL_SAVE_PATH):
            if create_folder_root(self.DIR_MODEL_SAVE_PATH):
                print("---> Face recognition model data path created!!!")
            else:
                print("---> Couldn't create face recognition root path")
                exit(1)

        if isfile(detection_model_path):
            self.CASC_FACE = cv2.CascadeClassifier(detection_model_path)
            print("---> Face detection data set Loaded!!!")
        else:
            print("---> Couldn't find detection_model_path")
            exit(1)

        # FIXME: Her train aşamasından sonra bu dosyanın yeniden yüklenmesi gerekiyor...
        if isfile(self.DIR_KNN_MODEL):
            try:
                with open(self.DIR_KNN_MODEL, 'rb') as f:
                    self.KNN_CLF = pickle.load(f)

                self.is_model_loaded = self.KNN_CLF is not None
                print("---> Face recognition model data set Loaded!!!")
            except:
                self.is_model_loaded = False
        else:
            self.is_model_loaded = False

        self._event_ready.set()

    def try_load_knn_model(self, knn_model_path):
        if isfile(knn_model_path):
            try:
                self.is_model_loading = True

                with open(knn_model_path, 'rb') as f:
                    self.KNN_CLF = pickle.load(f)

                self.is_model_loading = False
                self.is_model_loaded = self.KNN_CLF is not None
                return True
            except:
                self.is_model_loaded = False
                return False
        else:
            self.is_model_loaded = False
            return False

    # Ref: https://github.com/ageitgey/face_recognition/blob/master/examples/face_recognition_knn.py
    def try_train_knn_model(self, n_neighbors=None, knn_algo='ball_tree', verbose=False):
        X = []
        y = []

        # Loop through each person in the training set
        for class_dir in os.listdir(self.DIR_STORE):
            if not os.path.isdir(os.path.join(self.DIR_STORE, class_dir)):
                continue

            # Loop through each training image for the current person
            for img_path in self.get_image_files_in_folder(os.path.join(self.DIR_STORE, class_dir)):
                image = load_image_file(img_path)
                face_bounding_boxes = face_locations(image)

                if len(face_bounding_boxes) != 1:
                    # If there are no people (or too many people) in a training image, skip the image.
                    if verbose:
                        print("Image {} not suitable for training: {}".format(img_path, "Didn't find a face" if len(face_bounding_boxes) < 1 else "Found more than one face"))
                else:
                    # Add face encoding for current image to the training set
                    X.append(face_encodings(image, known_face_locations = face_bounding_boxes)[0])
                    y.append(class_dir)

        # Determine how many neighbors to use for weighting in the KNN classifier
        if n_neighbors is None:
            n_neighbors = int(round(math.sqrt(len(X))))
            if verbose:
                print("Chose n_neighbors automatically:", n_neighbors)

        # Create and train the KNN classifier
        knn_clf = neighbors.KNeighborsClassifier(n_neighbors = n_neighbors, algorithm = knn_algo, weights = 'distance')
        knn_clf.fit(X, y)

        if not check_folder_root(self.DIR_MODEL_SAVE_PATH):
            if create_folder_root(self.DIR_MODEL_SAVE_PATH):
                print("---> Face recognition model data path created!!!")
            else:
                print("---> Couldn't create face recognition data path")

        # Save the trained KNN classifier
        if self.DIR_KNN_MODEL is not None:
            with open(self.DIR_KNN_MODEL, 'wb') as f:
                pickle.dump(knn_clf, f)

        return knn_clf

    def run(self):
        super(FaceRecognitionMD, self).run()
        print("[MODULE::FACE_RECOGNITION]: run()")

        self.processor.start()

    def stop(self):
        super(FaceRecognitionMD, self).stop()

        self.processor.stop()

    async def do_process(self, data):
        super(FaceRecognitionMD, self).do_process(data)
        return self.processor.process(data)

    # Gelen Face'leri Crop yap, işlemden geçir ve klasöre ekle
    def do_face_add(self, data, id):
        print("[MODULE::FACE_RECOGNITION::FACE_ADD::DO_FACE_ADD]:")

        print("[MODULE::FACE_RECOGNITION::FACE_ADD::PIPELINE]: Sending to PROCESS Pipe")
        print("[MODULE::FACE_RECOGNITION::FACE_ADD::PROCESS]: [START]")

        result = {'success': True, 'message': 'null', 'folder_id': 0, 'face_id': 0, 'limit': False}

        if not check_folder_root(self.DIR_STORE):
            create_folder_root(self.DIR_STORE)

        count = get_folder_count(self.DIR_STORE)

        if count == 0 and id == -1:
            create_folder_id(self.DIR_STORE, 0)

            face_id = self.add_face_to_folder_id(data, 0)
            result['folder_id'] = 0
            result['face_id'] = 0

        elif count == 0 and id >= 0:
            result['message'] = "There are no folders but 'id' is greater than zero"
            result['success'] = False

        elif count > 0:

            last_id = get_latest_folder_id(self.DIR_STORE)

            if last_id == -1:
                result['message'] = "Failed to get latest folder id"
                result['success'] = False

            else:

                if last_id < id:
                    result['message'] = "ID cannot be more than latest folder ID, post 'face_add' first!"
                    result['success'] = False

                else:
                    new_id = last_id + 1

                    if id >= 0:
                        new_id = id

                    create_folder_id(self.DIR_STORE, new_id)

                    FACE_LIMIT = 2

                    is_face_limit = get_latest_face_id_from_folder_id(self.DIR_STORE, new_id) >= FACE_LIMIT

                    result['folder_id'] = new_id

                    if not is_face_limit:

                        face_id = self.add_face_to_folder_id(data, new_id)

                        result['face_id'] = face_id

                        if face_id == -1:
                            result['message'] = "Face id returns -1"
                            result['success'] = False

                    else:
                        result['message'] = "Reached to face limit for id"
                        result['limit'] = True

        return

    def do_face_add_solr(self, data, name):

        result = {'success': True, 'message': 'null', 'found': 0, 'folder_id': 0, 'face_id': 0, 'limit': False}

        image_rgb = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)

        x_face_locations = face_locations(image_rgb)

        result['found'] = len(x_face_locations)

        if len(x_face_locations) <= 0:
            result['success'] = False
            result['message'] = 'There is no face to process'
            return json.dumps(result)

        if len(x_face_locations) > 1:
            result['success'] = False
            result['message'] = 'There are more than one face!'
            return json.dumps(result)

        if len(x_face_locations) == 1:

            data_solr = {}

            # Find encodings for faces in the face
            faces_encodings = face_encodings(image_rgb, known_face_locations = x_face_locations)[0]

            # Use the Apache Solr to add the face

            if name is "":
                name = "unknown"

            data_solr['name'] = name

            for i, val in enumerate(faces_encodings):
                idx = '{}{}'.format(self.SOLR_VALUE_PREFIX, str(i))
                data_solr[idx] = val

            try:
                self.SOLR.add([data_solr])
                result['success'] = True
            except pysolr.SolrError as e:
                result['success'] = False
                result['message'] = str(e)

        return result

    # Verilen Face ID için DB'den Name çekme fonksiyonu
    def do_set_name_for_face_id(self, id):
        # TODO: DB operations

        return True

    # Verilen Face ID için DB'den Name çekme fonksiyonu
    def do_get_name_for_face_id(self, id):
        # TODO: DB operations

        if id == 0:
            return "Barbara Palvin"
        elif id == 1:
            return "Benedict Cumberbatch"
        elif id == 2:
            return "Christian Bale"
        elif id == 3:
            return "Johnny Depp"
        elif id == 4:
            return "Margot Robbie"
        elif id == 5:
            return "Scarlett Johansson"

        return "unknown"

    # Train etmek için
    def do_face_train(self):
        print("[MODULE::FACE_RECOGNITION::FACE_TRAIN::DO_FACE_TRAIN]:")

        print("[MODULE::FACE_RECOGNITION::FACE_TRAIN::PIPELINE]: Sending to PROCESS Pipe")
        print("[MODULE::FACE_RECOGNITION::FACE_TRAIN::PROCESS]: [START]")

        result = {'success': False, 'message': 'null'}

        # FIXME: n_neighbors sayısı aynı kişi için kaç sampling var onu yaz!!!!!!!!!!!!!!!!!!
        ok = self.try_train_knn_model(n_neighbors = 2, knn_algo = 'ball_tree', verbose = True)

        if ok:
            reload = self.try_load_knn_model(self.DIR_KNN_MODEL)
            if reload:
                result['success'] = True
            else:
                result['message'] = "KNN model reload failed"
        else:
            result['message'] = "KNN model train failed"

        data = json.dumps(result)
        print("[MODULE::FACE_RECOGNITION::FACE_TRAIN::PROCESS]: [END] - Result: {}".format(data))

        return data

    def get_image_files_in_folder(self, folder):
        return [os.path.join(folder, f) for f in os.listdir(folder) if re.match(r'.*\.(jpg|jpeg|png)', f, flags = re.I)]

    def add_face_to_folder_id(self, face, folder_id):

        id = get_latest_face_id_from_folder_id(self.DIR_STORE, folder_id) + 1
        if id >= 0:
            cv2.imwrite(os.path.join('{}/{}/'.format(self.DIR_STORE, folder_id), '{}.jpg'.format(id)), face)
            return id
        return -1

    def print_debug(self, data):
        super(FaceRecognitionMD, self).print_debug(data)
        return

    def print_log(self, data):
        super(FaceRecognitionMD, self).print_log(data)
        return
