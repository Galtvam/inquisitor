"""Retain apiclient as an alias for googleapiclient."""

from six import iteritems

import classroom.googleapiclient as googleapiclient

from classroom.googleapiclient import channel
from classroom.googleapiclient import discovery
from classroom.googleapiclient import errors
from classroom.googleapiclient import http
from classroom.googleapiclient import mimeparse
from classroom.googleapiclient import model
try:
    from classroom.googleapiclient import sample_tools
except ImportError:
    # Silently ignore, because the vast majority of consumers won't use it and
    # it has deep dependence on oauth2client, an optional dependency.
    sample_tools = None
from classroom.googleapiclient import schema

__version__ = googleapiclient.__version__

_SUBMODULES = {
    'channel': channel,
    'discovery': discovery,
    'errors': errors,
    'http': http,
    'mimeparse': mimeparse,
    'model': model,
    'sample_tools': sample_tools,
    'schema': schema,
}

import sys
for module_name, module in iteritems(_SUBMODULES):
  sys.modules['apiclient.%s' % module_name] = module
