from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import View
from django.core.urlresolvers import reverse
from braces.views import MultiplePermissionsRequiredMixin

from questionnaire.models import Questionnaire, Section


class Home(MultiplePermissionsRequiredMixin, View):
    def __init__(self, *args, **kwargs):
        super(Home, self).__init__(*args, **kwargs)
        self.permissions = {'any': ('auth.can_submit_responses', 'auth.can_view_users')}
        self.template_name = "home/index.html"
        self.questionnaires = Questionnaire.objects.all()
        self.sections = Section.objects.order_by('order')

    def get(self, *args, **kwargs):
        if self.request.user.has_perm('auth.can_view_users'):
            return self._render_global_admin_home()
        if self.questionnaires.exists() and self.sections.exists():
            return self._render_questionnaire_section()
        return render(self.request, self.template_name)

    def _render_global_admin_home(self):
        global_admin_template = 'home/global/index.html'
        context = {'finalized_questionnaires': self.questionnaires.filter(finalized=True),
                   'draft_questionnaires': self.questionnaires.filter(finalized=False)}
        return render(self.request, global_admin_template, context)

    def _render_questionnaire_section(self):
        args = (self.questionnaires.latest('created').id, self.sections[0].id)
        return HttpResponseRedirect(reverse('questionnaire_entry_page', args=args))