from django.views.generic import ListView
from questionnaire.models import LocationType


class ListLocationTypes(ListView):
    model = LocationType
    template_name = 'locations/type/index.html'