# coding: utf-8

"""
cyclens.modules.common
~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~

Implements common post-processor class for modules.

This program comes with ABSOLUTELY NO WARRANTY; This is free software,
and you are welcome to redistribute it under certain conditions; See
file LICENSE, which is part of this source code package, for details.

:copyright: Copyright © 2019, The Cyclens Project
:license: MIT, see LICENSE for more details.
"""

from __future__ import unicode_literals

from datetime import datetime


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

        del data['process']['locations']

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
