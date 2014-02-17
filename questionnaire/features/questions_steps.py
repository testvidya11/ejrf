from lettuce import step, world
from questionnaire.features.pages.questions import QuestionListingPage
from questionnaire.models import Question


@step(u'And I have 100 questions')
def and_i_have_100_questions(step):
    for i in range(0, 100):
        Question.objects.create(text="When will you be %s years old" % i,
                                instructions="question %s answer sensibly" % i, UID="%s" % i)

@step(u'And I visit the question listing page')
def and_i_visit_the_question_listing_page(step):
    world.page.click_by_id('id-question-bank-link')
    world.page = QuestionListingPage(world.browser)

@step(u'Then I should see all questions paginated')
def then_i_should_see_all_questions_paginated(step):
    for i in range(0, 4):
        world.page.is_text_present("When will you be %s years old" % i, instructions="question %s answer sensibly" % i, UID="%s" % i)
    world.page.click_link_by_text("2")

@step(u'And I click add new question page')
def and_i_click_add_new_question_page(step):
    world.page.click_by_id('id-add-new-question-link')

@step(u'And I fill in the question details')
def and_i_fill_in_the_question_details(step):
    world.data = {'text': 'How many measles cases did you find this year',
                  'instructions': 'Just give an answer',
                  'short_instruction': 'Answer please'}
    world.page.fill_form(world.data)
    world.page.select('answer_type', 'Number')

@step(u'Then I should see the question created')
def then_i_should_see_the_question_created(step):
    world.page.is_text_present("Question successfully created")

@step(u'And I click save question button')
def and_i_click_save_question_button(step):
    world.page.click_by_css('.submit')