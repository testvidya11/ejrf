from django.contrib.auth.models import User, Group, Permission
from questionnaire.forms.user_profile import UserProfileForm
from questionnaire.models import Country, Region, UserProfile, Organization
from questionnaire.tests.base_test import BaseTest


class UserProfileFormTest(BaseTest):

    def setUp(self):
        self.region = Region.objects.create(name="Afro")
        self.uganda = Country.objects.create(name="uganda", code="UGX")
        self.global_admin = Group.objects.create(name='Global Admin')
        self.organization = Organization.objects.create(name="UNICEF")

        self.region.countries.add(self.uganda)
        self.form_data = {
            'username': 'user',
            'password1': 'kant',
            'password2': 'kant',
            'email': 'raj@ni.kant',
            'country': self.uganda.id,
            'region': self.region.id,
            'organization': self.organization.id,
            'groups': self.global_admin.id
        }

    def test_valid(self):
        user_profile_form = UserProfileForm(self.form_data)
        self.assertTrue(user_profile_form.is_valid())
        user = user_profile_form.save()
        saved_user = User.objects.get(username='user')
        self.failUnless(saved_user.id)
        self.assertEqual(1, len(saved_user.groups.all()))
        self.assertIn(self.global_admin, saved_user.groups.all())

        user_profile = UserProfile.objects.filter(user=user)
        self.failUnless(user_profile)
        self.assertEqual(user_profile[0].region, self.region)
        self.assertEqual(user_profile[0].country, self.uganda)
        self.assertEqual(user_profile[0].organization, self.organization)

    def test_email_already_used(self):
        form_data = self.form_data
        User.objects.create(email=form_data['email'])

        user_form = UserProfileForm(form_data)
        self.assertFalse(user_form.is_valid())
        message = "%s is already associated to a different user." % form_data['email']
        self.assertEquals(user_form.errors['email'], [message])

    def test_clean_username_no_duplicates_on_create(self):
        form_data = self.form_data
        User.objects.create(username=form_data['username'])
        user_form = UserProfileForm(form_data)
        self.assertFalse(user_form.is_valid())
        message = "%s is already associated to a different user." % form_data['username']
        self.assertEquals(user_form.errors['username'], [message])

    def test_clean_confirm_password(self):
        form_data = self.form_data
        form_data['password2'] = 'tank'
        user_form = UserProfileForm(form_data)
        self.assertFalse(user_form.is_valid())
        message = "The two password fields didn't match."
        self.assertEquals(user_form.errors['password2'], [message])

        form_data['password2'] = form_data['password1']
        user_form = UserProfileForm(form_data)
        self.assertTrue(user_form.is_valid())

    def test_country_must_belong_to_selected_region(self):
        sudan = Country.objects.create(name="Sudan", code="SDX")
        form_data = self.form_data.copy()
        form_data['country'] = sudan.id
        user_form = UserProfileForm(form_data)
        self.assertFalse(user_form.is_valid())
        message = "%s does not belong to region %s" % (sudan.name, self.region.name)
        self.assertEquals(user_form.errors['country'], [message])

    def test_valid_when_region_is_blank(self):
        form_data = self.form_data.copy()
        form_data['country'] = ''
        form_data['region'] = ''
        user_form = UserProfileForm(form_data)
        self.assertTrue(user_form.is_valid())

    def test_invalid_when_country_is_given_with_no_region(self):
        form_data = self.form_data.copy()
        form_data['country'] = self.uganda.id
        form_data['region'] = ''
        user_form = UserProfileForm(form_data)
        self.assertFalse(user_form.is_valid())
        message = "%s should belong to a region" % self.uganda.name
        self.assertEquals(user_form.errors['country'], [message])