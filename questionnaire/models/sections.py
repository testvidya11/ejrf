from questionnaire.models import Questionnaire, Question
from questionnaire.models.base import BaseModel
from django.db import models


class Section(BaseModel):
    name = models.CharField(max_length=100, blank=False, null=True)
    title = models.CharField(max_length=256, blank=False, null=False)
    order = models.IntegerField(blank=False, null=False)
    description = models.TextField(blank=True, null=True)
    questionnaire = models.ForeignKey(Questionnaire, blank=False, null=False, related_name="sections")

    def all_questions(self):
        subsections = self.sub_sections.order_by('order')
        questions = []
        for subsection in subsections:
            for group in subsection.question_group.order_by('order'):
                questions.extend(group.question.values_list('id', flat=True))
        return Question.objects.filter(id__in=questions)


class SubSection(BaseModel):
    title = models.CharField(max_length=256, blank=False, null=False)
    order = models.IntegerField(blank=False, null=False)
    section = models.ForeignKey(Section, blank=False, null=False, related_name="sub_sections")
    description = models.TextField(blank=True, null=True)

    def all_question_groups(self):
        return self.question_group.all()

    def all_questions(self):
        all_questions = []
        for question_group in self.all_question_groups():
            all_questions.extend(question_group.all_questions())
        return all_questions
