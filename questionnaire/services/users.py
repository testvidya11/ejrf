from questionnaire.models import Answer, AnswerGroup


class UserQuestionnaireService(object):

    def __init__(self, user, questionnaire):
        self.user = user
        self.country = user.user_profile.country
        self.questionnaire = questionnaire
        self.unanswered_section = None
        self.answers_in_questionnaire = self.questionnaire_answers()
        self.version = self.answer_version()
        self.answers = self.answers_in_questionnaire.filter(version=self.version)

    def all_answers(self):
        return Answer.objects.filter(country=self.country).select_subclasses()

    def questionnaire_answers(self):
        answer_groups = AnswerGroup.objects.filter(grouped_question__subsection__section__questionnaire=self.questionnaire)
        return Answer.objects.filter(country=self.country, answergroup__in=answer_groups).select_subclasses()

    def submit(self):
        for answer in self.answers:
            answer.status = Answer.SUBMITTED_STATUS
            answer.save()

    def answer_version(self):
        answers = self.answers_in_questionnaire
        if not answers.exists():
            return 0

        draft_answers = answers.filter(status=Answer.DRAFT_STATUS)
        if draft_answers.exists():
            return draft_answers.latest('modified').version

        return answers.latest('modified').version + 1

    def required_sections_answered(self):
        for section in self.questionnaire.sections.all():
            if not self.answered_required_questions_in(section):
                self.unanswered_section = section
                return False
        return True

    def answered_required_questions_in(self, section):
        required_question_in_section = filter(lambda question: question.is_required, section.ordered_questions())
        return self.answers.filter(question__in=required_question_in_section).count() == len(required_question_in_section)
