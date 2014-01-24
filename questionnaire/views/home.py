from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from questionnaire.models import Questionnaire, Section
from braces.views import LoginRequiredMixin

class Home(LoginRequiredMixin, View):
    template_name="home/index.html"

    def get(self, request, *args, **kwargs):
        questionnaires = Questionnaire.objects.all()
        sections = Section.objects.order_by('order')
        if questionnaires.exists() and sections.exists():
            return HttpResponseRedirect('questionnaire/entry/%d/section/%d/' % (questionnaires.latest('created').id,
                                                                                sections[0].id))
        return render(request, self.template_name)
