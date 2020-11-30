"""
Models for the blog app. (post and comment)
"""

from django.contrib.auth import get_user_model
from django.db import models
from django.urls import reverse

User = get_user_model()

class Post(models.Model):
    """
    Defines post model
    """
    title = models.CharField(max_length=100)
    author = models.ForeignKey(User, models.SET_NULL, null=True)
    authorInfo = models.CharField(max_length=100)
    content = models.TextField()
    date = models.DateTimeField(auto_now=True)
    posted = models.BooleanField()
    def get_absolute_url(self):
        """
        get object URL to redirect after creation
        """
        return reverse('blog:article', kwargs={'pk': self.pk})

class Comment(models.Model):
    """
    Defines comment model
    """
    author = models.ForeignKey(User, models.SET_NULL, null=True)
    authorInfo = models.CharField(max_length=100)
    post = models.ForeignKey(Post, models.CASCADE, "comments")
    content = models.TextField(max_length=500)
    date = models.DateTimeField(auto_now=True)
    class Meta:
        ordering = ['-date']
    def get_absolute_url(self):
        """
        get object URL to redirect after creation
        """
        return reverse('article', kwargs={'pk': self.pk})
