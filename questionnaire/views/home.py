from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from questionnaire.models import Questionnaire, Section
from django.core.urlresolvers import reverse
from braces.views import LoginRequiredMixin, PermissionRequiredMixin


class Home(PermissionRequiredMixin, View):
    permission_required = 'auth.can_submit_responses'
    template_name = "home/index.html"


    def get(self, request, *args, **kwargs):
        questionnaires = Questionnaire.objects.all()
        sections = Section.objects.order_by('order')
        if questionnaires.exists() and sections.exists():
            args = (questionnaires.latest('created').id, sections[0].id)
            return HttpResponseRedirect(reverse('questionnaire_entry_page', args=args))
        return render(request, self.template_name)
