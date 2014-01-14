from django.views.generic import ListView
from questionnaire.models import Region


class ListRegions(ListView):
    model = Region
    template_name = 'locations/region/index.html'