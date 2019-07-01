import mistune
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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
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
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    def __str__(self):
        return self.name

    class Meta:
        verbose_name = verbose_name_plural = "标签"

    @classmethod
    def get_all(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL)


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
    content_html = models.TextField(verbose_name="正文HTML代码", blank=True, editable=False)
    status = models.PositiveIntegerField(default=STATUS_NORMAL,
                                         choices=STATUS_ITEM, verbose_name="状态")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="分类")
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    owner = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")

    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ["-id"]  # 根据id进行降序排列

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
    def hot_article(cls):
        return cls.objects.filter(status=cls.STATUS_NORMAL).order_by("-pv")

    def save(self, *args, **kwargs):
        self.content_html = mistune.markdown(self.content)  # 展示文章用这个字段。编辑文章用Markdown，展示用HTML格式
        super(Article, self).save(*args, **kwargs)






