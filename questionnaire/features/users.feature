Feature: User management
    Scenario: User login
        Given I am registered user
        And I visit the login page
        And I fill in the login credentials
        And I submit the form
        Then I should be redirected home page
        And I should see my username and the logout link
        When I click the logout link
        Then I should see the login page again

    Scenario: User login with invalid credentials
        Given I visit the login page
        And I fill in invalid user credentials
        And I submit the form
        Then I should see an error message

    Scenario: User accessing extract page without logging in
        Given I visit the extract page
        When I fill in the login credentials
        Then I should see the extract page