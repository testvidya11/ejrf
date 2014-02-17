from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.core.urlresolvers import reverse
from braces.views import MultiplePermissionsRequiredMixin

from questionnaire.models import Questionnaire, Section


class Home(MultiplePermissionsRequiredMixin, View):
    permissions = {'any': ('auth.can_submit_responses', 'auth.can_view_users')}
    template_name = "home/index.html"

    def get(self, request, *args, **kwargs):
        if request.user.has_perm('auth.can_submit_responses'):
            questionnaires = Questionnaire.objects.all()
            sections = Section.objects.order_by('order')
            if questionnaires.exists() and sections.exists():
                args = (questionnaires.latest('created').id, sections[0].id)
                return HttpResponseRedirect(reverse('questionnaire_entry_page', args=args))
        return render(request, self.template_name)