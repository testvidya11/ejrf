Feature: Location types
    Scenario: List Location types
      Given I have three location types
      And I visit the list location types page
      Then I should see the list of location types
