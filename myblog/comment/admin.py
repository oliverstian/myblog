from django.contrib import admin
from comment.models import ArticleComment


@admin.register(ArticleComment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ("rep_to", "author", "content", "belong", "created_time")



