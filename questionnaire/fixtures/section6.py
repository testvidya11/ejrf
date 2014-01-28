from django.core import serializers
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionOption, QuestionGroupOrder

questionnaire = Questionnaire.objects.get(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")

section_1 = Section.objects.create(order=6, questionnaire=questionnaire, name="Indicators",
                                   title="Immunization System Indicators")

sub_section = SubSection.objects.create(order=1, section=section_1, title="Planning and management")

question1 = Question.objects.create(text="Does the country have a  multi-year plan (MYP) for immunization?",
                                    UID='C00074', answer_type='MultiChoice')

QuestionOption.objects.create(text="Yes", question=question1)
QuestionOption.objects.create(text="No", question=question1)
QuestionOption.objects.create(text="NR", question=question1)

question2 = Question.objects.create(text="If yes, what years does the MYP cover?", UID='C00075', answer_type='Text')


question3 = Question.objects.create(text="Did the country have an annual workplan for immunization activities in 2013?",
                                    UID='C00076', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question3)
QuestionOption.objects.create(text="No", question=question3)
QuestionOption.objects.create(text="NR", question=question3)


question4 = Question.objects.create(text="Number of districts with updated micro-plans to raise immunization coverage",
                                    UID='C00077', answer_type='Text')

parent1 = QuestionGroup.objects.create(subsection=sub_section, order=1)
parent1.question.add(question2, question1, question3, question4)
QuestionGroupOrder.objects.create(question=question1, question_group=parent1, order=1)
QuestionGroupOrder.objects.create(question=question2, question_group=parent1, order=2)
QuestionGroupOrder.objects.create(question=question3, question_group=parent1, order=3)
QuestionGroupOrder.objects.create(question=question4, question_group=parent1, order=4)


sub_section1 = SubSection.objects.create(order=2, section=section_1, title="National Immunization Advisory Mechanism")
question_1 = Question.objects.create(text="Did  your country have a standing technical advisory group on immunization in 2013? If no, please skip to next page",
                                     UID='C00078', answer_type='MultiChoice', instructions="")
QuestionOption.objects.create(text="Yes", question=question_1)
QuestionOption.objects.create(text="No", question=question_1)
QuestionOption.objects.create(text="NR", question=question_1)

question_2 = Question.objects.create(text="Does the advisory group have formal written terms of reference?",
                                     UID='C00078', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_2)
QuestionOption.objects.create(text="No", question=question_2)
QuestionOption.objects.create(text="NR", question=question_2)

question_3 = Question.objects.create(text="Are there legislative or administrative basis for the advisory group?",
                                     UID='C00079', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_3)
QuestionOption.objects.create(text="No", question=question_3)
QuestionOption.objects.create(text="NR", question=question_3)


#subgroup
question_4 = Question.objects.create(text="A. pediatrics", UID='C00080', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_4)
QuestionOption.objects.create(text="No", question=question_4)
QuestionOption.objects.create(text="NR", question=question_4)

question_5 = Question.objects.create(text="B. public health", UID='C00080', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_5)
QuestionOption.objects.create(text="No", question=question_5)
QuestionOption.objects.create(text="NR", question=question_5)

question_6 = Question.objects.create(text="C. infectious diseases", UID='C00081', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_6)
QuestionOption.objects.create(text="No", question=question_6)
QuestionOption.objects.create(text="NR", question=question_6)

question_7 = Question.objects.create(text="D. epidemiology", UID='C00082', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_7)
QuestionOption.objects.create(text="No", question=question_7)
QuestionOption.objects.create(text="NR", question=question_7)

question_8 = Question.objects.create(text="E. immunology", UID='C00083', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_8)
QuestionOption.objects.create(text="No", question=question_8)
QuestionOption.objects.create(text="NR", question=question_8)

question_9 = Question.objects.create(text="F. other: please specify under explanatory comments", UID='C00084',
                                     answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question_9)
QuestionOption.objects.create(text="No", question=question_9)
QuestionOption.objects.create(text="NR", question=question_9)


# *************************************************************
#end of subgroup
#******************************************************************

question_10 = Question.objects.create(text="How many times did the advisory group meet in 2013?", UID='C00085', answer_type='Number',
                                      instructions="Altough groups can have ad hoc meetings when necessary, it is recommended to have meetings at regular intervals on predetermined dates and at least once a year. This ensures that the group remains active and recommendations remain current. And it also facilitates increased attendance rates allowing members to plan the time commitment into their schedules in advance.")

question_11 = Question.objects.create(text="Were the agenda and background documents distributed (at least 1 week) prior to meetings in 2013?", UID='C00086', answer_type='MultiChoice',
                                      instructions="An agenda for each NITAG meeting should be distributed in advance to all members. This allows to properly prepare for the meeting. Ideally, background materials would also be distributed prior to the meetings to provide members with current research available on the topic. The distribution of this material facilitates a well rounded, informed discussion during the meeting, provided the members receive the information within sufficient time prior to the meeting.")
QuestionOption.objects.create(text="Yes", question=question_11)
QuestionOption.objects.create(text="No", question=question_11)
QuestionOption.objects.create(text="NR", question=question_11)

question_12 = Question.objects.create(text="Are members of the advisory group required to disclose conflict of interest?", UID='C00087', answer_type='MultiChoice',
                                      instructions="To ensure transparency and avoid conflicts of interests as much as possible, NITAGs should require all members to declare their interests prior to official appointment. A conflict of interest occurs in the case of the member having a personal investment, activity, or relationship which may affect, or appear to affect, their responsibilities of the NITAG. A conflict of interest, whether real or perceived, can compromise the quality of the recommendations made by the group and can compromise the reputation and integrity of the NITAG. It can also compromise the credibility of the group, even if it would not influence the recommendations. Therefore, interests should be declared prior to the individual’s official appointment as a core member. The individual should only be appointed as a member if the person is considered an independent expert so that that their interests do not compromise the integrity of the NITAG.")
QuestionOption.objects.create(text="Yes", question=question_12)
QuestionOption.objects.create(text="No", question=question_12)
QuestionOption.objects.create(text="NR", question=question_12)

question_13 = Question.objects.create(text="Does the advisory group have a website or webpage? If yes, please provide the address in next box (explanatory comments)", UID='C00088', answer_type='MultiChoice',
                                      instructions=" WHO  encourages sharing experiences between countries and their NITAGs. In order to facilitate experience sharing process, WHO would like to circulate website or webpage addresses of NITAGs to others interested.")
QuestionOption.objects.create(text="Yes", question=question_13)
QuestionOption.objects.create(text="No", question=question_13)
QuestionOption.objects.create(text="NR", question=question_13)

parent2 = QuestionGroup.objects.create(subsection=sub_section1, order=1)
parent2.question.add(question_1, question_2, question_3, question_10, question_11, question_12, question_13)
QuestionGroupOrder.objects.create(question=question_1, question_group=parent2, order=1)
QuestionGroupOrder.objects.create(question=question_2, question_group=parent2, order=2)
QuestionGroupOrder.objects.create(question=question_3, question_group=parent2, order=3)

parent3 = QuestionGroup.objects.create(subsection=sub_section1, order=2, parent=parent2)
parent3.question.add(question_4, question_5, question_6, question_7, question_8, question_9)

QuestionGroupOrder.objects.create(question=question_4, question_group=parent2, order=4)
QuestionGroupOrder.objects.create(question=question_5, question_group=parent2, order=5)
QuestionGroupOrder.objects.create(question=question_6, question_group=parent2, order=6)
QuestionGroupOrder.objects.create(question=question_7, question_group=parent2, order=7)
QuestionGroupOrder.objects.create(question=question_8, question_group=parent2, order=8)
QuestionGroupOrder.objects.create(question=question_9, question_group=parent2, order=9)
QuestionGroupOrder.objects.create(question=question_9, question_group=parent2, order=10)
QuestionGroupOrder.objects.create(question=question_9, question_group=parent2, order=11)
QuestionGroupOrder.objects.create(question=question_9, question_group=parent2, order=12)
QuestionGroupOrder.objects.create(question=question_9, question_group=parent2, order=13)

################################################################################################
sub_section2 = SubSection.objects.create(order=3, section=section_1, title="District coverage reported for routine immunization services in 2013")

question_1 = Question.objects.create(text="DTP3", UID='C00089', answer_type='MultiChoice')
question_2 = Question.objects.create(text="A. Coverage is <50%", UID='C00090', answer_type='Number')
question_3 = Question.objects.create(text="B. Coverage is 50-79%", UID='C00091', answer_type='Number')
question_4 = Question.objects.create(text="A. Coverage is 80-89%", UID='C00092', answer_type='Number')
question_5 = Question.objects.create(text="A. Coverage is 90-94%", UID='C00093', answer_type='Number')
question_6 = Question.objects.create(text="A. Coverage is >=95%", UID='C00094', answer_type='Number')


data = serializers.serialize("json", [section_1, sub_section, sub_section1, sub_section2])
print data

data = serializers.serialize("json", [parent1, parent2, parent3])
print data

data = serializers.serialize("json", parent1.question.all())
print data

data = serializers.serialize("json", parent2.question.all())
print data

data = serializers.serialize("json", parent3.question.all())
print data

data = serializers.serialize("json", parent1.orders.all())
print data

data = serializers.serialize("json", parent2.orders.all())
print data

data = serializers.serialize("json", parent3.orders.all())
print data