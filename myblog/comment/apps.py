from django.apps import AppConfig


class CommentConfig(AppConfig):
    name = 'comment'  # 数据库中各app下数据表的前缀？
    verbose_name = "评论"
