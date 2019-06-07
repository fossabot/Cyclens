#!/usr/bin/env python
# coding: utf-8

"""
cyclens
~~~~~~~

Real-time camera client demo for Cyclens

This program comes with ABSOLUTELY NO WARRANTY; This is free software,
and you are welcome to redistribute it under certain conditions; See
file LICENSE, which is part of this source code package, for details.

:copyright: Copyright © 2019, The Cyclens Project
:license: MIT, see LICENSE for more details.
"""

import cv2 as cv2
import json
import requests
import time
import numpy

from pathlib import Path

base_path = Path(__file__).parent.parent

WIDTH = 600
HEIGHT = 480

cap = cv2.VideoCapture(0)

cam_w = cap.set(cv2.CAP_PROP_FRAME_WIDTH, WIDTH)
cam_h = cap.set(cv2.CAP_PROP_FRAME_HEIGHT, HEIGHT)

faceCascade = cv2.CascadeClassifier(str((base_path / "./data/models/detection/haarcascade_frontalface_default.xml").resolve()))

res = {}

tmp_time = time.time()
fps_list = []

font = cv2.FONT_HERSHEY_SIMPLEX


def get_response(image):
    url = 'http://localhost:5000/api/v1/demo/single'
    files = {'file': image}
    params = {'ap': 'true', 'er': 'true', 'fr': 'true', 'gp': 'true'}

    return requests.post(url, params = params, files = files)


while cap.isOpened():

    ok, frame = cap.read()

    if not ok:
        break

    _, image = cv2.imencode('.jpg', frame)

    response = get_response(image)

    res = json.loads(response.text)

    if res['success']:

        delay = time.time() - tmp_time
        tmp_time = time.time()
        fps_list.append(delay)

        fps = len(fps_list) / numpy.sum(fps_list)

        cv2.putText(frame, ('FPS: %.2f' % fps), (0, 20), font, 0.5, (200, 255, 155))

        faces = faceCascade.detectMultiScale(
            frame,
            scaleFactor = 1.1,
            minNeighbors = 5,
            minSize = (30, 30),
            flags = cv2.CASCADE_SCALE_IMAGE
        )

        # Draw a rectangle around the faces
        for (x, y, w, h) in faces:

            cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 255, 0), 2)

            z = ''

            for m in res['modules']:
                n = m['module']

                top_conf = 0.0
                top_result = ''

                for n in range(len(m['faces'])):
                    conf = m['faces'][n]['confidence']
                    result = m['faces'][n]['result']

                    if conf > top_conf:
                        top_conf = conf
                        top_result = result

                z += str(top_result) + ', '

            cv2.putText(frame, z, (x, y + 20), font, 0.5, (200, 255, 155))

    cv2.imshow('DEMO', frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        cap.release()
        break

cv2.destroyAllWindows()
