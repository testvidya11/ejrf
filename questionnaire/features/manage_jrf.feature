Feature: Manage JRF

    Scenario: Global admin view
        Given I am logged in as a global admin
        Then I should see manage JRF, users, question bank, extract and attachments links
        Given I have four finalised questionnaires
        And I have two draft questionnaires for two years
        And I visit manage JRF page
        Then I should see a list of the three most recent finalised questionnaires
        And I should see a list of draft questionnaires
        
    Scenario: Viewing older finalised questionnaires
        Given I am logged in as a global admin
        Given I have four finalised questionnaires
        And I visit manage JRF page
        Then I should see a list of the three most recent finalised questionnaires
        And When I click Older
        Then I should also see the fourth finalised questionnaire