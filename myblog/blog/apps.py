from django.apps import AppConfig


class BlogConfig(AppConfig):
    """
    就像对每个model都有配置一样，这里是对整个blog app的配置。
    注意配置好这个后，需要在blog.__init__.py下写上如下一句
    default_app_config = "blog.apps.BlogConfig"，让xadmin
    导入blog模块时找到这个配置信息
    """
    name = 'blog'
    verbose_name = "博客应用"  # 这个app在后台显示的名称
