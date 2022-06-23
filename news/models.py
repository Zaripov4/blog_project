from django.db import models
from django import forms


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=40)
    email = models.EmailField()


class News(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)
    category = models.ForeignKey
    picture = models.ImageField(upload_to='images/')


class Comment(models.Model):
    post = models.ForeignKey(News, on_delete=models.CASCADE, related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return 'Comment {} by {}'.format(self.body, self.name)
