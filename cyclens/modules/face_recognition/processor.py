# coding: utf-8

"""Processor functions for Face Recognition"""

from __future__ import unicode_literals

from ...common.preprocessor import div_255, get_date_now, get_date_str, crop_face
from ...common.processor import Processor
from ...common.api import load_image_file, face_locations, face_encodings, face_distance

import time
import json
import pysolr
import cv2
import sys


from ...utils import (
    ProcessingError,
)


class FaceRecognitionPROC(Processor):

    def __init__(self, module=None, ready=None):
        super(FaceRecognitionPROC, self).__init__(module, ready)

        self._event_ready.set()

    def run(self):
        super(FaceRecognitionPROC, self).run()
        return

    def stop(self):
        super(FaceRecognitionPROC, self).stop()
        print("[MODULE::FACE_RECOGNITION::PROC]: stop()")
        return

    def process2(self, data):
        super(FaceRecognitionPROC, self).process(data)

        date_start = get_date_now()

        result = {'module': 'face_recognition', 'success': False, 'message': 'null', 'process': {'start': get_date_str(date_start), 'end': 0, 'total': 0}, 'found': 0, 'rate': 0, 'faces': []}

        if data is None:
            result['success'] = False
            result['message'] = 'There is no data to process'
            return json.dumps(result)

        if self.MD.is_model_loading:
            result['success'] = False
            result['message'] = 'Module is busy to load new model...'
            return json.dumps(result)

        if not self.MD.is_model_loaded:
            result['success'] = False
            result['message'] = 'Module is disabled until KNN model is loaded...'
            return json.dumps(result)

        image_rgb = cv2.cvtColor(data, cv2.COLOR_BGR2RGB)

        x_face_locations = face_locations(image_rgb)

        result['found'] = len(x_face_locations)

        if len(x_face_locations) <= 0:
            result['success'] = False
            result['message'] = 'There is no face to process'
            return json.dumps(result)

        print("[MODULE::FACE_RECOGNITION::RESULT]=====================================================================================")
        print("Total faces found: {}".format(len(x_face_locations)))

        distance_threshold = 0.6

        total_success_count = 0

        #try:

        if len(x_face_locations) > 0:

            # Find encodings for faces in the test iamge
            faces_encodings = face_encodings(image_rgb, known_face_locations = x_face_locations)

            # Use the KNN model to find the best matches for the test face
            closest_distances = self.MD.KNN_CLF.kneighbors(faces_encodings, n_neighbors = 1)

            are_matches = [closest_distances[0][i][0] <= distance_threshold for i in range(len(x_face_locations))]

            # Predict classes and remove classifications that aren't within the threshold
            matched_faces = [(pred, loc) if rec else ("unknown", loc) for pred, loc, rec in zip(self.MD.KNN_CLF.predict(faces_encodings), x_face_locations, are_matches)]

            if len(matched_faces) == 0:
                result['message'] = 'There are no matched faces'

            else:

                for i, face in enumerate(matched_faces):
                    [pred, loc] = face
                    [y, right, bottom, x] = loc

                    name = pred

                    try:
                        id = int(name)
                        name = self.MD.do_get_name_for_face_id(id)
                    except:
                        name = "unknown"

                    dist = round(closest_distances[0][i][0], 2)

                    result_face = {'id': i, 'x': int(x), 'y': int(y), 'bottom': int(bottom), 'right': int(right), 'distance': dist, 'result': name, 'success': True}
                    result['faces'].append(result_face)

                    total_success_count += 1

        if total_success_count != len(x_face_locations):
            msg = 'There are {} faces but {} faces processed successfully. Please check what (tf) is going on!'.format(len(x_face_locations), total_success_count)
            result['message'] = msg
            print(msg)

        rate = len(x_face_locations) / total_success_count * 100

        print("Processing success rate: %{}".format(rate))

        result['rate'] = rate
        result['success'] = True
        self.process_successes += 1
        #except:
        #    result['success'] = False
        #    result['message'] = 'TRY-EXCEPT'
        #    self.process_fails += 1

        self.total_processed += 1

        date_end = get_date_now()

        ms_diff = (date_end - date_start).total_seconds() * 1000

        self.response_times.append(ms_diff)

        result['process']['end'] = get_date_str(date_end)
        result['process']['total'] = round(ms_diff, 2)

        print("===========================================================================================")

        self.is_busy = False

        return json.dumps(result)

    def process(self, data):
        super(FaceRecognitionPROC, self).process(data)

        total_success_count = 0

        date_start_locations = get_date_now()
        x_face_locations = face_locations(data['frame_rgb'])
        date_end_locations = get_date_now()

        data['process']['locations'] = round((date_end_locations - date_start_locations).total_seconds() * 1000, 2)

        data['found'] = len(x_face_locations)

        if len(x_face_locations) <= 0:
            data['success'] = False
            data['message'] = 'There is no face to process'
            return data

        print("[MODULE::FACE_RECOGNITION::RESULT]=====================================================================================")
        print("Total faces found: {}".format(len(x_face_locations)))

        distance_threshold = 0.5

        try:
            if len(x_face_locations) >= 1:

                process_ms_encodings = 0
                process_ms_searches = 0

                top_name = ''
                top_dist = 1.0

                for i in range(len(x_face_locations)):

                    # Find encodings for faces in the test iamge

                    date_start_encodings = get_date_now()
                    faces_encodings = face_encodings(data['frame_rgb'], known_face_locations = x_face_locations)[i]
                    date_end_encodings = get_date_now()

                    process_ms_encodings += round((date_end_encodings - date_start_encodings).total_seconds() * 1000, 2)

                    query = self.MD.SOLR_QUERY_DIST

                    for i, val in enumerate(faces_encodings):
                        query += '{},'.format(str(val))

                    query += ')'

                    date_start_search = get_date_now()
                    searches = self.MD.SOLR.search(q = '*:*', sort = query + ' asc', fl = 'name,' + query)
                    date_end_search = get_date_now()

                    process_ms_searches += round((date_end_search - date_start_search).total_seconds() * 1000, 2)

                    # if searches query result != 0 ->
                    total_success_count += 1

                    # TODO: searches 0. mı?
                    # FIXME: for 1 kez dönüyor tek face için
                    for search in searches:
                        try:
                            name = search['name']
                            dist = round(1.0 - search[query], 2)
                        except KeyError as e:
                            name = 'unknown'
                            dist = 10.0

                        result_face = {'result': name, 'confidence': dist}
                        data['faces'].append(result_face)

                        if dist < top_dist:
                            top_dist = dist
                            top_name = name
                        if dist >= distance_threshold:
                            data['result'] = top_name

                data['process']['encodings'] = process_ms_encodings
                data['process']['search'] = process_ms_searches

            if total_success_count != data['found']:
                msg = 'There are {} faces but {} faces processed successfully. Please check what (tf) is going on!'.format(data['found'], total_success_count)
                data['message'] = msg

            rate = data['found'] / total_success_count * 100

            data['rate'] = rate
            data['success'] = True
            self.process_successes += 1
        except pysolr.SolrError as e:
            data['success'] = False
            data['message'] = str(e)
            self.process_fails += 1
        except:
            data['success'] = False
            data['message'] = ('Type: {}, Message: TRY-EXCEPT', sys.exc_info()[0])
            self.process_fails += 1

        self.total_processed += 1

        self.is_busy = False

        return data
