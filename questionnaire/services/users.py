from questionnaire.models import Answer, AnswerGroup


class UserService(object):

    def __init__(self, user):
        self.user = user
        self.country = user.user_profile.country

    def answers(self):
        return Answer.objects.filter(country=self.country).select_subclasses()

    def answers_in(self, questionnaire):
        answer_groups = AnswerGroup.objects.filter(grouped_question__subsection__section__questionnaire=questionnaire)
        return Answer.objects.filter(country=self.country, answergroup__in=answer_groups).select_subclasses()

    def submit(self, questionnaire):
        self_answers_in = self.answers_in(questionnaire)
        for answer in self_answers_in:
            answer.status = Answer.SUBMITTED_STATUS
            answer.save()
