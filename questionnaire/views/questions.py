from django.views.generic import ListView
from questionnaire.models import Question


class QuestionList(ListView):
    template_name = 'questions/index.html'
    model = Question
    object_list = Question.objects.all()

    def get(self, *args, **kwargs):
        context = {'request': self.request, 'questions': self.model.objects.all()}
        return self.render_to_response(context)
