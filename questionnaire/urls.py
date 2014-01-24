from django.conf.urls import patterns, url
from questionnaire.views.export_to_text import ExportToTextView
from questionnaire.views.home import Home
from questionnaire.views.locations import ListRegions, ListCountries
from questionnaire.views.questionnaires import Entry
from questionnaire.views.users import UsersList, CreateUser

urlpatterns = patterns('',
    url(r'^locations/region/$', ListRegions.as_view(), name='list_region_page'),
    url(r'^locations/region/(?P<region_id>\d+)/country/$', ListCountries.as_view(), name="list_country_page"),
    url(r'^accounts/login/$', 'django.contrib.auth.views.login', {'template_name': 'users/login.html'}, name="login_page"),
    url(r'^users/$', UsersList.as_view(), name="list_users_page"),
    url(r'^users/new/$', CreateUser.as_view(), name="create_user_page"),
    url(r'^logout/$', 'django.contrib.auth.views.logout', {'next_page': '/accounts/login/'}, name="logout_page"),
    url(r'^$',  Home.as_view(), name="home_page"),
    url(r'^questionnaire/entry/(?P<questionnaire_id>\d+)/section/(?P<section_id>\d+)/$',
        Entry.as_view(), name="questionnaire_entry_page"),
    url(r'^extract/$', ExportToTextView.as_view(), name="export_page")
)