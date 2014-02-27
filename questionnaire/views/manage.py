from django.core.urlresolvers import reverse
from django.shortcuts import render
from django.views.generic import View
from questionnaire.forms.filter import QuestionnaireFilterForm
from questionnaire.models import Section, Questionnaire


class ManageJRF(View):
    def __init__(self, *args, **kwargs):
        super(ManageJRF, self).__init__(**kwargs)
        self.permissions = {'any': ('auth.can_view_users', )}
        self.template_name = 'home/global/index.html'
        self.questionnaires = Questionnaire.objects.all().order_by('-year')
        self.sections = Section.objects.order_by('order')

    def get(self, *args, **kwargs):
        context = {'finalized_questionnaires': self.questionnaires.filter(status=Questionnaire.FINALIZED),
                   'draft_questionnaires': self.questionnaires.filter(status=Questionnaire.DRAFT),
                   'filter_form': QuestionnaireFilterForm(),
                   'btn_label': 'Duplicate',
                   'action': reverse('duplicate_questionnaire_page')}
        return render(self.request, self.template_name, context)