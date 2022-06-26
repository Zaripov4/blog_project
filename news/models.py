from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class News(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)
    category = models.ForeignKey
    picture = models.ImageField(upload_to='images/')
    views = models.IntegerField(default=0, editable=False)
    author = models.ForeignKey(User, on_delete=models.CASCADE, null=True, editable=False)

    def __str__(self):
        return self.title


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
        return f'Comment {self.body} by {self.name}'
