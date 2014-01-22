class ExportToTextService:
    def __init__(self, questionnaire):
        self.questionnaire = questionnaire

    def get_formatted_responses(self):
        formatted_response = []
        questions = self.questionnaire.get_all_questions()
        for question in questions:
            answers = question.all_answers()
            for answer in answers:
                answer_format = (self.questionnaire.year, answer.country.code, str(question.UID), str(answer.response))
                formatted_response.append(["%s\t%s\t%s\t%s" % answer_format])
        return formatted_response