# coding: utf-8

"""
cyclens.modules.face_recognition
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implements processor engine for 'FACE RECOGNITION' module

This program comes with ABSOLUTELY NO WARRANTY; This is free software,
and you are welcome to redistribute it under certain conditions; See
file LICENSE, which is part of this source code package, for details.

:copyright: Copyright © 2019, The Cyclens Project
:license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals

import json
import pysolr
import cv2
import sys

from ...common.preprocessor import get_date_now, get_date_str
from ...common.processor import Processor
from ...common.api import face_locations, face_encodings


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

    def process(self, data):
        super(FaceRecognitionPROC, self).process(data)

        data['module'] = self.MD.module_name

        distance_threshold = 0.6

        total_success_count = 0

        if data['found'] > 0:

            #try:

            process_ms_encodings = 0
            process_ms_searches = 0

            for i in range(len(data['frame_faces'])):

                # Find encodings for faces in the test iamge

                date_start_encodings = get_date_now()
                faces_encodings = face_encodings(data['frame_rgb'], known_face_locations = data['frame_faces'])[i]
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

                # TODO: if searches query result != 0 ->
                total_success_count += 1

                top_name = ''
                top_dist = 0.0

                for search in searches:
                    try:
                        name = search['name']
                        dist = round(1.0 - search[query], 2)
                    except KeyError as e:
                        name = 'unknown'
                        dist = 100.0

                    if dist > top_dist:
                        top_dist = dist
                        top_name = name

                if top_dist >= distance_threshold:
                    result_face = {'result': top_name, 'confidence': top_dist}
                else:
                    result_face = {'result': 'unknown', 'confidence': -1.0}

                data['faces'].append(result_face)

            data['process']['encodings'] = process_ms_encodings
            data['process']['search'] = process_ms_searches

            if total_success_count != data['found']:
                msg = 'There are {} faces but {} faces processed successfully. Please check what (tf) is going on!'.format(data['found'], total_success_count)
                data['message'] = msg

            if total_success_count > 0:
                rate = data['found'] / total_success_count * 100
                data['rate'] = rate
            else:
                data['rate'] = 0

            data['success'] = True
            self.process_successes += 1
        #except pysolr.SolrError as e:
        #    data['success'] = False
        #    data['message'] = str(e)
        #    self.process_fails += 1
        #except:
        #    data['success'] = False
        #    data['message'] = ('Type: {}, Message: TRY-EXCEPT', sys.exc_info()[0])
        #    self.process_fails += 1

            self.total_processed += 1

        self.is_busy = False

        return self.MD.post_processor.process(self.MD, data)
