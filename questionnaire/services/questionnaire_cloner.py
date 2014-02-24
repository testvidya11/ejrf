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
        self.assign_sub_groups()
        self.assign_questions_to_groups()
        return self.questionnaire, self.original_questionnaire

    def clone_sections(self):
        sections = self.original_questionnaire.sections.all()
        fields = ['name', 'title', 'description', 'order']
        return self._create_copy_of(fields, sections, Section, questionnaire=self.questionnaire)

    def clone_sub_sections(self):
        sub_sections_map = {}
        fields = ['title', 'description', 'order']
        for old_section, new_section in self.sections.items():
            sub_sections = old_section.sub_sections.all()
            sub_sections_map.update(self._create_copy_of(fields, sub_sections, SubSection, section=new_section))
        return sub_sections_map

    def clone_question_groups(self):
        question_groups_map = {}
        fields = ['name', 'instructions', 'parent', 'order', 'allow_multiples']
        for old_sub_section, new_sub_section in self.sub_sections.items():
            question_groups = old_sub_section.all_question_groups()
            question_groups_map.update(self._create_copy_of(fields, question_groups, QuestionGroup, subsection=new_sub_section))
        return question_groups_map

    def _query_params(self, model, fields):
        return dict((field, getattr(model, field)) for field in fields)

    def _create_copy_of(self, fields, objects, klass, **kwargs):
        copy_map = {}
        for model in objects:
            kwargs.update(**self._query_params(model, fields))
            copy_map[model] = klass.objects.create(**kwargs)
        return copy_map

    def assign_sub_groups(self):
        for old, new in self.question_groups.items():
            if old.parent:
                new.parent = self.question_groups.get(old.parent)
                new.save()

    def assign_questions_to_groups(self):
        for old, new in self.question_groups.items():
            new.question.add(*old.all_questions())