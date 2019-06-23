from django.contrib import admin
from django.urls import reverse
from django.utils.html import format_html

from blog.models import Article, Category, Tag
from blog.adminforms import ArticleAdminForm
from myblog.base_admin import BaseOwnerAdmin


@admin.register(Category)
class CategoryAdmin(BaseOwnerAdmin):
    list_display = ("name", "status", "is_nav", "created_time", "owner")  # 展示的条目
    fields = (("name", "status"), "is_nav")  # 允许编辑的条目,name和status放同一行显示

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)


@admin.register(Tag)
class TagAdmin(BaseOwnerAdmin):
    list_display = ("name", "status", "created_time")
    fields = ("name", "status")

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(admin.SimpleListFilter):
    """自定义过滤器只展示当前用户分类"""

    title = "分类过滤器"
    parameter_name = 'owner_category'

    def lookups(self, request, model_admin):
        """右侧过滤器显示的选项，即该用户创建的所有分类。返回显示名称和id号（id号用于下面的queryset）"""
        return Category.objects.filter(owner=request.user).values_list("id", "name")  # owner和request.user都是User实例对象

    def queryset(self, request, queryset):
        """用户点击某分类后返回该分类下所有的文章。queryset参数是指Article.object.all()"""
        category_id = self.value()
        if category_id:
            return queryset.filter(category_id=self.value())  # category_id是分类的主键，因为数据库不能保存对象，所以把主键保存起来
        return queryset


@admin.register(Article)
class ArticleAdmin(BaseOwnerAdmin):
    form = ArticleAdminForm
    list_display = [
        "title", "category", "status",
        "created_time", "operator"
    ]
    list_display_links = ["title"]

    list_filter = [CategoryOwnerFilter]
    search_fields = ["title", "category__name"]

    actions_on_top = True
    actions_on_bottom = True

    save_on_top = True

    filter_horizontal = ("tag", )  # 多对多关系，实现一个水平的选择框

    fields = (
        ("category", "title"),  # 括号表示显示到一行
        "desc",
        "status",
        "content",
        "tag",
    )
    # fieldsets = (
    #     ("基础配置", {
    #         "description": "基础配置描述",
    #         "fields": (("title", "category"), "status"),
    #     }),
    #     ("内容", {
    #         "fields": ("desc", "content", ),
    #     }),
    #     ("额外信息", {
    #         "classes": ("collapse", ),
    #         "fields": ("tag", ),
    #     })
    # )

    def operator(self, obj):  # 参见官网list_display的四种值类型
        return format_html(
            '<a href="{}">编辑</a>',
            reverse('admin:blog_article_change', args=(obj.id, ))
        )
    operator.short_description = '操作'




















