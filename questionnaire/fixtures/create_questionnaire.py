from questionnaire.models import Questionnaire, Section, SubSection, Question

questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")
section = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                                              questionnaire=questionnaire, name="Reported Cases")

sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1, section=section)

question1 = Question.objects.create(text='Disease', UID='abc123', answer_type='MultiChoice')


