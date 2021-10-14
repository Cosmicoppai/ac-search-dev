from django.apps import apps
from django.contrib import admin
from .models import Post, Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ['comment_id', 'post_id', 'author']
    list_filter = ['sub', 'author', 'date']
    list_display = ['sub', 'author', 'text']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['id', 'author', 'title']
    list_filter = ['sub', 'author', 'title', 'date']
    list_display = ['sub', 'author', 'title']
