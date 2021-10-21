from django.apps import apps
from django.contrib import admin
from .models import Post, Comment


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    search_fields = ['comment_id', 'post_id', 'username']
    list_filter = ['sub', 'username', 'create_date', 'post_id']
    list_display = ['sub', 'username', 'text']


@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    search_fields = ['post_id', 'username', 'title']
    list_filter = ['sub', 'username', 'create_date', ]
    list_display = ['sub', 'username', 'title']
