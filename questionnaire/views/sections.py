from braces.views import PermissionRequiredMixin
from django.contrib import messages

from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import CreateView
from questionnaire.forms.sections import SectionForm, SubSectionForm
from questionnaire.models import Section, SubSection, Questionnaire


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

class NewSubSection(CreateView):
    def __init__(self, **kwargs):
        super(NewSubSection, self).__init__(**kwargs)
        self.object = SubSection
        self.form_class = SubSectionForm
        self.template_name = "sections/subsections/new.html"

    def post(self, request, *args, **kwargs):
        questionnaire_id = kwargs.get('questionnaire_id')
        section_id = kwargs.get('section_id')
        section = Section.objects.get(id=section_id)
        next_order = SubSection.get_next_order(section_id)
        self.form = SubSectionForm(instance=SubSection(section=section, order=next_order), data=request.POST)
        self.referer_url = reverse('questionnaire_entry_page', args=(questionnaire_id, section_id))
        if self.form.is_valid():
            return self._form_valid()
        return self._form_invalid()

    def _form_valid(self):
        self.form.save()
        messages.success(self.request,"Subsection successfully created." )
        return HttpResponseRedirect(self.referer_url)

    def _form_invalid(self):
        messages.error(self.request,"Subsection NOT created. See errors below." )
        context = {'id':  "new-subsection-modal",
                   'form': self.form, 'btn_label': "Create", }
        return self.render_to_response(context)


