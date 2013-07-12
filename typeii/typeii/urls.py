from django.conf.urls.defaults import patterns, include, url
from django.views.generic import DetailView, ListView
from enzymes.models import Genome
from django.views.static import * 
from django.conf import settings
from django.views.generic.simple import direct_to_template

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()



urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'typeii.views.home', name='home'),
    # url(r'^typeii/', include('typeii.foo.urls')),
    url(r'^Typei/loadGenome', 'enzymes.views.loadGenome'),
    url(r'^Typei/loadPiece', 'enzymes.views.loadPiece'),
    url(r'^Typei/loadSystem', 'enzymes.views.loadSystem'),
    url(r'^Typei/loadProtein', 'enzymes.views.loadProtein'),
    url(r'^Typei/searchView', 'enzymes.views.searchView'),
    
    
    url(r'^enzymes/base', direct_to_template, {'template': 'typei/base_home.html'}),
    url(r'^enzymes/browse', 'enzymes.views.browse'),
    url(r'^enzymes/contact', direct_to_template, {'template': 'typei/contact.html'}),
    url(r'^enzymes/searchAll', 'enzymes.views.searchAll'),  
    url(r'^enzymes/calculate_order', 'enzymes.views.calculate_order'),
    
    url(r'^enzymes/listing', 'enzymes.views.listing'),
    url(r'^enzymes/home', 'enzymes.views.home'),   
    url(r'^enzymes/stats', 'enzymes.views.stats'), 
    url(r'^enzymes/export', 'enzymes.views.data_for_Alberas'), 
    
    url(r'^enzymes/searchSys', 'enzymes.views.searchSys'),   
    url(r'^enzymes/browseFam', 'enzymes.views.browse_by_family'),
    url(r'^enzymes/formtest', 'enzymes.views.formtest'),
    url(r'^enzymes/basic_browse', 'enzymes.views.basic_browse'),
    
    url(r'^enzymes/list', 'enzymes.views.listdisplay'),
    url(r'^enzymes/protein/(?P<pk>\d+)/$', 'enzymes.views.detailedProtein'),
    url(r'^enzymes/genome/(?P<pk>\d+)/$', 'enzymes.views.genome'),
    url(r'^enzymes/dna/(?P<pk>\d+)/$', 'enzymes.views.dna'),
    url(r'^enzymes/system/(?P<pk>\d+)/$', 'enzymes.views.system'),
    url(r'^enzymes/results_to_text_file', 'enzymes.views.results_to_text_file'),

    # Required to make static serving work 
    url(r'^media/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT}),
    # Required to make static serving work 
    url(r'^static/(?P<path>.*)$', 'django.views.static.serve', {'document_root': settings.STATIC_ROOT}),
    
    # Uncomment the admin/doc line below to enable admin documentation:
    url(r'^admin/doc/', include('django.contrib.admindocs.urls')),
    # Uncomment the next line to enable the admin:
    url(r'^admin/', include(admin.site.urls)),
)
