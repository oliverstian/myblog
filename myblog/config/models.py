from django.db import models
from django.contrib.auth.models import User
from django.template.loader import render_to_string


class Link(models.Model):  # 友链
    models.Manager()
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEMS = {
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
    }
    title = models.CharField(max_length=50, verbose_name="标题")
    href = models.URLField(verbose_name="链接")  # 默认长度200
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEMS,
                                         verbose_name="状态")
    weight = models.PositiveIntegerField(default=1, choices=zip(range(1, 6), range(1, 6)),
                                         verbose_name="权重", help_text="权重越高展示越前")
    owner = models.ForeignKey("user.User", verbose_name="作者", on_delete=models.CASCADE)
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = "友链"

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by("-weight")


class SideBar(models.Model):
    STATUS_SHOW = 1
    STATUS_HIDE = 0
    STATUS_ITEM = {
        (STATUS_SHOW, "展示"),
        (STATUS_HIDE, "隐藏"),
    }

    DISPLAY_HTML = 1
    DISPLAY_LATEST = 2
    DISPLAY_HOT = 3
    DISPLAY_COMMENT = 4
    SIDE_TYPE = (
        (DISPLAY_HTML, "HTML"),
        (DISPLAY_LATEST, "最新文章"),
        (DISPLAY_HOT, "最热文章"),
        (DISPLAY_COMMENT, "最近评论"),
    )
    title = models.CharField(max_length=50, verbose_name="标题")  # 后续把这个去掉，只留下展示类型（也就是侧栏有几种展示类型）
    display_type = models.PositiveIntegerField(default=1, choices=SIDE_TYPE,
                                               verbose_name="展示类型")
    content = models.CharField(max_length=500, blank=True, verbose_name="内容",  # 这个可以留着，可以作为备注
                               help_text="如果设置的不是HTML类型，可为空")
    status = models.PositiveIntegerField(default=STATUS_SHOW, choices=STATUS_ITEM,
                                         verbose_name="状态")
    owner = models.ForeignKey("user.User", on_delete=models.CASCADE, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = verbose_name_plural = "侧边栏"

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_SHOW)

    @property
    def content_html(self):
        """直接渲染模板"""
        from blog.models import Article  # 避免循环引用，即避免在article中又引入sidebar
        from comment.models import Comment

        result = ''
        if self.display_type == self.DISPLAY_HTML:
            result = self.content
        elif self.display_type == self.DISPLAY_LATEST:
            context = {
                "articles": Article.latest_article()
            }
            result = render_to_string("config/block/sidebar_articles.html", context)
        elif self.display_type == self.DISPLAY_HOT:
            context = {
                "articles": Article.hot_article()
            }
            result = render_to_string("config/block/sidebar_articles.html", context)
        elif self.display_type == self.DISPLAY_COMMENT:
            context = {
                "comments": Comment.objects.filter(status=Comment.STATUS_NORMAL)
            }
            result = render_to_string("config/block/sidebar_comments.html", context)
        return result






















































