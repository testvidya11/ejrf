from questionnaire.models import Answer, AnswerGroup


class UserQuestionnaireService(object):

    def __init__(self, user, questionnaire):
        self.user = user
        self.country = user.user_profile.country
        self.questionnaire = questionnaire

    def all_answers(self):
        return Answer.objects.filter(country=self.country).select_subclasses()

    def questionnaire_answers(self):
        answer_groups = AnswerGroup.objects.filter(grouped_question__subsection__section__questionnaire=self.questionnaire)
        return Answer.objects.filter(country=self.country, answergroup__in=answer_groups).select_subclasses()

    def submit(self):
        self_answers_in = self.questionnaire_answers()
        for answer in self_answers_in:
            answer.status = Answer.SUBMITTED_STATUS
            answer.save()

    def answer_version(self):
        answers = self.questionnaire_answers()
        if not answers.exists():
            return 0

        draft_answers = answers.filter(status=Answer.DRAFT_STATUS)
        if draft_answers.exists():
            return draft_answers.latest('modified').version

        return answers.latest('modified').version + 1
