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

    Scenario: List users
        Given I have a global admin user
        And I have 100 other users
        And I logged in the user
        And I visit the user listing page
        Then I should see the list of users paginated

    Scenario: Create a global admin user
        Given I have a global admin user
        And I have 100 other users
        And I logged in the user
        And I visit the user listing page
        And I click an new user button
        And I fill in the user information
        And I submit the form
        Then I should see that the user was successfully created
        And I should see the user listed on the listing page