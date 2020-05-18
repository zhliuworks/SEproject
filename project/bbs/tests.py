from django.test import TestCase
from bbs.models import Category, Post, Tag, Comment, Message
from login.models import User


class BbsTest(TestCase):
    def setUp(self):
        cate = Category.objects.create(name='测试')
        tag = Tag.objects.create(name='测试')

        user1 = User.objects.create(sno='518021910692',
                                    name='xll',
                                    nickname='xll2333',
                                    password='12345',
                                    email='12345@sjtu.edu.cn',
                                    sex='male',
                                    institute='chuan_jian',
                                    major='engineering mechanics')

        user2 = User.objects.create(sno='518021910691',
                                    name='xll',
                                    nickname='xll2333',
                                    password='12345',
                                    email='123456@sjtu.edu.cn',
                                    sex='male',
                                    institute='chuan_jian',
                                    major='engineering mechanics')

        tag.post_set.create(title='测试标题',
                            content='测试内容',
                            category=cate,
                            author=user1,)
        post = Post.objects.get(title='测试标题')

        Comment.objects.create(post=post,
                               name=user1,
                               content='测试评论',)

        Message.objects.create(title='测试私信标题',
                               content='测试私信',
                               sender=user1,
                               receiver=user2)

    def test_output_info(self):
        post = Post.objects.get(title='测试标题')
        self.assertEqual(post.content, '测试内容')
        self.assertEqual(post.category.name, '测试')
        self.assertEqual(post.author.sno, '518021910692')

        comment_test = Comment.objects.get(post=post)
        self.assertEqual(comment_test.name.sno, '518021910692')
        self.assertEqual(comment_test.content, '测试评论')

        message_test = Message.objects.get(title='测试私信标题')
        self.assertEqual(message_test.sender.sno, '518021910692')
        self.assertEqual(message_test.receiver.sno, '518021910691')
        self.assertEqual(message_test.content, '测试私信')


class UrlResponseTest(TestCase):
    def test_index(self):
        response = self.client.get('/bbs/')
        self.assertEqual(response.status_code, 302)

    def test_detail(self):
        response = self.client.get('/bbs/detail/')
        self.assertEqual(response.status_code, 404)

    def test_post_edit_page(self):
        response = self.client.get('/bbs/edit/<int:post_id>')
        self.assertEqual(response.status_code, 404)

    def test_post_edit_page_action(self):
        response = self.client.get('/bbs/edit/action/')
        self.assertEqual(response.status_code, 302)

    def test_like_post(self):
        response = self.client.get('/bbs/like/<int:post_id>')
        self.assertEqual(response.status_code, 404)

    def test_post_comment_page(self):
        response = self.client.get('/bbs/comment/<int:post_id>/<int:comment_id>')
        self.assertEqual(response.status_code, 404)

    def test_post_comment_page_action(self):
        response = self.client.get('/bbs/comment/action/')
        self.assertEqual(response.status_code, 302)

    def test_delete_comment(self):
        response = self.client.get('/bbs/delete/<int:comment_id>')
        self.assertEqual(response.status_code, 404)

    def test_delete_post(self):
        response = self.client.get('/bbs/delete_post/<int:post_id>')
        self.assertEqual(response.status_code, 404)

