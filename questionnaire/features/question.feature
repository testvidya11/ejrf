Feature: Questions feature
  Scenario: List questions
    Given I have a global admin user
    And I have 100 questions
    And I logged in the user
    And I visit the question listing page
    Then I should see all questions paginated

  Scenario: Create a simple question
    Given I have a global admin user
    And I logged in the user
    And I visit the question listing page
    And I click add new question page
    And I fill in the question details
    And I click save question button
    Then I should see the question created