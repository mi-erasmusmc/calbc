'''
Created on Oct 2, 2009

@author: mulligen

This module will import the sense data for terms in the database
'''

import getopt, sys
from django.db import transaction
import sys
from elementtree.ElementTree import XML,XMLID

CHUNKSIZE = 1000

def ReadAbstract( fd ):
    text = ""
    isPubMedAbstract = False
    
    while True:
        line = fd.readline().replace( "\r", "" ).replace( "\n", "" )

        if line == "</PubmedArticle>":
            text += line
            return text
        
        if isPubMedAbstract:
            text += line
            
        if line == "<PubmedArticle>":
            text += line
            isPubMedAbstract = True
            
    return ""

def importAnnotation( verbose, annotationFilename ):
    
    fd = open( annotationFilename, "r" )
    cnt = 0

    # skip one line
    line = fd.readline().replace( "\r", "" ).replace( "\n", "" )
    
    while True:
        tree = XML( ReadAbstract( fd ) )
        pmid = tree.findall( ".//PMID" )[0].text
        print "pmid", pmid
        title = tree.findall( ".//ArticleTitle" )[0]
        text = ""
        for s in title.findall( "s" ):
            text += s.text
            for e in s.findall( "e" ):
                if e.text != None:
                    text += str(e.text)
                for w in e.findall( "w" ):
                    text += w.text
                    if w.tail != None:
                        text += w.tail
                if e.tail != None:
                    text += e.tail
            if s.tail != None:
                text += s.tail    
        print "title",text
        
        print "tokens", str( text.split() )

        abstracts = tree.findall( ".//AbstractText" )
        if len(abstracts) > 0:
            text = ""
            for s in abstracts[0].findall( "s" ):
                text += s.text
                for e in s.findall( "e" ):
                    if e.text != None:
                        text += str(e.text)
                    for w in e.findall( "w" ):
                        text += w.text
                        if w.tail != None:
                            text += w.tail
                    if e.tail != None:
                        text += e.tail
                if s.tail != None:
                    text += s.tail    
            print "abstract", text

        cnt += 1
        if cnt == 1:
            break
    fd.close()


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], "d", ["annotationFile="])
    except getopt.GetoptError, err:
        # print help information and exit:
        print str(err) # will print something like "option -a not recognized"
        sys.exit(2)

    annotationFilename = None
    verbose            = False
    
    for o, a in opts:
        if o == "-d":
            verbose = True
        elif o in ("--annotationFile"):
            annotationFilename = a
    
    if annotationFilename != None:
        importAnnotation( verbose, annotationFilename )
    
if __name__ == "__main__":
    main()