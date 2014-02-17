Feature: Questions feature
  Scenario: List questions
    Given I have a global admin user
    And I have 100 questions
    And I logged in the user
    And I visit the question listing page
    Then I should see all questions paginated
