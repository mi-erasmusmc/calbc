from django.conf import settings as _settings
from ontology import version as _version

def settings(request):
    return {'settings': _settings}

def version(request):
    return {'version': _version}