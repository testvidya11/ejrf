Feature: Subsection feature
    Scenario: Create a subsection
        Given I am logged in as a global admin
        And I have a questionnaire with sections and subsections
        And I visit that questionnaires section page
        And I click add new subsection link
        Then I should see a new subsection modal
        When i fill in the subsection data
        And I save the subsection
        Then I should see the subsection I just created