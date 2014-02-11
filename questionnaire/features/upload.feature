Feature: Support document upload
  Scenario: Upload PDF file
   Given I am logged in as a data submitter
   And I have a questionnaire with sections and subsections
   And I have a pdf document
   And I visit that questionnaires section page
   And I click the upload support document link
   Then I should see the upload form
   When I select a file to upload 
   And I click upload button
   Then I should see the file was uploaded successfully
   And I should be able to download the file

  Scenario: Upload Unacceptable File Extension
    Given I am logged in as a data submitter
    And I have a questionnaire with sections and subsections
    And I have a zip file
    And I visit that questionnaires section page
    And I click the upload support document link
    Then I should see the upload form
    When I select a file to upload
    And I click upload button
    Then I should see an error that the file type is not supported