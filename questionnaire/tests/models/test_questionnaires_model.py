from questionnaire.models.questionnaires import Questionnaire
from questionnaire.tests.base_test import BaseTest


class QuestionnaireTest(BaseTest):

    def test_questionnaire_fields(self):
        questionnaire = Questionnaire()
        fields = [str(item.attname) for item in questionnaire._meta.fields]
        self.assertEqual(5, len(fields))
        for field in ['id', 'created', 'modified', 'name', 'description']:
            self.assertIn(field, fields)

    def test_questionnaire_store(self):
        questionnaire = Questionnaire.objects.create(name="Uganda Revision 2014", description="some description")
        self.failUnless(questionnaire.id)
        self.assertEqual("Uganda Revision 2014", questionnaire.name)