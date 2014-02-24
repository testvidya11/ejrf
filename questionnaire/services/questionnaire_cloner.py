import copy
from questionnaire.models import Section, SubSection, QuestionGroup


class QuestionnaireClonerService(object):
    def __init__(self, questionnaire):
        self.questionnaire = questionnaire
        self.original_questionnaire = copy.deepcopy(self.questionnaire)
        self.sections = None
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
        sections = self.original_questionnaire.sections.all()
        bulk_sections = dict((section, Section.objects.create(questionnaire=self.questionnaire, **self._querable_fields(section, ['name', 'title', 'description', 'order']))) for section in sections)
        return bulk_sections

    def clone_sub_sections(self):
        sub_sections_map = {}
        for old_section, new_section in self.sections.items():
            sub_sections = old_section.sub_sections.all()
            sub_sections_map.update(dict((sub_section, SubSection.objects.create(section=new_section, **self._querable_fields(sub_section, ['title', 'description', 'order']))) for sub_section in sub_sections))
        return sub_sections_map

    def clone_question_groups(self):
        question_groups_map = {}
        for old_sub_section, new_sub_section in self.sub_sections.items():
            question_groups = old_sub_section.all_question_groups()
            question_groups_map.update(dict((question_group, QuestionGroup.objects.create(subsection=new_sub_section, **self._querable_fields(question_group, ['name', 'instructions', 'parent', 'order', 'allow_multiples']))) for question_group in question_groups))
        return question_groups_map


    def _get_fields_to_query(self, fields_to_query, model):
        return dict((key, value) for key, value in model.__dict__.iteritems() if value and key in fields_to_query)

    def _querable_fields(self, model, fields):
        return dict((field, getattr(model,field)) for field in fields)