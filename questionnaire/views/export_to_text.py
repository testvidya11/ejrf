import csv
from django.http import HttpResponse
from django.views.generic import TemplateView
from questionnaire.models import Questionnaire
from questionnaire.services.export_data_service import ExportToTextService


class ExportToTextView(TemplateView):
    template_name = "home/extract.html"

    def get_context_data(self, **kwargs):
        context = super(ExportToTextView, self).get_context_data(**kwargs)
        context['questionnaires'] = Questionnaire.objects.all()
        return context

    def post(self, request, *args, **kwargs):
        questionnaire = Questionnaire.objects.get(id=request.POST['questionnaire'])
        formatted_responses = ExportToTextService(questionnaire).get_formatted_responses()
        response = HttpResponse(content_type='text/csv')
        response['Content-Disposition'] = 'attachment; filename="%s-%s.txt"'% (questionnaire.name, questionnaire.year)

        writer = csv.writer(response)
        for row in formatted_responses:
            writer.writerow(row)
        return response