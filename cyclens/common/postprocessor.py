# coding: utf-8

"""Common post-processor class for modules."""

from __future__ import unicode_literals

from datetime import datetime
import json


class PostProcessor:

    def __init__(self):
        pass

    def try_load(self):
        return True

    def process(self, module, data):

        if data is None:
            result = {'success': False, 'message': 'There is no data for post-processor'}
            return result

        date_end = datetime.now()

        ms_diff = (date_end - data['process']['start']).total_seconds() * 1000

        data['process']['start'] = get_date_str(data['process']['start'])
        data['process']['end'] = get_date_str(date_end)
        data['process']['total'] = round(ms_diff, 2)

        del data['frame_faces']
        del data['frame_gray']
        del data['frame_rgb']

        if module is None:
            data['success'] = False
            data['message'] = 'There is no data for post-processor'
            return data

        if module is not None and module is not 'test':
            module.processor.response_times.append(ms_diff)

        return data


def get_date_str(date):
    return date.strftime('%Y-%m-%dT%H:%M:%S.%f')
