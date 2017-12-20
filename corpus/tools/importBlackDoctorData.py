'''
Created on Oct 2, 2009

@author: mulligen

This module will import the sense data for terms in the database
'''

import getopt, sys
from django.db import transaction
from ontology.annotations.models import ConceptSite, ConceptAnnotation, ConceptRelation, Concept, Term, TermAnnotation
import sys

CHUNKSIZE = 1000

concepts = {}

def importSiteData( verbose, siteFilename ):
    
    fd = open( siteFilename, "r" )
    cnt = 0

    # skip one line
    line = fd.readline().replace( "\r", "" ).replace( "\n", "" )
    
    while True:
        line = fd.readline().replace( "\r", "" ).replace( "\n", "" )
        
        if line == "":
            break
        
        pieces = line.split( "\t" ) 
        cui = pieces[0].split("/")[1]
        try:
            comment = pieces[4]
        except:
            comment = ""
        
        if not concepts.has_key(cui):
            concepts[cui] = { 'comment': comment, 'frequency': 1 }
            cnt += 1
            if cnt % CHUNKSIZE == 0:
                print "processing record", cnt
        else:
            concepts[cui]['frequency'] = concepts[cui]['frequency'] + 1

    fd.close()

    siteName = "Black Doctor"
    for cui in concepts.keys():
        sourceConcept = Concept.objects.get( conceptId = cui )
        sourceConceptAnnotation = ConceptAnnotation.objects.get( conceptId = sourceConcept )
        try:
            sourceConceptSite = ConceptSite.objects.get( conceptId = sourceConcept, site = siteName )
            sourceConceptSite.level = 0
            sourceConceptSite.save()
        except:
            ConceptSite( conceptId = sourceConcept,  annotation = sourceConceptAnnotation, site = siteName, comment = concepts[cui]['comment'], frequency = concepts[cui]['frequency'], level = 0 ).save()
          
        # now add the targets to the ConceptSite table  
        relations = ConceptRelation.objects.filter( sourceConceptId = sourceConcept, suppressed = False ).only( "targetConceptId" )
        for relation in relations:
            targetConceptAnnotation = ConceptAnnotation.objects.get( conceptId = relation.targetConceptId.id )
            try:
                relatedConceptSite = ConceptSite.objects.get( conceptId = relation.targetConceptId, site = siteName )
            except:
                ConceptSite( conceptId = relation.targetConceptId, annotation = targetConceptAnnotation, site = siteName, comment = "", frequency = concepts[cui]['frequency'], level = 1 ).save()

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d", ["siteFile="])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        sys.exit(2)

    siteFilename = None
    verbose       = False
    
    for o, a in opts:
        if o == "-d":
            verbose = True
        elif o in ("--siteFile"):
            siteFilename = a
    
    if siteFilename != None:
        importSiteData( verbose, siteFilename )
        print "ready"
    
if __name__ == "__main__":
    main()