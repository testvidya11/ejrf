from django.contrib import messages
from django.core.urlresolvers import reverse
from django.http import HttpResponseRedirect
from django.views.generic import ListView, CreateView
from questionnaire.forms.questions import QuestionForm
from questionnaire.models import Question


class QuestionList(ListView):
    template_name = 'questions/index.html'
    model = Question
    object_list = Question.objects.all()

    def get(self, *args, **kwargs):
        context = {'request': self.request, 'questions': self.model.objects.all()}
        return self.render_to_response(context)


class CreateQuestion(CreateView):
    def __init__(self, **kwargs):
        super(CreateQuestion, self).__init__(**kwargs)
        self.template_name = 'questions/new.html'
        self.object = Question
        self.model = Question
        self.form_class = QuestionForm
        self.form = None

    def get_context_data(self, **kwargs):
        context = super(CreateQuestion, self).get_context_data(**kwargs)
        context.update({'btn_label': 'CREATE', 'id': 'id-new-question-form'})
        return context

    def post(self, request, *args, **kwargs):
        self.form = QuestionForm(data=request.POST)
        if self.form.is_valid():
            return self._form_valid()
        return self._form_invalid()

    def _form_valid(self):
        self.form.save()
        messages.success(self.request, "Question successfully created.")
        return HttpResponseRedirect(reverse('list_questions_page'))

    def _form_invalid(self):
        messages.error(self.request, "Question NOT created. See errors below.")
        context = {'form': self.form, 'btn_label': "CREATE", 'id': 'id-new-question-form'}
        return self.render_to_response(context)