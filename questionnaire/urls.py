from django.conf.urls import patterns, include, url
from questionnaire.views.locations import ListLocationTypes

urlpatterns = patterns('',
    url(r'^locations/type/', ListLocationTypes.as_view(), name='list_location_types_page'),
)
