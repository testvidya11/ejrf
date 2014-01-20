from django.conf.urls import patterns, url
from django.views.generic import TemplateView
from questionnaire.views.locations import ListRegions, ListCountries

urlpatterns = patterns('',
    url(r'^locations/region/$', ListRegions.as_view(), name='list_region_page'),
    url(r'^locations/region/(?P<region_id>\d+)/country/$', ListCountries.as_view(), name="list_country_page"),
    url(r'^login/$', 'django.contrib.auth.views.login', {'template_name': 'users/login.html'}, name="login_page"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/login/'}, name="logout_page"),
    url(r'^$', TemplateView.as_view(template_name="home/index.html"), name="home_page")
)
