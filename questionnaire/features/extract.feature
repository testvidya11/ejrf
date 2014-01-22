Feature: Export responses to DEF file

	Background: 
		Given I am registered user	
	    Given I have two countries in a region
	    And I visit the login page

	Scenario: Export un filtered text
		And I logged in the user
		And I have a questionnaires
		And I have questions and their answers
		And I visit the extract page
		Then I should see a list of questionnaires
		When I click export data button
