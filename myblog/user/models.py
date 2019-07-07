from django.db import models
from django.contrib.auth.models import AbstractUser


class BaseModel(models.Model):
    """模型抽象基类，其余的model都继承这个类，而不需要去继承model.Model了，定义了一些共有方法"""
    create_time = models.DateTimeField(auto_now_add=True, verbose_name="创建时间")
    update_time = models.DateTimeField(auto_now_add=True, verbose_name="更新时间")
    is_delete = models.BooleanField(default=False, verbose_name="删除标记")

    class Meta:
        abstract = True  # 指定是抽象模型类，只能继承不能实例化，不写这个迁移时会报错


class User(AbstractUser, BaseModel):
    """用户模型类"""

    class Meta:
        db_table = 'df_user'
        verbose_name = '用户'
        verbose_name_plural = verbose_name

