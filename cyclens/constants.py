# coding: utf-8

"""
cyclens
~~~~~~~

Implements constants used by Cyclens modules.

This program comes with ABSOLUTELY NO WARRANTY; This is free software,
and you are welcome to redistribute it under certain conditions; See
file LICENSE, which is part of this source code package, for details.

:copyright: Copyright © 2019, The Cyclens Project
:license: MIT, see LICENSE for more details.
"""

####################################
# [PYTHON]
####################################

REQUIRED_PYTHON_VER = (3, 7, 1)

####################################
# [CONFIG::GENERAL]
####################################



####################################
# [MODULE::STATES]
####################################

STATE_ENABLE = 'ENABLE'
STATE_DISABLE = 'DISABLE'

STATE_BOOTING = 'BOOTING'
STATE_INITIALIZING = 'INITIALIZING'
STATE_SHUTDOWN = 'SHUTDOWN'

STATE_OK = 'OK'
STATE_IDLE = 'IDLE'
STATE_STANDBY = 'STANDBY'

STATE_PROBLEM = 'PROBLEM'

####################################
# [SERVER::API]
####################################

SERVER_PORT = 1997

URL_ROOT = '/'
URL_API = '/api/'

HTTP_HEADER_HA_AUTH = 'X-HA-access'
HTTP_HEADER_X_REQUESTED_WITH = 'X-Requested-With'

CONTENT_TYPE_JSON = 'application/json'
CONTENT_TYPE_TEXT_PLAIN = 'text/plain'

####################################
# [APACHE::SOLR]
####################################

SOLR_URL = 'http://localhost:8983/solr/cyclens'

