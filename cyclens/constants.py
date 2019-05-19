# coding: utf-8

"""Constants used by Cyclens modules."""

####################################
# [VERSION]
####################################

VERSION_MAJOR = 0
VERSION_MINOR = 0
VERSION_PATCH = '0.dev0'

__short_version__ = '{}.{}'.format(VERSION_MAJOR, VERSION_MINOR)
__version__ = '{}.{}'.format(__short_version__, VERSION_PATCH)


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

