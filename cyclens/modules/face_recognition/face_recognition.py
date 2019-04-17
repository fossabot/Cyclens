# coding: utf-8

from __future__ import unicode_literals

from ...common.module import Module
from ...common.path_system import create_folder_root, create_folder_id, check_folder_root, get_latest_folder_id, get_latest_face_id_from_folder_id, get_folder_count

import threading

import numpy as np
import tensorflow as tf

import cv2
import os
import json

from os.path import isfile

from .processor import FaceRecognitionPROC


class FaceRecognitionMD(Module):

    def __init__(self, ready=None):
        super(FaceRecognitionMD, self).__init__(ready)

        self.module_id = 3
        self.module_name = 'face_recognition'

        _ready = threading.Event()

        _ready.clear()
        self.processor = FaceRecognitionPROC(self, _ready)
        _ready.wait()

        self.DIR_STORE = '/tmp/cyclens/face-recognition/'

        self.CASC_FACE = None
        self.INCEPTION_MODEL = None
        self.INCEPTION_LABEL = None

        detection_model_path = '../data/models/detection/haarcascade_frontalface_default.xml'
        inception_model_path = '../data/models/inception/retrained_graph.pb'
        inception_label_path = '../data/models/inception/retrained_labels.txt'

        # FIXME: yolları sabit yap, train aşamasından sonra yeni .pb ve .txt oluşacak
        # EĞİTİM İÇİN:
        # python -m retrain
        # --output_graph=tf_files/retrained_graph.pb
        # --output_labels=tf_files/retrained_labels.txt
        # --architecture=inception_v3
        # --image_dir=tf_files/images
        # --how_many_training_steps=300
        # --summaries_dir=training_summaries/basic

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

        if isfile(detection_model_path):
            self.CASC_FACE = cv2.CascadeClassifier(detection_model_path)
            print("---> Face detection data set Loaded!!!")
        else:
            print("---> Couldn't find cascade model")
            exit(1)

        # FIXME: Her train aşamasından sonra bu dosyanın yeniden yüklenmesi gerekiyor...
        if isfile(inception_model_path):
            try:
                self.INCEPTION_MODEL = self.load_graph(inception_model_path)
                print("---> Inception v3 2015 model data set Loaded!!!")
            except:
                print("---> Inception v3 2015 model data set load ERROR!!!")
                exit(1)
        else:
            print("---> Couldn't find cascade model")
            exit(1)

        if isfile(inception_label_path):
            try:
                self.INCEPTION_LABEL = self.load_labels(inception_label_path)
                print("---> Inception v3 2015 label data set Loaded!!!")
            except:
                print("---> Inception v3 2015 label data set load ERROR!!!")
                exit(1)
        else:
            print("---> Couldn't find cascade model")
            exit(1)
        self._event_ready.set()

    def load_graph(self, file):
        graph = tf.Graph()
        graph_def = tf.GraphDef()

        with open(file, "rb") as f:
            graph_def.ParseFromString(f.read())
        with graph.as_default():
            tf.import_graph_def(graph_def)

        return graph

    def load_labels(self, file):
        label = []
        proto_as_ascii_lines = tf.gfile.GFile(file).readlines()
        for l in proto_as_ascii_lines:
            label.append(l.rstrip())
        return label

    # TODO: file_name kaldırılıp, oraya opencv image data type gelmeli
    # https://stackoverflow.com/a/42828577/5685796
    # # https://stackoverflow.com/a/46415482/5685796
    def read_tensor_from_image_file(self, file_name, input_height = 299, input_width = 299, input_mean = 0, input_std = 255):
        input_name = "file_reader"
        output_name = "normalized"
        file_reader = tf.read_file(file_name, input_name)

        if file_name.endswith(".png"):
            image_reader = tf.image.decode_png(file_reader, channels = 3, name = 'png_reader')
        elif file_name.endswith(".gif"):
            image_reader = tf.squeeze(tf.image.decode_gif(file_reader, name = 'gif_reader'))
        elif file_name.endswith(".bmp"):
            image_reader = tf.image.decode_bmp(file_reader, name = 'bmp_reader')
        else:
            image_reader = tf.image.decode_jpeg(file_reader, channels = 3, name = 'jpeg_reader')

        float_caster = tf.cast(image_reader, tf.float32)
        dims_expander = tf.expand_dims(float_caster, 0)
        resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
        normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
        sess = tf.Session()
        result = sess.run(normalized)

        return result

    def read_tensor_from_cv2(self, data, input_height = 299, input_width = 299, input_mean = 0, input_std = 255):
        float_caster = tf.cast(data, tf.float32)
        dims_expander = tf.expand_dims(float_caster, 0)
        resized = tf.image.resize_bilinear(dims_expander, [input_height, input_width])
        normalized = tf.divide(tf.subtract(resized, [input_mean]), [input_std])
        sess = tf.Session()
        result = sess.run(normalized)
        return result

    def run(self):
        super(FaceRecognitionMD, self).run()
        print("[MODULE::FACE_RECOGNITION]: run()")

        self.processor.start()

    def stop(self):
        super(FaceRecognitionMD, self).stop()

        self.processor.stop()

    def do_process(self, data):
        super(FaceRecognitionMD, self).do_process(data)
        print("[MODULE::FACE_RECOGNITION::DO_PROCESS]:")

        print("[MODULE::FACE_RECOGNITION::PIPELINE]: Sending to PROCESS Pipe")
        print("[MODULE::FACE_RECOGNITION::PROCESS]: [START]")
        data = self.processor.process(data)
        print("[MODULE::FACE_RECOGNITION::PROCESS]: [END] - Result: {}".format(data))

        return data

    # Gelen Face'leri Crop yap, işlemden geçir ve klasöre ekle
    def do_face_add(self, data):
        super(FaceRecognitionMD, self).do_process(data)
        print("[MODULE::FACE_RECOGNITION::FACE_ADD::DO_PROCESS]:")

        print("[MODULE::FACE_RECOGNITION::FACE_ADD::PIPELINE]: Sending to PROCESS Pipe")
        print("[MODULE::FACE_RECOGNITION::FACE_ADD::PROCESS]: [START]")

        result = {'success': True, 'message': 'null', 'folder_id': 0, 'face_id': 0}

        count = get_folder_count(self.DIR_STORE)
        print(count)

        if count == 0:
            create_folder_id(self.DIR_STORE, 1)

        last_id = get_latest_folder_id(self.DIR_STORE)
        result['folder_id'] = last_id

        if last_id == -1:
            result['message'] = "Folder id returns -1"
            result['success'] = False
        else:
            face_id = self.add_face_to_folder_id(data, last_id)
            result['face_id'] = face_id

            if face_id == -1:
                result['message'] = "Face id returns -1"
                result['success'] = False

        data = json.dumps(result)
        print("[MODULE::FACE_RECOGNITION::FACE_ADD::PROCESS]: [END] - Result: {}".format(data))

        return data

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
