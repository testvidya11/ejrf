from questionnaire.models import QuestionGroup, SubSection, Section, Questionnaire, Question
from questionnaire.models.question_text_history import QuestionTextHistory
from questionnaire.tests.base_test import BaseTest


class QuestionGroupOrderTest(BaseTest):
    def setUp(self):
        self.question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Text')
        self.questionnaire = Questionnaire.objects.create(name="Uganda Revision 2014", description="some description")
        self.section = Section.objects.create(title="Immunisation Coverage", order=1, questionnaire=self.questionnaire)
        self.sub_section = SubSection.objects.create(title="Immunisation Extra Coverage", order=1, section=self.section)
        self.question1 = Question.objects.create(text='B. Number of cases tested',
                                                 UID='C00003', answer_type='Number')
        self.parent_group = QuestionGroup.objects.create(subsection=self.sub_section, name="Laboratory Investigation")
        self.parent_group.question.add(self.question1)

    def test_question_group_order_fields(self):
        question_text_history = QuestionTextHistory()
        fields = [str(item.attname) for item in question_text_history._meta.fields]
        self.assertEqual(7, len(fields))
        for field in ['id', 'created', 'modified', 'text', 'export_label', 'questionnaire_id', 'question_id']:
            self.assertIn(field, fields)

    def test_question_history_store(self):
        text = "Whats your best moment of 2013"
        export_text = "Best moment of 2013"
        history = QuestionTextHistory.objects.create(text=text, export_label=export_text,
                                                     questionnaire=self.questionnaire, question=self.question)
        self.failUnless(history.id)
        self.assertEqual(self.question, history.question)
        self.assertEqual(self.questionnaire, history.questionnaire)
        self.assertEqual(text, history.text)
        self.assertEqual(export_text, history.export_label)