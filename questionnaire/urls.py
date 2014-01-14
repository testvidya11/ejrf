from django.conf.urls import patterns, include, url
from questionnaire.views.locations import ListRegions

urlpatterns = patterns('',
    url(r'^locations/region/', ListRegions.as_view(), name='list_region_page'),
)
