import csv
from django.contrib.auth.models import User
from django.test import TestCase
from urllib import quote
from questionnaire.models import Country, UserProfile


class BaseTest(TestCase):

    def write_to_csv(self, mode, data, csvfilename='test.csv'):
        with open(csvfilename, mode) as fp:
            _file = csv.writer(fp, delimiter=',')
            _file.writerows(data)
            fp.close()

    def create_user_with_no_permissions(self):
        self.user = User.objects.create(username="user", email="user@mail.com")
        uganda = Country.objects.create(name="Uganda")
        UserProfile.objects.create(user=self.user, country=uganda)

        self.user.set_password("pass")
        self.user.save()
        return self.user

    def login_user(self):
        self.client.login(username='user', password='pass')

    def assert_login_required(self, url):
        self.client.logout()
        response = self.client.get(url)
        self.assertRedirects(response, expected_url='/accounts/login/?next=%s' % quote(url),
                             status_code=302, target_status_code=200, msg_prefix='')
