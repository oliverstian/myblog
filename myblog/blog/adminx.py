import xadmin
from xadmin import views

from xadmin.layout import Row, Fieldset
from xadmin.filters import RelatedFieldListFilter
from xadmin.filters import manager

from django.urls import reverse
from django.utils.html import format_html

from blog.models import Article, Category, Tag
from blog.adminforms import ArticleAdminForm
from myblog.base_xadmin import BaseOwnerXadmin
"""
关于admin和xadmin的笔记记在此处。
1、后台关联每一个注册的model，如果不自定义显示样式，仅是注册（即不定义class CategoryAdmin()类，xadmin好像必须定义）则是默认显示样式。
2、后台会对每个model提供增删改查四个url，实现对表的增删改查
3、xadmin使用crispy_forms来管理django的form表单（比如加入id或class属性，指定表单提交方式等，创建表单还是django.forms）,
使用方法参考官网：https://django-crispy-forms.readthedocs.io
4、xadmin.layout.py定义了一些用来布局的类（均继承自crispy_forms.layout），布局框架用的bootstrap
"""


# **************** 后台的全局设置开始，放在blog APP这里 ***************

@xadmin.sites.register(views.BaseAdminView)  # 页面基础设置
class BaseSetting(object):
    enable_themes = True  # 增加主题设置选项
    use_bootswatch = True  # 增加主题设置下拉菜单


@xadmin.sites.register(views.CommAdminView)  # 全局设置
class GlobalSetting(object):
    site_title = "Blog of OliverTian"  # 左上角logo
    site_footer = "olvertian个人博客"  # 页面底部标识
    menu_style = "accordion"  # 左侧导航栏的菜单栏改为下拉式

# *********************** 后台的全局设置结束 ***********************


# ********************* 对blog APP下的所有model的设置开始 *****************
# ####### 主要注释在ArticleAdmin那里

@xadmin.sites.register(Category)
class CategoryAdmin(BaseOwnerXadmin):
    list_display = ("name", "status", "is_nav", "created_time", "owner")
    fields = (("name", "status"), "is_nav")

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(CategoryAdmin, self).save_model(request, obj, form, change)


@xadmin.sites.register(Tag)
class TagAdmin(BaseOwnerXadmin):
    list_display = ("name", "status", "created_time")
    fields = ("name", "status")

    def save_model(self, request, obj, form, change):
        obj.owner = request.user
        return super(TagAdmin, self).save_model(request, obj, form, change)


class CategoryOwnerFilter(RelatedFieldListFilter):

    @classmethod
    def test(cls, field, request, params, model, admin_view, field_path):
        return field.name == 'category'

    def __init__(self, field, request, params, model, model_admin, field_path):
        super().__init__(field, request, params, model, model_admin, field_path)
        # 重新获取lookup_choices，根据owner过滤
        self.lookup_choices = Category.objects.filter(owner=request.user).values_list('id', 'name')


manager.register(CategoryOwnerFilter, take_priority=True)


@xadmin.sites.register(Article)  # 注册之后就能在后台看到，但是显示样式是默认的
class ArticleAdmin(BaseOwnerXadmin):  # 这玩意是个元类（用来创建类的类）
    """xadmin界面使用cripy_forms作为表单（类似于django内置form），所以布局要按照cripy_froms"""
    form = ArticleAdminForm
    list_display = [  # 显示的字段
        "title", "category", "status",
        "created_time", "is_top", "operator",
    ]

    list_display_links = ["title", "category"]  # 默认每一行只允许第一个字段可点击进入编辑数据行，在这里添加可点击编辑数据行的字段
    list_filter = ["category", "tag", "is_top"]  # 侧栏（admin）或导航栏(xadmin)中过滤器使用的字段
    search_fields = ["title", "category__name"]  # 输入关键字，用关键字在这些字段中去匹配。多个字段间是或的关系
    list_editable = ["title"]  # 可直接在列表中修改的字段，注意这里指单独修改数据行中的某个字段
    ordering = ["is_top", "created_time"]  # 排序
    filter_horizontal = ("tag", )  # 多对多关系，实现一个水平的选择框

    # actions_on_top = True
    # actions_on_bottom = True
    # save_on_top = True

    """
    form_layout对应编辑页面中，model中各字段的排版
    Fieldset在xadmin模块的layout.py中，该模块还定义了其他布局类，
    比如col、container等（对应到bootstrap的class就能明白啥意思了，均继承自crispy_forms.layout）
    """
    form_layout = (
        Fieldset(  # 一个fieldset相当于一个独立排版的模块
            '基础信息',
            Row("title", "category"),  # 排版在同一行
            Row('status', "is_top"),
            'tag',
        ),
        Fieldset(
            '内容信息',
            'desc',
            'is_md',
            'content_ck',
            'content_md',
            'content',
            "article_pic",
        )

    )

    def operator(self, obj):  # 参见官网list_display的四种值类型
        """
        把这个函数名放在list_display里面，会新增一个字段显示这个函数的返回值,但是这个函数
        不能放在list_display_links中
        """
        return format_html(  # 相比于 mark_safe()，官网更推荐format_html这种方式https://docs.djangoproject.com/en/2.2/howto/custom-template-tags/#howto-writing-custom-template-tags（simple tags那里）
            '<a href="{}">编辑</a>',
            reverse('xadmin:blog_article_change', args=(obj.id, ))
        )
    operator.short_description = '操作'

    def delete_article(self, request, queryset):  # queryset就是页面中选中的那些实例
        queryset.delete()  # 使用的queryset的delete方法将选中的实例删除，还有update方法等，详情官网，内容不多
    delete_article.short_description = "删除所选文章_by_oliver"

    actions = [delete_article]  # 动作列表，即批量操作，详情官网，admin action那一节，内容不多，很好理解

# ************************* 对blog APP下所有model设置结束 ********************


# ************************ 对blog APP本身设置开始 ************************

# 对各个APP的设置放在各APP下的apps.py中

# ************************ 对blog APP本身设置结束 ************************











