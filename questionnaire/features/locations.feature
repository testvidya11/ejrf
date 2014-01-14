Feature: Location types
    Scenario: List Regions
      Given I have two regions
      And I visit the list regions page
      Then I should see the list of regions

    Scenario: List Countries
      Given I have two countries in a region
      And I visit the list countries page in that region
      Then I should see the list of countries in that region
