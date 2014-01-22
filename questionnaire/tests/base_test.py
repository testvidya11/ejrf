import csv
from django.contrib.auth.models import User
from django.test import TestCase


class BaseTest(TestCase):

    def write_to_csv(self, mode, data, csvfilename='test.csv'):
        with open(csvfilename, mode) as fp:
            file = csv.writer(fp, delimiter=',')
            file.writerows(data)
            fp.close()

    def create_user_with_no_permissions(self):
        self.user = User.objects.create(username="user", email="user@mail.com")
        self.user.set_password("pass")
        self.user.save()

    def login_user(self):
        self.client.login(username='user', password='pass')