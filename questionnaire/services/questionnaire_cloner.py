import copy
from questionnaire.models import QuestionGroupOrder
from questionnaire.utils.cloner_util import create_copies


class QuestionnaireClonerService(object):
    def __init__(self, questionnaire):
        self.questionnaire = questionnaire
        self.original_questionnaire = copy.deepcopy(self.questionnaire)
        self.sections = None
        self.sub_sections = None
        self.question_groups = None

    def clone(self):
        self.questionnaire.pk = None
        self.questionnaire.finalized = False
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
        return create_copies(sections, fields, questionnaire=self.questionnaire)

    def clone_sub_sections(self):
        sub_sections_map = {}
        fields = ['title', 'description', 'order']
        for old_section, new_section in self.sections.items():
            sub_sections = old_section.sub_sections.all()
            sub_sections_map.update(create_copies(sub_sections, fields, section=new_section))
        return sub_sections_map

    def clone_question_groups(self):
        question_groups_map = {}
        fields = ['name', 'instructions', 'parent', 'order', 'allow_multiples']
        for old_sub_section, new_sub_section in self.sub_sections.items():
            question_groups = old_sub_section.all_question_groups()
            question_groups_map.update(create_copies(question_groups, fields, subsection=new_sub_section))
        return question_groups_map

    def assign_sub_groups(self):
        for old, new in self.question_groups.items():
            if old.parent:
                new.parent = self.question_groups.get(old.parent)
                new.save()

    def assign_questions_to_groups(self):
        for old, new in self.question_groups.items():
            for index, question in enumerate(old.ordered_questions()):
                new.question.add(question)
                QuestionGroupOrder.objects.create(order=index + 1, question_group=new, question=question)