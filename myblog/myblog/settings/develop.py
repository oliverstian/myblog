from myblog.settings.base import *  # NOQA 告诉pep8工具此处不需要检测


DEBUG = True

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'blog_develop',
        'USER': 'root',
        'PASSWORD': 'root',
        'HOST': '134.175.30.49',
        'PORT': 3306,
    },
}
