'''
Created on Oct 16, 2009

@author: mulligen
'''

from ontology.annotations.annotation_utils import handleData, getParam, printRequest
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.shortcuts import render_to_response
from django.core.urlresolvers import reverse
from django.db import connection, transaction
from django.http import HttpResponse, HttpResponseRedirect
from ontology.annotations.models import Concept, ConceptAnnotation, ConceptSite, ConceptSemanticType, ConceptVocabulary, Term, SemanticType
from django.contrib.auth.decorators import login_required
from django.template import RequestContext

def details( request, concept_id ):
    
    concept = Concept.objects.get( id = concept_id )
    conceptAnnotation = ConceptAnnotation.objects.get( id = concept_id )
    semantictypes = ConceptSemanticType.objects.filter( conceptId = concept )
    vocabularies = ConceptVocabulary.objects.filter( conceptId = concept )
    
    if request.method == "POST":
        action = getParam( request, "action", "" )
        if action == "save":
            handleData(request, [conceptAnnotation], concept_id, "concept" )
        return HttpResponseRedirect( reverse( 'ontology.annotations.concepts.list' ) )
    
    return render_to_response("concepts/details.html", 
                              { 'concept': concept, 
                                'conceptAnnotation': conceptAnnotation, 
                                'semantictypes': semantictypes,
                                'vocabularies': vocabularies,  
                              }, 
                              context_instance = RequestContext(request) )

details = login_required(redirect_field_name='redirect_to',)(details)


                
def list(request):
    
    search    = getParam( request, 'search', '' )
    sort      = getParam( request, 'sort',   'conceptId')
    page      = getParam( request, 'page',   1 )
    displayed = getParam( request, 'displayed', 0 )
    semtype   = int(getParam( request, 'semtypes', 0 ))

    if len(search) > 0:
        extra = []
        if len(search) == 8 and search[0] == "C":
            try:
                concept = Concept.objects.get( conceptId = search  )
                extra.append( concept.id )
            except:
                pass
        else:
            terms = Term.objects.filter( label__icontains = search ).only("conceptId")
            for term in terms:
                extra.append( term.getId() )

        conceptList = ConceptAnnotation.objects.filter( conceptId__in = extra ).order_by( sort )
    else:
        conceptList = ConceptAnnotation.objects.all().order_by( sort )

    if semtype != 0:
        semanticType = SemanticType.objects.get( semanticTypeId = semtype )
        semConceptList = ConceptSemanticType.objects.filter( semanticTypeId = semanticType ).only("conceptId")
        extra = []
        for semConceptItem in semConceptList:
            extra.append( semConceptItem.conceptId )

        conceptList = conceptList.filter( conceptId__in = extra )
        
    if displayed:
        conceptList = conceptList.filter( displayed = displayed )

    paginator = Paginator(conceptList, 25)
    
    try:
        concepts = paginator.page(page)
    except (EmptyPage, InvalidPage):
        concepts = paginator.page(paginator.num_pages)
    
    semtypes = SemanticType.objects.all().order_by( "label" )
     
    return render_to_response( 'concepts/list.html', 
                               {
                                    'concepts': concepts, 
                                    'semantictypes': semtypes,
                                    'search': search,
                                    'sort': sort,
                                    'displayed': displayed,
                                    'semtype': semtype,
                                }, 
                                context_instance = RequestContext(request) )

list = login_required(redirect_field_name='redirect_to',)(list)