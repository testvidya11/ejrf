from django.conf.urls import patterns, url
from questionnaire.views.locations import ListRegions, ListCountries

urlpatterns = patterns('',
    url(r'^locations/region/$', ListRegions.as_view(), name='list_region_page'),
    url(r'^locations/region/(?P<region_id>\d+)/country/$', ListCountries.as_view(), name="list_country_page"),
)
