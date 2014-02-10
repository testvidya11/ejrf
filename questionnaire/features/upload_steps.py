from lettuce import world, step
from mock import mock_open, patch
from questionnaire.features.pages.uploads import UploadDocumentPage


@step(u'And I click the upload support document link')
def and_i_click_the_upload_support_document_link(step):
    world.page.click_by_id('upload-file')

@step(u'Then I should see the upload form')
def then_i_should_see_the_upload_form(step):
    world.page = UploadDocumentPage(world.browser, world.questionnaire)
    world.page.validate_url()
    world.page.validate_upload_form({'Support document': 'path'})

@step(u'When I select a file to upload')
def when_i_select_a_file_to_upload(step):
    world.page.input_file(world.filename)

@step(u'And I click upload button')
def and_i_click_upload_button(step):
    world.page.click_by_id('upload-btn')

@step(u'Then I should see the file was uploaded successfully')
def then_i_should_see_the_file_was_uploaded_successfully(step):
    world.page.is_text_present("File was uploaded successfully")

@step(u'And I have a pdf document')
def and_i_have_a_pdf_document(step):
    world.filename = 'sample_document.pdf'
    m = mock_open()
    with patch('__main__.open', m, create=True):
        with open(world.filename, 'w') as document:
            document.write("Some stuff")

@step(u'And I should be able to download the file')
def and_i_should_be_able_to_download_the_file(step):
    world.page.is_text_present(world.filename)