from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse

class Post(models.Model):
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, models.SET_NULL, null=True)
    authorInfo = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    posted = models.BooleanField()
    def get_absolute_url(self):
        return reverse('blog:article', kwargs={'pk': self.pk})

class Comment(models.Model):
    author = models.ForeignKey(User, models.SET_NULL, null=True)
    authorInfo = models.CharField(max_length=100)
    post = models.ForeignKey(Post, models.CASCADE, "comments")
    content = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-date']
    def get_absolute_url(self):
        return reverse('article', kwargs={'pk': self.pk})
