from myblog.settings.base import *  # NOQA 告诉pep8工具此处不需要检测


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog_develop',
        'USER': 'olivertian',  # root用户限制了只允许localhost登陆，oliver这个也有所有root权限
        'PASSWORD': '181855makesi',
        'HOST': '134.175.30.49',
        'PORT': 3306,
    },
}
