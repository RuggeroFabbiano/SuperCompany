from django.contrib import admin
from .models import Post, Comment
from mediumeditor.admin import MediumEditorAdmin

@admin.register(Post)
class PostAdmin(MediumEditorAdmin, admin.ModelAdmin):
    mediumeditor_fields = ('title', 'content')
    search_fields = ['title', 'content']
    list_display = ['title', 'content', 'date']
    list_filter = ['title']
    list_editable = ['content']

@admin.register(Comment)
class CommentAdmin(MediumEditorAdmin, admin.ModelAdmin):
    mediumeditor_fields = ('content')
