import copy
from questionnaire.models import Section, SubSection, QuestionGroup


class QuestionnaireClonerService(object):
    def __init__(self, questionnaire):
        self.questionnaire = questionnaire
        self.original_questionnaire = copy.deepcopy(self.questionnaire)
        self.sections = None
        self.sections_mapping = None
        self.sub_sections = None
        self.question_groups = None

    def clone(self):
        self.questionnaire.pk = None
        self.questionnaire.save()
        self.sections = self.clone_sections()
        self.sub_sections = self.clone_sub_sections()
        self.question_groups = self.clone_question_groups()
        return self.questionnaire, self.original_questionnaire

    def clone_sections(self):
        sections = self.original_questionnaire.sections.all().values('name', 'title', 'description', 'order')
        bulk_sections = [Section.objects.create(questionnaire=self.questionnaire, **section_data) for section_data in sections]
        return bulk_sections

    def clone_sub_sections(self):
        sub_sections = []
        fields_to_query = ['title', 'description', 'order']
        for section in self.sections:
            query_params = self._get_fields_to_query(fields_to_query, section)
            old_section = Section.objects.filter(questionnaire=self.original_questionnaire, **query_params)
            for data in old_section[0].sub_sections.all().values('title', 'description', 'order'):
                sub_sections.extend([SubSection.objects.create(section=section, **data)])
        return sub_sections

    def clone_question_groups(self):
        question_groups = []
        fields_to_query = ['name', 'instructions', 'parent', 'order', 'allow_multiples']
        sections_all = self.original_questionnaire.sections.all()
        for section in sections_all:
            for sub_section in section.sub_sections.all():
                query_params = self._get_fields_to_query(fields_to_query, sub_section)
                old_sub_sections = SubSection.objects.filter(section=section, **query_params)
                for data in old_sub_sections[0].all_question_groups().values('name', 'instructions', 'parent', 'order', 'allow_multiples'):
                    question_groups.extend([QuestionGroup.objects.create(subsection=sub_section, **data)])
        return question_groups


    def _get_fields_to_query(self, fields_to_query, model):
        return dict((key, value) for key, value in model.__dict__.iteritems() if value and key in fields_to_query)
