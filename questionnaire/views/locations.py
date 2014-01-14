from django.views.generic import ListView
from questionnaire.models import Region, Country


class ListRegions(ListView):
    model = Region
    template_name = 'locations/region/index.html'


class ListCountries(ListView):
    model = Country
    template_name = 'locations/country/index.html'

    def get(self, request, *args, **kwargs):
        self.region = Region.objects.get(id=self.kwargs['region_id'])
        return super(ListCountries, self).get(request, *args, **kwargs)

    def get_queryset(self):
        return self.region.countries.all()
