Feature: Permissions menu
    Scenario: Data submitter view
        Given I am logged in as a data submitter
        Then I should not see the users and questionnaire links
        And I should see home, extract and attachments links

    Scenario: Global admin view
        Given I am logged in as a global admin
        Then I should see manage JRF, users, question bank, extract and attachments links
        Given I have four finalised questionnaires
        And I have two draft questionnaires for two years
        And I visit manage JRF page
        And I should see a list of finalised questionnaires
        And I should see a list of draft questionnaires