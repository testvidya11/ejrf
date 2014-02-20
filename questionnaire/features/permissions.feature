Feature: Permissions menu
    Scenario: Data submitter view
        Given I am logged in as a data submitter
        Then I should not see the users and questionnaire links
        And I should see home, extract and attachments links