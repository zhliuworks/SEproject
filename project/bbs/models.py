from django.db import models
from login.models import User


class Category(models.Model):
    name = models.CharField('名称', max_length=16)

    def __str__(self):
        return self.name


class Tag(models.Model):
    name = models.CharField('名称', max_length=16)

    def __str__(self):
        return self.name


class Post(models.Model):
    title = models.CharField(max_length=32)
    content = models.TextField(null=True)
    create_time = models.DateTimeField('创建时间', auto_now_add=True)
    author = models.ForeignKey(to='login.User', on_delete=models.CASCADE, verbose_name='作者', related_name='author')
    likes = models.IntegerField(default=0)
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name='分类')
    tags = models.ManyToManyField(Tag, verbose_name='标签')
    like_users = models.ManyToManyField(User, verbose_name='用户', related_name='like_users')

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, verbose_name='帖子')
    name = models.ForeignKey(to='login.User', related_name='comments', on_delete=models.CASCADE, verbose_name='评论者')
    content = models.TextField(verbose_name='内容')
    created = models.DateTimeField('发布时间', auto_now_add=True)
    root = models.ForeignKey('self', related_name='root_comment', null=True, blank=True, on_delete=models.CASCADE)
    parent = models.ForeignKey('self', related_name='parent_comment', null=True, blank=True, on_delete=models.CASCADE)
    reply_to = models.ForeignKey(to='login.User', related_name="replies", blank=True, null=True, on_delete=models.CASCADE)

    def __str__(self):
        return self.content
