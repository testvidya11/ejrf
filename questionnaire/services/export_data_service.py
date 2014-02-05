from questionnaire.models import AnswerGroup


class ExportToTextService:
    HEADERS = "ISO\tCountry\tYear\tField code\tQuestion text\tValue"

    def __init__(self, questionnaire):
        self.questionnaire = questionnaire

    def get_formatted_responses(self):
        formatted_response = [self.HEADERS]
        for subsection in self.questionnaire.sub_sections():
            subsection_answers = self._answers(subsection)
            formatted_response.extend(subsection_answers)
        return formatted_response

    def _answers(self, subsection):
        formatted_response = []
        for group in subsection.parent_question_groups():
            ordered_questions = group.ordered_questions()
            primary_question = ordered_questions[0]
            answer_groups = AnswerGroup.objects.filter(answer__question=primary_question)
            for index, answer_group in enumerate(answer_groups):
                answers = answer_group.answer.all().select_subclasses()
                for question in ordered_questions:
                    answer = answers.get(question=question)
                    response_row = self._format_response(answer, question, primary_question.UID, group, index)
                    formatted_response.append(response_row)
        return formatted_response

    def _format_response(self, answer, question, primary_question_uid, group, index):
        question_prefix = 'C' if question.is_core else 'R'
        answer_id = "%s_%s_%s_%d" % (question_prefix, primary_question_uid, question.UID, index + 1)
        if question.is_primary:
            primary_question_uid = question.UID
            question_option = ""
            if question.answer_type == 'MultiChoice':
                question_option = answer.response.UID
            answer_id = "%s_%s_%s_%s" % (question_prefix, primary_question_uid, question.UID, question_option)
        question_text_format = "%s | %s | %s" % (group.subsection.section.title, group.subsection.title, question.text)
        answer_format = (answer.country.code, answer.country.name, self.questionnaire.year, answer_id,
                         question_text_format, str(answer.response))
        return "%s\t%s\t%s\t%s\t%s\t%s" % answer_format
