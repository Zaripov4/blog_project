from django.db import models
from django.contrib.auth import get_user_model

User = get_user_model()


class Category(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name


class News(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)
    category = models.ForeignKey(
        Category, on_delete=models.RESTRICT, null=True, related_name='news'
    )
    picture = models.ImageField(upload_to='images/')
    views = models.IntegerField(default=0, editable=False)
    author = models.ForeignKey(
        User, on_delete=models.CASCADE, null=True, editable=False
    )
    like = models.ManyToManyField(User, related_name='news_like')
    dislike = models.ManyToManyField(User, related_name='news_dislike')

    def __str__(self):
        return self.title

    def number_of_likes(self):
        return self.like.count()

    def number_of_dislikes(self):
        return self.dislike.count()


class Comment(models.Model):
    post = models.ForeignKey(
        News, on_delete=models.CASCADE, related_name='comments'
    )
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created_on = models.DateTimeField(auto_now_add=True)
    active = models.BooleanField(default=False)

    class Meta:
        ordering = ['created_on']

    def __str__(self):
        return f'Comment {self.body} by {self.name}'
