'''
Created on Oct 16, 2009

@author: mulligen
'''

from ontology.annotations.models import Concept, ReviewerConcept
import urllib
import urllib2
import json
from unicode import translateUnicode

def index(text):
    url = 'http://test.knewco.com/knownow/peregrinews'
    values = {  'sn' : 'c4dbf1f65ed5439f9555770233c389fb',
                'sid' : 'HW',
                'ctid' : '3',
                'cmd' : 'index',
                'opt' : '3',
                'txt' : translateUnicode( unicode(text) )  
             }

    obj = json.read( urllib2.urlopen( urllib2.Request( url, urllib.urlencode( values ) ) ).read() )
    
    res = []
    for concept in obj['concepts']:
        res.append( { 'id': concept['id'].split("/")[1], 'tf': len(concept['positions']) } )
    return res

def getParam(request,param,default):
    if request.method == 'GET':
        try:
            value = request.GET[param]
        except:
            value = default
    elif request.method == 'POST':
        try:
            value = request.POST[param]
        except:
            value = default
    return value

def convertValue(type,value):
    if type == "text":
        return value
    else:
        return int( value == "True" )

def printRequest(request):    
    fd = open( "/tmp/django.out", "w" )
    for key in request.POST.keys():
        fd.write( "request[" + key + "]=" + request.POST[key] + "\n" )
    fd.close()

def handleData( request, objects, concept_id, entity ):
    entities = []
    
    for object in objects:
        changed = False
        for type in ["radio","checkbox","text"]:
            for field in object.__dict__.keys():
                key = type + "-" + str(object.id) + "-" + field
                if request.POST.has_key(key):
                    value = convertValue(type,request.POST[key])
                    if str(object.__dict__[field]) != str(value):
                        object.__dict__[field] = value
                        changed = True
        if changed:
            object.save()
            if not entity in entities:
                entities.append(entity)

    for entity in entities:
        concept = Concept.objects.get( id = concept_id )
        reviewerConcept = ReviewerConcept( reviewerId = request.user, conceptId = concept, entityType = entity )
        reviewerConcept.save()
    