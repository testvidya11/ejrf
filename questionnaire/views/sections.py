from django.core.urlresolvers import reverse
from django.views.generic import CreateView
from questionnaire.forms.sections import SectionForm
from questionnaire.models import Section


class NewSection(CreateView):
    def __init__(self, **kwargs):
        super(NewSection, self).__init__(**kwargs)
        self.form_class = SectionForm
        self.object = Section
        self.template_name = "questionnaires/sections/new.html"

    def form_valid(self, form):
        section = form.save(commit=False)
        section.order = Section.get_next_order(form.cleaned_data['questionnaire'])
        section.save()
        return super(NewSection, self).form_valid(form)

    def form_invalid(self, form):
        return super(NewSection, self).form_invalid(form)