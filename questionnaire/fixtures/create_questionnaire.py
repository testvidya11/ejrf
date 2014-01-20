from questionnaire.models import Questionnaire, Section, SubSection, Question, QuestionGroup, QuestionOption, QuestionGroupOrder

questionnaire = Questionnaire.objects.create(name="JRF 2013 Core English", description="From dropbox as given by Rouslan")

########################################################################################################
# SECTION: Reported Cases of Selected Vaccine Preventable Diseases (VPDs)
########################################################################################################
section_1 = Section.objects.create(title="Reported Cases of Selected Vaccine Preventable Diseases (VPDs)", order=1,
                                              questionnaire=questionnaire, name="Reported Cases")

sub_section = SubSection.objects.create(title="Reported cases for the year 2013", order=1, section=section_1)

question1 = Question.objects.create(text='Disease', UID='C00001', answer_type='MultiChoice')
question2 = Question.objects.create(text='A. Total Cases', short_instruction="Include clinically, epidemiologically, and"
" laboratory-confirmed cases. Do not include suspect cases.",
instructions="""<h2><strong>Column A</strong> refers only to <strong>CONFIRMED</strong> cases, including those confirmed clinically, epidemiologically, or by laboratory investigation.&nbsp;<br />
<br />
<strong>Clinically-confirmed case:</strong> a case that meets the clinical case definition of the country<br />
<br />
<strong>Epidemiologically-confirmed case: </strong>a case that meets the clinical case definition and is linked epidemiologically to a laboratory-confirmed case<br />
<br />
<strong>Laboratory-confirmed case:</strong> a case that meets the clinical case definition and is confirmed by laboratory investigation<br />
<br />
Cases that have been <strong>discarded</strong> following laboratory investigation should <strong>NOT</strong> be included in these columns.</h2>
""",
UID='C00002', answer_type='Number')

question3 = Question.objects.create(text='B. Number of cases tested',
                                    instructions="Enter the total number of cases for which specimens were collected, and tested in laboratory",
                                    UID='C00003', answer_type='Number')

question4 = Question.objects.create(text='C. Number of cases positive',
                                    instructions="Include only those cases found positive for the infectious agent.",
                                    UID='C00004', answer_type='Number')

parent = QuestionGroup.objects.create(subsection=sub_section, order=1)
parent.question.add(question1, question2)

sub_group = QuestionGroup.objects.create(subsection=sub_section, parent=parent, name="Laboratory Investigation")
sub_group.question.add(question3, question4)

QuestionOption.objects.create(text="Diphteria", question=question1)
QuestionOption.objects.create(text="Measles", question=question1)
QuestionOption.objects.create(text="Neonatal tetanus (NT)", question=question1)
QuestionOption.objects.create(text="Total tetanus (all tetanus including NT)", question=question1)
QuestionOption.objects.create(text="Pertussis", question=question1)
QuestionOption.objects.create(text="Yellow fever", question=question1)
QuestionOption.objects.create(text="Japanese encephalitis", question=question1)
QuestionOption.objects.create(text="Mumps", question=question1)
QuestionOption.objects.create(text="Rubella", question=question1)
QuestionOption.objects.create(text="Congenital rubella syndrome", question=question1)

sub_section_2 = SubSection.objects.create(title="Presence of surveillance systems", order=2, section=section_1)
question5 = Question.objects.create(text="""Is there a surveillance system in place for invasive bacterial diseases (for example bacterial meningitis,
sepsis or bacteremic pneumonia), in which suspected cases are confirmed by laboratory and surveillance data could provide information to allow evaluation
of the impact of vaccination against Hib and/or Pneumococcus?""",
                                      UID='C00005',
                                      answer_type='MultiChoice')
question_5_group = QuestionGroup.objects.create(subsection=sub_section, order=2)
question_5_group.question.add(question5)

QuestionOption.objects.create(text="Yes", question=question5)
QuestionOption.objects.create(text="No", question=question5)
QuestionOption.objects.create(text="NR", question=question5)


