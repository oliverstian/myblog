from django.db import models
from django.contrib.auth.models import AbstractUser
from imagekit.models import ProcessedImageField
from imagekit.processors import ResizeToFill


class BaseModel(models.Model):
    """模型抽象基类，其余的model都继承这个类，而不需要去继承model.Model了，定义了一些共有方法"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="更新时间")
    is_delete = models.BooleanField(default=False, verbose_name="删除标记")

    class Meta:
        abstract = True  # 指定是抽象模型类，只能继承不能实例化，不写这个迁移时会报错


class User(AbstractUser, BaseModel):
    """
    注意：由于xadmin是pip安装的，所以后面部署时源码会重新下载，到时需要把xadmin/plugins/auth.py
    替换掉新下载的，因为auth.UserAdmin改动了源码
    """
    website = models.URLField(verbose_name="个人网址", blank=True, null=True, help_text="必须以http(s)开头的完整形式")
    avatar = ProcessedImageField(upload_to='avatar/%Y/%m/%d',
                                 default='avatar/default.png',
                                 verbose_name='头像',
                                 format='PNG',  # 转换格式
                                 options={'quality': 60},
                                 processors=[ResizeToFill(80, 80)]
                                 )  # 把头像按配置修改后保存到media_root/avatar下，同时把图片路径保存到数据库

    class Meta:
        db_table = 'df_user'
        verbose_name = '用户信息'
        verbose_name_plural = verbose_name


















