from time import sleep
from lettuce import step, world
from questionnaire.features.pages.questionnaires import QuestionnairePage
from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionGroupOrder


@step(u'And I have a questionnaire with sections and subsections')
def and_i_have_a_questionnaire_with_sections_and_subsections(step):
    world.questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")

    world.section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                                                  questionnaire=world.questionnaire, name="Reported Cases")

    world.sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1, section=world.section_1)

@step(u'And I have a question group and questions in that group')
def and_i_have_a_question_group_and_questions_in_that_group(step):
    world.question1 = Question.objects.create(text='Disease', UID='C00001', answer_type='MultiChoice')
    world.question2 = Question.objects.create(text='B. Number of cases tested',
                                instructions="Enter the total number of cases for which specimens were collected, and tested in laboratory",
                                UID='C00003', answer_type='Number')

    world.question3 = Question.objects.create(text='C. Number of cases positive',
                                        instructions="Include only those cases found positive for the infectious agent.",
                                        UID='C00004', answer_type='Number')

    world.question_group = QuestionGroup.objects.create(subsection=world.sub_section, order=1, name="Immunization")
    world.question_group.question.add(world.question1, world.question3, world.question2)

@step(u'And I set orders for the questions in the group')
def and_i_set_orders_for_the_questions_in_the_group(step):
    QuestionGroupOrder.objects.create(question=world.question1, question_group=world.question_group, order=1)
    QuestionGroupOrder.objects.create(question=world.question2, question_group=world.question_group, order=2)
    QuestionGroupOrder.objects.create(question=world.question3, question_group=world.question_group, order=3)

@step(u'And I visit that questionnaires section page')
def and_i_visit_that_questionnaires_section_page(step):
    world.page = QuestionnairePage(world.browser, world.questionnaire)
    world.page.visit()

@step(u'Then I should see the questions')
def then_i_should_see_the_questions(step):
    world.page.is_text_present(world.question1.text,world.question2.text,world.question3.text)

@step(u'And I should see the answer fields')
def and_i_should_see_the_answer_fields(step):
    world.page.validate_fields()

@step(u'And I should see the instructions')
def and_i_should_see_the_instructions(step):
    world.page.validate_instructions(world.question2)

@step(u'And i have a subgroup with questions in that group')
def and_i_have_a_subgroup_with_questions_in_that_group(step):
    world.question_1a = Question.objects.create(text='Disease', UID='C00021', answer_type='MultiChoice')

    world.question_subgroup = QuestionGroup.objects.create(subsection=world.sub_section, order=1,
                                                           parent=world.question_group, name="Immunization subgroup")
    world.question_subgroup.question.add(world.question_1a)

@step(u'And I set question orders for the group and subgroup')
def and_i_set_question_orders_for_the_group_and_subgroup(step):
    QuestionGroupOrder.objects.create(question=world.question_1a, question_group=world.question_group, order=4)

@step(u'Then I should see the group title and description')
def then_i_should_see_the_group_title_and_description(step):
    world.page.is_text_present(world.question_group.name)

@step(u'And I should see the subgroup title and description')
def and_i_should_see_the_subgroup_title_and_description(step):
    world.page.is_text_present(world.question_subgroup.name)