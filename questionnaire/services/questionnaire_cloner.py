import copy
from questionnaire.models import Section


class QuestionnaireClonerService(object):
    def __init__(self, questionnaire):
        self.questionnaire = questionnaire
        self.original_questionnaire = copy.deepcopy(self.questionnaire)

    def clone(self):
        self.questionnaire.pk = None
        self.questionnaire.save()
        self.clone_sections()
        return self.questionnaire, self.original_questionnaire

    def clone_sections(self):
        sections = self.original_questionnaire.sections.all().values('name', 'title', 'description')
        for section_data in sections:
            Section.objects.create(questionnaire=self.questionnaire, order=Section.get_next_order(self.questionnaire),
                                   **section_data)