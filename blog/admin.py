"""
Admin. registration module
"""

from django.contrib import admin
from mediumeditor.admin import MediumEditorAdmin
from .models import Post, Comment


@admin.register(Post)
class PostAdmin(MediumEditorAdmin, admin.ModelAdmin):
    """
    Admin. registration for post model
    """

    mediumeditor_fields = ('title', 'content')
    search_fields = ['title', 'content']
    list_display = ['title', 'content', 'date']
    list_filter = ['title']
    list_editable = ['content']

@admin.register(Comment)
class CommentAdmin(MediumEditorAdmin, admin.ModelAdmin):
    """
    Admin. registration for comment model
    """

    mediumeditor_fields = ('content')
