from django.shortcuts import render
from django.views.generic import View
from questionnaire.models import Section, Questionnaire


class ManageJRF(View):
    def __init__(self, *args, **kwargs):
        super(ManageJRF, self).__init__(**kwargs)
        self.permissions = {'any': ('auth.can_view_users', )}
        self.template_name = 'home/global/index.html'
        self.questionnaires = Questionnaire.objects.all().order_by('-year')
        self.sections = Section.objects.order_by('order')

    def get(self, *args, **kwargs):
        context = {'finalized_questionnaires': self.questionnaires.filter(finalized=True),
                   'draft_questionnaires': self.questionnaires.filter(finalized=False)}
        return render(self.request, self.template_name, context)