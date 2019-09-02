import mistune
import markdown

from django.db import models
from django.contrib.auth.models import User
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


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
    WEIGHT_POST = 0
    WEIGHT_TOP_NORMAL = 1
    WEIGHT_TOP_IGNORE = 2
    WEIGHT_NORMAL = 3
    WEIGHT_ITEM = {  # 为了样式好看，置顶栏放了三个置顶文章，但是为了支持响应式，有一个在移动端会隐藏
        (WEIGHT_POST, "海报栏"),
        (WEIGHT_TOP_NORMAL, "凑数置顶栏"),  # 移动端忽略的文章，最好固定一篇就不要动了
        (WEIGHT_TOP_IGNORE, "置顶栏"),
        (WEIGHT_NORMAL, "普通栏"),
    }

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
    is_top = models.PositiveIntegerField(default=WEIGHT_NORMAL,
                                         choices=WEIGHT_ITEM, verbose_name="置顶")
    category = models.ForeignKey(Category, on_delete=models.CASCADE, verbose_name="分类")
    tag = models.ManyToManyField(Tag, verbose_name="标签")
    owner = models.ForeignKey("user.User", on_delete=models.CASCADE, verbose_name="作者")
    created_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    article_pic = ProcessedImageField(upload_to='article_pic/%Y/%m/%d',
                                      default="article_pic/default.png",
                                      verbose_name='文章配图',
                                      format='PNG',  # 转换格式
                                      options={'quality': 60},
                                      processors=[ResizeToFill(600, 300)],
                                      blank=True  # 后台修改时，可以为空，也就是说不改
                                      )
    pv = models.PositiveIntegerField(default=1)
    uv = models.PositiveIntegerField(default=1)

    class Meta:
        verbose_name = verbose_name_plural = "文章"
        ordering = ["is_top", "-id"]  # 根据id进行降序排列

    def __str__(self):
        return self.title

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