question6 = Question.objects.create(text="""Is there a surveillance system in place for rotavirus diarrhoea, in which suspected cases are confirmed
 by laboratory and surveillance data could provide information to allow evaluation of the impact of vaccination against rotavirus?""",
                                      UID='C00006',
                                      answer_type='MultiChoice')

question_6_group = QuestionGroup.objects.create(subsection=sub_section, order=3)
question_6_group.question.add(question6)

QuestionOption.objects.create(text="Yes", question=question6)
QuestionOption.objects.create(text="No", question=question6)
QuestionOption.objects.create(text="NR", question=question6)

QuestionGroupOrder.objects.create(question=question1, question_group=parent, order=1)
QuestionGroupOrder.objects.create(question=question2, question_group=parent, order=2)
QuestionGroupOrder.objects.create(question=question3, question_group=parent, order=3)
QuestionGroupOrder.objects.create(question=question4, question_group=parent, order=4)
QuestionGroupOrder.objects.create(question=question5, question_group=question_5_group, order=1)
QuestionGroupOrder.objects.create(question=question6, question_group=question_6_group, order=1)


########################################################################################################
# SECTION: School Based Immunization
########################################################################################################
section_2 = Section.objects.create(title="School Based Immunization", order=2,
                                    questionnaire=questionnaire, name="School Imm Delivery", description="""Please complete this section if in your country
routine immunization is given to school-aged children using the school as a venue. For the purpose of this section,
please consider as ""routine"" only those doses that are part of the national immunization schedule.
Do not include doses given in campaigns, even if during those campaigns schools were used as vaccination sites.""")
sub_section_3 = SubSection.objects.create(order=1, section=section_2)

question7 = Question.objects.create(text='Are any routine doses of vaccine given to children at school?', UID='C00007', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question7)
QuestionOption.objects.create(text="No", question=question7)
QuestionOption.objects.create(text="NR", question=question7)

question_7_group = QuestionGroup.objects.create(subsection=sub_section_3, order=1)
question_7_group.question.add(question7)

QuestionGroupOrder.objects.create(question=question7, question_group=question_7_group, order=1)

question8 = Question.objects.create(text='Vaccine procurement', UID='C00008', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question8)
QuestionOption.objects.create(text="No", question=question8)

question9 = Question.objects.create(text='Vaccinators', UID='C00009', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question9)
QuestionOption.objects.create(text="No", question=question9)

question10 = Question.objects.create(text='Supervision', UID='C00010', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question10)
QuestionOption.objects.create(text="No", question=question10)


question11 = Question.objects.create(text='Planing', UID='C00011', answer_type='MultiChoice')
QuestionOption.objects.create(text="Yes", question=question11)
QuestionOption.objects.create(text="No", question=question11)

question_8_11__group = QuestionGroup.objects.create(subsection=sub_section_3, order=2)
sub_group_2 = QuestionGroup.objects.create(subsection=sub_section, parent=question_8_11__group, name="Which"
"activities the EPI Program responsible for (and not the school staff per se ):")

sub_group_2.question.add(question8, question9, question10, question11)

QuestionGroupOrder.objects.create(question=question8, question_group=question_8_11__group, order=1)
QuestionGroupOrder.objects.create(question=question9, question_group=question_8_11__group, order=2)
QuestionGroupOrder.objects.create(question=question10, question_group=question_8_11__group, order=3)
QuestionGroupOrder.objects.create(question=question11, question_group=question_8_11__group, order=4)

#################################### next sub
sub_section_4 = SubSection.objects.create(order=2, section=section_2, title="Routine Immunization given at school"
    "(please complete one row  for each grade level or age and vaccine", instructions="""
     Please complete the table by using one row for each vaccine and each target group. Examples: if TT and MR is given in grade 2 and TT in grade 8, use three rows (TT-grade 2; MR-grade 2; TT-grade 8); if TT and MR are given to children aged 8 years, and TT to children aged 14 years, use three rows (TT-8 years; MR-8 years; TT-14 years)
     """)
