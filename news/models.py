from django.db import models


class User(models.Model):
    username = models.CharField(max_length=50)
    password = models.CharField(max_length=40)
    email = models.EmailField()


class News(models.Model):
    title = models.CharField(max_length=100)
    body = models.CharField(max_length=1000)
    category = models.ForeignKey
    picture = models.ImageField(upload_to='images/')
