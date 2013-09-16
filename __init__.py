# encoding: utf-8
VERSION = '0.0.3'


# Default arguments
ACTION_START = 'start'
ACTION_STOP = 'stop'
DEFAULT_ACTION = ACTION_START
DEFAULT_BIND = '0.0.0.0'
DEFAULT_PORT = 80 
DEFAULT_PIDFILE = '/var/run/py-web.pid'


# Http Defaults
USER_AGENT = 'Pywebserver'
DEFAULT_MIMETYPE = 'text/plain'


### XenStore defaults
# Xen store read path
XS_READ = '/usr/bin/xenstore-read'


# Path for vm-data
BLOCK_PATH = '/local/domain/%(dom_id)d/vm-data/%(block)d'
COUNT_PATH = '/local/domain/%(dom_id)d/vm-data/count'

# unified logging
import logging
LOG = logging.getLogger('Pywebserver')


# Try using any json lib
try:
    json = __import__('json')
except ImportError:
    json = __import__('simplejson')
