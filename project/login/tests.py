from django.test import TestCase
from . import models


class UserTest(TestCase):
    def setUp(self):
        models.User.objects.create(sno='518021910692',
                                   name='xll',
                                   nickname='xll2333',
                                   password='12345',
                                   email='12345@sjtu.edu.cn',
                                   sex='male',
                                   institute='chuan_jian',
                                   major='engineering mechanics')

    def test_output_info(self):
        user = models.User.objects.get(sno='518021910692')
        self.assertEqual(user.name, 'xll')
        self.assertEqual(user.sex, 'male')


class UrlResponseTest(TestCase):
    def test_index(self):
        response = self.client.get('/login/index/')
        self.assertEqual(response.status_code, 302)

    def test_login(self):
        response = self.client.get('/login/login/')
        self.assertEqual(response.status_code, 200)

    def test_register(self):
        response = self.client.get('/login/register/')
        self.assertEqual(response.status_code, 200)

    def test_logout(self):
        response = self.client.get('/login/logout/')
        self.assertEqual(response.status_code, 302)
