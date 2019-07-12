import xadmin
from comment.models import ArticleComment


@xadmin.sites.register(ArticleComment)
class CommentAdmin(object):
    list_display = ["author", "rep_to", "content", "belong", "created_time"]



