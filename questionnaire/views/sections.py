from braces.views import PermissionRequiredMixin
from django.contrib import messages
from django.views.generic import CreateView
from questionnaire.forms.sections import SectionForm
from questionnaire.models import Section


class NewSection(PermissionRequiredMixin, CreateView):
    permission_required = 'auth.can_view_users'

    def __init__(self, **kwargs):
        super(NewSection, self).__init__(**kwargs)
        self.form_class = SectionForm
        self.object = Section
        self.template_name = "base/modals/_create.html"

    def form_valid(self, form):
        section = form.save(commit=False)
        section.order = Section.get_next_order(form.cleaned_data['questionnaire'])
        section.save()
        messages.success(self.request,"Section created successfully" )
        return super(NewSection, self).form_valid(form)

    def form_invalid(self, form):
        return super(NewSection, self).form_invalid(form)