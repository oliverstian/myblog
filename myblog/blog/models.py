import mistune
import markdown

from django.db import models
from django.contrib.auth.models import User


class Category(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEM = {
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
    }

    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEM,
                                         verbose_name="状态")
    is_nav = models.BooleanField(default=False, verbose_name="是否为导航")
    owner = models.ForeignKey("user.User", on_delete=models.CASCADE, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "分类"

    @classmethod
    def get_navs(cls):
        nav_category = []
        normal_category = []
        categories = cls.objects.filter(status=cls.STATUS_NORMAL)
        for category in categories:
            if category.is_nav:
                nav_category.append(category)
            else:
                normal_category.append(category)

        return {
            "nav_category": nav_category,
            "normal_category": normal_category
        }


class Tag(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_ITEM = {
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
    }

    name = models.CharField(max_length=50, verbose_name="名称")
    status = models.PositiveIntegerField(default=STATUS_NORMAL, choices=STATUS_ITEM,
                                         verbose_name="状态")
    owner = models.ForeignKey("user.User", on_delete=models.CASCADE, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "标签"

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL)

    def article_nums(self):  # 返回该标签实例下的文章数
        return self.article_set.count()


class Article(models.Model):
    STATUS_NORMAL = 1
    STATUS_DELETE = 0
    STATUS_DRAFT = 2
    STATUS_ITEM = {
        (STATUS_NORMAL, "正常"),
        (STATUS_DELETE, "删除"),
        (STATUS_DRAFT, "草稿"),
    }

    title = models.CharField(max_length=255, verbose_name="标题")
    desc = models.CharField(max_length=1024, blank=True, verbose_name="摘要")
    content = models.TextField(verbose_name="正文", help_text="必须为MarkDown格式")
    is_md = models.BooleanField(default=False, verbose_name="markdown")
    content_html = models.TextField(verbose_name="正文HTML代码", blank=True, editable=False)
    content_toc = models.TextField(verbose_name="文章目录", null=True, blank=True, editable=False)
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEM, verbose_name="状态")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="分类")
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    owner = models.ForeignKey("user.User", on_delete=models.CASCADE, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ["-id"]  # 根据id进行降序排列

    def save(self, *args, **kwargs):
        """
        保存两份的好处是，博客写操作往往只有很少次（写、改），而读有很多次，如果数据库中保存的
        是Markdown格式，则每次取数据都要转换成HTML，这样不科学，所以最好是写入时转换一次
        """
        # self.content_html = mistune.markdown(self.content)  # 展示文章用这个字段。编辑文章用Markdown，展示用HTML格式
        if self.is_md:
            md = markdown.Markdown(extensions=[
                                        'markdown.extensions.extra',
                                        'markdown.extensions.codehilite',
                                        'markdown.extensions.toc',
                                        ])
            self.content_html = md.convert(self.content)
            self.content_toc = md.toc  # 文章目录
        else:
            self.content_html = self.content
            self.content_toc = None  # 简单根据这个判断有没有目录
        super(Article, self).save(*args, **kwargs)

    def time_short_format(self):
        return str(self.created_time).split(" ")[0]  # 把具体时刻去掉，只留下年月日

    @staticmethod
    def get_by_tag(tag_id):
        if tag_id:
            try:
                tag = Tag.objects.get(id=tag_id)
            except Tag.DoesNotExist:
                article_ls = []
                tag = None
            else:
                article_ls = tag.article_set.filter(status=Article.STATUS_NORMAL)\
                    .select_related("owner", "category")
        else:
            article_ls = []
            tag = None
        return article_ls, tag

    @staticmethod
    def get_by_category(category_id):
        try:
            category = Category.objects.get(id=category_id)
        except Category.DoesNotExist:
            category = None
            article_ls = []
        else:
            article_ls = category.article_set.filter(status=Article.STATUS_NORMAL)\
                .select_related("owner", "category")
        return article_ls, category

    @classmethod
    def latest_article(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL)
        return queryset

    @classmethod
    def get_newest_article(cls):
        queryset = cls.objects.filter(status=cls.STATUS_NORMAL).order_by("created_time")[:5]
        return queryset

    @classmethod
    def hot_article(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by("-pv")[:5]







