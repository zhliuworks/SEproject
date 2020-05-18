from django.test import TestCase
from . import models


class CourseTest(TestCase):
    def setUp(self):
        course1 = models.Course.objects.create(cno='111',
                                               name='软件工程',
                                               credit=1,
                                               mean_score=80,
                                               fail_rate=0)
        course1.teacher_set.create(tno='001',
                                   name='myh',
                                   title='jiaosshou',
                                   email='myh@sjtu.edu.cn',
                                   sex='female',
                                   institute='dian_yuan',
                                   department='xinxianquan',
                                   address='lue',
                                   resume='lue',
                                   )

    def test_output_info(self):
        course1 = models.Course.objects.get(cno='111')
        self.assertEqual(course1.name, '软件工程')
        self.assertEqual(course1.credit, 1)

        teacher1 = models.Teacher.objects.get(tno='001')
        self.assertEqual(teacher1.name, 'myh')
        self.assertEqual(teacher1.sex, 'female')


class UrlResponseTest(TestCase):
    def test_index(self):
        response = self.client.get('/course/')
        self.assertEqual(response.status_code, 302)

    def test_upload_file(self):
        response = self.client.get('/course/upload/')
        self.assertEqual(response.status_code, 302)

    def test_upload_file_action(self):
        response = self.client.get('/course/upload/action/')
        self.assertEqual(response.status_code, 302)