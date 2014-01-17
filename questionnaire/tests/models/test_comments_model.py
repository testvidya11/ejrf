from django.contrib.auth.models import User
from questionnaire.models import Question, Country, NumericalAnswer
from questionnaire.models.comments import Comment
from questionnaire.tests.base_test import BaseTest


class CommentTest(BaseTest):

    def setUp(self):
        self.question = Question.objects.create(text='Uganda Revision 2014 what what?', UID='abc123', answer_type='Text')
        self.country = Country.objects.create(name="Peru")
        self.tony = User.objects.create(username="Tony")
        self.montana = User.objects.create(username="Montana")
        self.answer = NumericalAnswer.objects.create(question=self.question, country=self.country, response=11.2)

    def test_comment_fields(self):
        comment = Comment()
        fields = [str(item.attname) for item in comment._meta.fields]
        self.assertEqual(5, len(fields))
        for field in ['id', 'created', 'modified', 'text', 'user_id']:
            self.assertIn(field, fields)

    def test_comments_store(self):
        tony_comment = Comment.objects.create(user=self.tony, text="This is an absurd figure")
        montana_comment = Comment.objects.create(user=self.montana, text="This is an absurd figure")
        self.answer.comments.add(tony_comment)
        self.answer.comments.add(montana_comment)
        answer_comments = self.answer.comments.all()

        self.failUnless(tony_comment.id)
        self.failUnless(montana_comment.id)
        self.assertEqual(2, answer_comments.count())
        self.assertIn(montana_comment, answer_comments)
        self.assertIn(tony_comment, answer_comments)