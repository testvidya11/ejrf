Feature: Questionnaire feature
  Background:
    Given I am logged in

  Scenario: Show questionnaire form
    And I have a questionnaire with sections and subsections
    And I have a question group and questions in that group
    And I set orders for the questions in the group
    And I visit that questionnaires section page
    Then I should see the questions
    And I should see the answer fields
    And I should see the instructions
