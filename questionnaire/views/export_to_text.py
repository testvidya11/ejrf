from django.views.generic import TemplateView
from questionnaire.models import Questionnaire


class ExportToTextView(TemplateView):
    template_name = "home/extract.html"

    def get_context_data(self, **kwargs):
        context = super(ExportToTextView, self).get_context_data(**kwargs)
        context['questionnaires'] = Questionnaire.objects.all()
        return context