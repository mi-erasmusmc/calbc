from django.conf.urls.defaults import *
from django.conf import settings
from ontology import version
from django.views.generic.simple import direct_to_template
from django.contrib import admin
from jsonrpc import jsonrpc_site
from ontology import views # you must import the views that need connected

handler404 = 'ontology.views.handle404'
handler500 = 'ontology.views.handle500'

admin.autodiscover()

urlpatterns = patterns('',
    (r'^$', 'ontology.annotations.concepts.list' ),
    (r'^login/$', 'ontology.annotations.auth.login'),    
    (r'^logout/$', 'ontology.annotations.auth.logout'),
    (r'^password_change/$', 'ontology.annotations.auth.password_change'),
    (r'^password_change/done/$', 'ontology.annotations.auth.password_change_done'),
    (r'^password_reset/$', 'ontology.annotations.auth.password_reset'),
    (r'^password_reset/done/$', 'ontology.annotations.auth.password_reset_done'),
    (r'^reset/(?P<uidb36>[0-9A-Za-z]+)-(?P<token>.+)/$', 'ontology.annotations.auth.password_reset_confirm'),
    (r'^reset/done/$', 'ontology.annotations.auth.password_reset_complete'),    
    (r'^concepts/$', 'ontology.annotations.concepts.list'),
    (r'^concepts/(?P<concept_id>\d+)/$', 'ontology.annotations.concepts.details'),
    (r'^sites/$', 'ontology.annotations.sites.list'),
    (r'^intersection/$', 'ontology.annotations.sites.intersection'),
    (r'^sites/(?P<site>([^/])+)/$', 'ontology.annotations.sites.details'),
    (r'^sites/(?P<site>([^/])+)/export', 'ontology.annotations.sites.export'),
    (r'^newdefinition/(?P<concept_id>\d+)/$', 'ontology.annotations.definitions.new' ),
    (r'^newsource/(?P<concept_id>\d+)/$', 'ontology.annotations.sources.new' ),
    (r'^definitions/(?P<concept_id>\d+)/$', 'ontology.annotations.definitions.list' ),
    (r'^definition/(?P<definition_id>\d+)/$', 'ontology.annotations.definitions.details' ),
    (r'^relations/(?P<concept_id>\d+)/$', 'ontology.annotations.relations.list' ),
    (r'^terms/(?P<concept_id>\d+)/$', 'ontology.annotations.terms.list' ),
    (r'^term/(?P<term_id>\d+)/$', 'ontology.annotations.terms.details' ),
    (r'^reviewers/$', 'ontology.annotations.reviewer.list' ),
    (r'^reviewers/(?P<reviewer_id>\d+)/$', 'ontology.annotations.reviewer.details' ),
    (r'^pageanalysis/$', 'ontology.annotations.pageanalysis.list' ),
    (r'^pageanalysis/new', 'ontology.annotations.pageanalysis.new' ),
    (r'^pageanalysis/(?P<page_id>\d+)/analyze', 'ontology.annotations.pageanalysis.analyze' ),
    (r'^explore', 'ontology.annotations.explore.new' ),
    (r'^semantictype/(?P<semantictype_id>\d+)/$', 'ontology.annotations.semantictype.details' ),
    (r'^site-media/(?P<path>.*)$', 'django.views.static.serve',{'document_root': '/Users/mulligen/Workspaces/Knewco/Thesaurus/ontology/media', 'show_indexes': True}),
    (r'^admin/', include(admin.site.urls)),
    (r'^json/', jsonrpc_site.dispatch),
)
