Feature: Manage JRF

    Scenario: Global admin view
        Given I am logged in as a global admin
        Then I should see manage JRF, users, question bank, extract and attachments links
        Given I have four finalised questionnaires
        And I have two draft questionnaires for two years
        And I visit manage JRF page
        And I should see a list of finalised questionnaires
        And I should see a list of draft questionnaires