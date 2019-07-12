from django.db import models
from blog.models import Article


class Comment(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEM = {
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
    }
    # target = models.ForeignKey(Article, on_delete=models.CASCADE, verbose_name="评论目标")
    author = models.ForeignKey("user.User", on_delete=models.CASCADE, verbose_name="评论人")
    content = models.CharField(max_length=2000, verbose_name="评论内容")

    """%(class)s表示子类的类名小写"""
    parent = models.ForeignKey("self", null=True, related_name='%(class)s_child_comments', on_delete=models.CASCADE, verbose_name="父评论", blank=True)
    rep_to = models.ForeignKey("self", related_name='%(class)s_rep_comments', on_delete=models.CASCADE, verbose_name="回复", blank=True, null=True)
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEM,
                                         verbose_name="状态")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    class Meta:
        '''这是一个元类，用来继承的'''
        abstract = True


class ArticleComment(Comment):
    belong = models.ForeignKey(Article, on_delete=models.CASCADE, related_name='article_comments', verbose_name='所属文章')

    def __str__(self):
        return self.author.username

    class Meta:
        verbose_name = '文章评论'
        verbose_name_plural = verbose_name
        ordering = ['created_time']

    # def save(self, *args, **kwargs):  # for test
    #     self.parent = None
    #     super(ArticleComment, self).save(*args, **kwargs)













































