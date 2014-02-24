import copy
from questionnaire.models import Section, SubSection


class QuestionnaireClonerService(object):
    def __init__(self, questionnaire):
        self.questionnaire = questionnaire
        self.original_questionnaire = copy.deepcopy(self.questionnaire)
        self.sections = None
        self.sub_sections = None

    def clone(self):
        self.questionnaire.pk = None
        self.questionnaire.save()
        self.sections = self.clone_sections()
        self.sub_sections = self.clone_sub_sections()
        return self.questionnaire, self.original_questionnaire

    def clone_sections(self):
        sections = self.original_questionnaire.sections.all().values('name', 'title', 'description')
        bulk_sections = [Section.objects.create(questionnaire=self.questionnaire, order=Section.get_next_order(self.questionnaire),
                                                **section_data) for section_data in sections]
        return bulk_sections

    def clone_sub_sections(self):
        sub_sections = []
        fields_to_query = ['name', 'title', 'description']
        for section in self.sections:
            query_params = dict((key, value) for key, value in section.__dict__.iteritems() if value and key in fields_to_query)
            old_section = Section.objects.filter(questionnaire=self.original_questionnaire, **query_params)
            for data in old_section[0].sub_sections.all().values('title', 'description'):
                sub_sections = [SubSection.objects.create(section=section, order=SubSection.get_next_order(section.id), **data)]
        return sub_sections