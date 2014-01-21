from questionnaire.models.base import BaseModel
from django.db import models


class Questionnaire(BaseModel):
    name = models.CharField(max_length=256, null=False, blank=False)
    description = models.TextField(null=True, blank=True)

    def sub_sections(self):
        subsections = []
        sections = self.sections.all()
        for section in sections:
            subsections.extend(list(section.sub_sections.all()))
        return subsections

    def get_all_questions(self):
        all_questions = []
        for subsection in self.sub_sections():
            all_questions.extend(subsection.all_questions())
        return all_questions